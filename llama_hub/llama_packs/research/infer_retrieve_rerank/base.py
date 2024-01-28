"""Infer-Retrieve-Rerank Pack.

Taken from this paper: https://arxiv.org/pdf/2401.12178.pdf.

"""


from typing import Any, Dict, Optional

from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.llms import Replicate
from llama_index.schema import TextNode
from llama_index.embeddings import OpenAIEmbedding
from llama_index.ingestion import IngestionPipeline
from llama_index import VectorStoreIndex
from llama_index.retrievers import BaseRetriever
from llama_index.llms.llm import LLM
from llama_index.llms import OpenAI
from llama_index.prompts import PromptTemplate
from llama_index.query_pipeline import QueryPipeline
from llama_index.postprocessor.types import BaseNodePostprocessor
from llama_index.postprocessor.rankGPT_rerank import RankGPTRerank
from llama_index.output_parsers import ChainableOutputParser
from typing import List

INFER_PROMPT_STR = """\

Your job is to output a list of predictions given context from a given piece of text. The text context,
and information regarding the set of valid predictions is given below. 

Return the predictions as a comma-separated list of strings.

Text Context:
{doc_context}

Prediction Info:
{pred_context}

Predictions: """

INFER_PROMPT_TMPL = PromptTemplate(INFER_PROMPT_STR)


class PredsOutputParser(ChainableOutputParser):
    """Predictions output parser."""

    def parse(self, output: str) -> List[str]:
        """Parse predictions."""
        tokens = output.split(",")
        return [t.strip() for t in tokens]

preds_output_parser = PredsOutputParser()


RERANK_PROMPT_STR = """\
Given a piece of text, rank the {num} passages above based on their relevance \
to this piece of text. The passages \
should be listed in descending order using identifiers. \
The most relevant passages should be listed first. \
The output format should be [] > [], e.g., [1] > [2]. \
Only response the ranking results, \
do not say any word or explain. \

Here is a given piece of text: {query}. 

"""
RERANK_PROMPT_TMPL = PromptTemplate(RERANK_PROMPT_STR)


def infer_retrieve_rerank(
    query: str,
    retriever: BaseRetriever,
    llm: LLM,
    pred_context: str,
    infer_prompt: PromptTemplate,
    rerank_prompt: PromptTemplate,
    reranker_top_n: int = 3,
) -> List[str]:
    """Infer retrieve rerank."""
    infer_prompt_c = infer_prompt.as_query_component(
        partial={"pred_context": pred_context}
    )
    infer_pipeline = QueryPipeline(chain=[infer_prompt_c, llm, preds_output_parser])
    preds = infer_pipeline.run(query)

    all_nodes = []
    for pred in preds:
        nodes = retriever.retrieve(str(pred))
        all_nodes.extend(nodes)

    reranker = RankGPTRerank(
        llm=llm,
        top_n=reranker_top_n,
        rankgpt_rerank_prompt=rerank_prompt,
        # verbose=True,
    )
    reranked_nodes = reranker.postprocess_nodes(all_nodes, query_str=query)
    return [n.get_content() for n in reranked_nodes]


class InferRetrieveRerankPack(BaseLlamaPack):
    """Infer Retrieve Rerank pack."""

    def __init__(
        self,
        labels: List[str],
        llm: Optional[LLM] = None,
        pred_context: str = "",
        reranker_top_n: int = 3,
    ) -> None:
        """Init params."""
        # NOTE: we use 16k model by default to fit longer contexts
        self.llm = llm or OpenAI(model="gpt-3.5-turbo-16k")
        label_nodes = [TextNode(text=l) for l in labels]
        pipeline = IngestionPipeline(transformations=[OpenAIEmbedding()])
        label_nodes_w_embed = pipeline.run(documents=label_nodes)

        index = VectorStoreIndex(label_nodes_w_embed)
        self.label_retriever = index.as_retriever(similarity_top_k=2)
        self.pred_context = pred_context
        self.reranker_top_n = reranker_top_n

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "llm": self.llm,
            "label_retriever": self.label_retriever,
        }

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        inputs = kwargs.get("inputs", [])
        pred_reactions = []
        for idx, input in enumerate(inputs):
            cur_pred_reactions = infer_retrieve_rerank(
                input,
                self.label_retriever,
                self.llm,
                self.pred_context,
                reranker_top_n=self.reranker_top_n
            )

            pred_reactions.append(cur_pred_reactions)

        return pred_reactions
