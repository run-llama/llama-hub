"""RAG Fusion Pipeline."""

from llama_index.query_pipeline import QueryPipeline, QueryComponent, InputComponent
from typing import Dict, Any, List, Optional
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.agent import AgentRunner
from llama_index.llms.llm import LLM
from llama_index.llms.openai import OpenAI
from llama_index.tools.types import BaseTool
from llama_index.callbacks import CallbackManager
from llama_index import Document, VectorStoreIndex, ServiceContext
from llama_index.response_synthesizers import TreeSummarize

DEFAULT_CHUNK_SIZES = chunk_sizes = [128, 256, 512, 1024]


class RAGFusionPipelinePack(BaseLlamaPack):
    """RAG Fusion pipeline.

    Create a bunch of vector indexes of different chunk sizes.
    
    """

    def __init__(
        self,
        documents: List[Document],
        llm: Optional[LLM] = None,
        chunk_size: Optional[List[int]] = None
    ) -> None:
        """Init params."""
        self.documents = documents
        self.chunk_sizes = chunk_sizes or DEFAULT_CHUNK_SIZES

        # construct index
        self.llm = llm or OpenAI(model="gpt-3.5-turbo")

        service_contexts = []
        vector_indices = []
        query_engines = []
        self.retrievers = {}
        for chunk_size in chunk_sizes:
            service_context = ServiceContext.from_defaults(
                chunk_size=chunk_size, llm=llm
            )
            service_contexts.append(service_context)
            nodes = service_context.node_parser.get_nodes_from_documents(documents)

            vector_index = VectorStoreIndex(
                nodes, service_context=service_context
            )
            vector_indices.append(vector_index)
            query_engines.append(vector_index.as_query_engine())

            self.retrievers[chunk_size] = vector_index.as_retriever()

        # construct query pipeline
        p = QueryPipeline()
        module_dict = {
            **self.retrievers,
            "input": InputComponent(),
            "summarizer": TreeSummarize()
            # TODO: Join component:
            "join": JoinComponent()
        }
        p.add_modules(module_dict)
        # add links
        for chunk_size in chunk_sizes:
            p.link("input", chunk_size)
            p.link(chunk_size, "join")

        self.query_pipeline = p

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "vector_index": self.vector_index,
            "query_pipeline": self.query_pipeline,
        }

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.query_pipeline.query(*args, **kwargs)
