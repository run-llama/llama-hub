from typing import Any, Dict, List, Optional

import numpy as np
from llama_index import Document, VectorStoreIndex
from llama_index.bridge.pydantic import BaseModel, Field
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.llms import OpenAI
from llama_index.llms.llm import LLM
from llama_index.llms.types import ChatMessage, MessageRole
from llama_index.prompts import PromptTemplate
from sklearn.mixture import GaussianMixture
from umap import UMAP

SUMMARY_PROMPT_STR = """Write a summary of the following, including as many key details as
possible: {context}"""
SUMMARY_PROMPT = PromptTemplate(SUMMARY_PROMPT_STR)


class ClusteringModule(BaseModel):
    n_components: int = Field(
        default=64, description="dimensionality of the reduced dimension space"
    )
    metric: str = Field(
        default="cosine",
        description="Controls how distance is computed in the ambient space of the input data",
    )
    n_neighbors_list: List[int] = Field(
        default=[10, 25, 50],
        description="Controls how UMAP balances local versus global structure in the data.",
    )

    def __init__(
        self, n_components: int, metric: str, n_neighbors_list: List[int], max_ctx: int
    ) -> None:
        self.umap_list = [
            UMAP(n_neighbors=n_neighbors, n_components=n_components, metric=metric)
            for n_neighbors in n_neighbors_list
        ]
        self.max_ctx = max_ctx

    def _get_optimal_clusters(embeddings: List[List[float]]) -> List[int]:
        """Find the optimal cluster

        Args:
            embeddings (List[List[float]]): Embeddings

        Returns:
            List[int]: List of clusters for each vector
        """
        best_bic = np.inf
        best_clusters = None

        for n_clusters in range(1, 7):
            gmm = GaussianMixture(n_components=n_clusters)
            clusters = gmm.fit_predict(embeddings)
            bic = gmm.bic(embeddings)
            if bic < best_bic:
                best_bic = bic
                best_clusters = clusters

        return best_clusters

    def __call__(
        self, documents: List[str], embeddings: List[List[float]]
    ) -> List[List[str]]:
        """Group documents using clustering algorithm

        Args:
            documents (List[str]): List of documents
            embeddings (List[List[float]]): Their corresponsing embeddings

        Returns:
            List[List[str]]: List of documents grouped per cluster
        """
        # TODO recursive clustering on clusters with documents exceeding the max_ctx
        summary_documents = []
        for umap in self.umap_list:
            reduced_embeddings = umap.fit_transform(embeddings)
            clusters = self._get_optimal_clusters(reduced_embeddings)
            cluster_to_documents = {}
            for cluster, document in zip(clusters, documents):
                cluster_to_documents.get(cluster, []).append(document)

            summary_documents.append(cluster_to_documents.values())

        return summary_documents


class SummaryModule(BaseModel):
    llm: LLM = Field(..., description="LLM")
    summary_prompt: PromptTemplate = Field(
        default=SUMMARY_PROMPT, description="Summary prompt template"
    )

    def __init__(self, llm: LLM, summary_prompt: PromptTemplate) -> None:
        llm = llm or OpenAI(model="gpt-3.5-turbo")
        self.summary_prompt = summary_prompt

    def __call__(self, documents_per_cluster: List[str]) -> List[str]:
        """Generate summaries of documents per cluster

        Args:
            documents_per_cluster (List[str]): List of documents per cluster

        Returns:
            List[str]: List of summary for each cluster
        """
        summary = []
        for documents in documents_per_cluster:
            messages = [
                ChatMessage(
                    role=MessageRole.SYSTEM, content="You are a Summarizing Text Portal"
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=self.summary_prompt.as_query_component(
                        partial={"context": "\n".join(documents)}
                    ),
                ),
            ]

            summary.append(self.llm.chat(messages).message.content)
        return summary


class RaptorIndexingEngine(BaseModel):
    """Raptor indexing engine."""

    llm: LLM = Field(..., description="llm")
    index: VectorStoreIndex = Field(..., description="index")
    tree_depth: int = Field(default=3, description="Summary tree depth")
    summary_module: SummaryModule = Field(..., description="Summary module")
    clustering_module: ClusteringModule = Field(..., description="Clustering Module")
    verbose: bool = Field(default=True, description="Verbose.")

    def __init__(
        self,
        index: VectorStoreIndex,
        llm: LLM,
        tree_depth: int,
        summary_module: Optional[SummaryModule] = None,
        clustering_module: Optional[ClusteringModule] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(verbose=verbose, **kwargs)
        self.index = index
        self.llm = llm or OpenAI(model="gpt-3.5-turbo")
        self.tree_depth = tree_depth
        self.summary_module = summary_module or SummaryModule(llm=llm)
        self.clustering_module = clustering_module or ClusteringModule()

    def _get_embeddings_per_level(self, level: int = 0) -> List[float]:
        """Retrieve embeddings per level in the abstraction tree

        Args:
            level (int, optional): Target level. Defaults to 0 which stands for leaf nodes.

        Returns:
            List[float]: List of embeddings
        """
        vector_store = self.index.vector_store
        node_dict = self.index.index_struct.nodes_dict
        docstore = self.index.docstore
        target_vectors = node_dict.keys()

        if level > 0:
            target_vectors = [
                vector_id
                for vector_id, document_id in node_dict.items()
                if docstore.get_document(document_id).metadata["level"] == level
            ]
        return [vector_store.get(vector_id) for vector_id in target_vectors]

    def insert_abstractions(self, documents: List[Document]) -> None:
        """Given a set of documents, this function inserts higher level of abstractions within the index
        For later retrieval

        Args:
            documents (List[Document]): List of Documents
        """
        for level in range(self.tree_depth):
            embeddings = self._get_embeddings_per_level(level=level)
            documents_per_cluster = self.clustering_module(documents, embeddings)
            summaries_per_cluster = self.summary_module(documents_per_cluster)
            summaries_per_cluster = [
                Document(text=summary, metadata={"level": level})
                for summary in summaries_per_cluster
            ]
            self.index.insert_nodes(summaries_per_cluster)
            documents = summaries_per_cluster


class RaptorPack(BaseLlamaPack):
    """Raptor pack."""

    def __init__(
        self,
        llm: Optional[LLM] = None,
        verbose: bool = False,
        **kwargs: Any,
    ) -> None:
        """Init params."""

        self.indexing_engine = RaptorIndexingEngine(
            llm=llm,
            verbose=verbose,
            **kwargs,
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "indexing_engine": self.indexing_engine,
            "llm": self.indexing_engine.llm,
        }

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.indexing_engine.insert_abstractions(*args, **kwargs)
