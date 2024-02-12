"""LlamaPack class."""
from typing import Any, Dict, List
from prompts import DEFAULT_TRANSFORM_QUERY_TEMPLATE, DEFAULT_RELEVANCY_PROMPT_TEMPLATE

from llama_index import VectorStoreIndex, SummaryIndex
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.llms import OpenAI
from llama_index.schema import Document, NodeWithScore
from llama_index.query_pipeline.query import QueryPipeline
from llama_hub.tools.tavily_research.base import TavilyToolSpec


class CorrectiveRAGPack(BaseLlamaPack):
    def __init__(self, documents: List[Document], tavily_ai_apikey: str) -> None:
        """Init params."""

        llm = OpenAI(model="gpt-4")
        self.relevancy_pipeline = QueryPipeline(
            chain=[DEFAULT_RELEVANCY_PROMPT_TEMPLATE, llm]
        )
        self.transform_query_pipeline = QueryPipeline(
            chain=[DEFAULT_TRANSFORM_QUERY_TEMPLATE, llm]
        )

        self.llm = llm
        self.index = VectorStoreIndex.from_documents(documents)
        self.tavily_tool = TavilyToolSpec(api_key=tavily_ai_apikey)

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {"llm": self.llm, "index": self.index}

    def retrieve_nodes(self, query_str: str, **kwargs: Any) -> List[NodeWithScore]:
        """Retrieve the relevant nodes for the query"""
        retriever = self.index.as_retriever(**kwargs)
        return retriever.retrieve(query_str)

    def evaluate_relevancy(
        self, retrieved_nodes: List[Document], query_str: str
    ) -> List[str]:
        """Evaluate relevancy of retrieved documents with the query"""
        relevancy_results = []
        for node in retrieved_nodes:
            relevancy = self.relevancy_pipeline.run(
                context_str=node.text, query_str=query_str
            )
            relevancy_results.append(relevancy.message.content.lower().strip())
        return relevancy_results

    def extract_relevant_texts(
        self, retrieved_nodes: List[NodeWithScore], relevancy_results: List[str]
    ) -> str:
        """Extract relevant texts from retrieved documents"""
        relevant_texts = [
            retrieved_nodes[i].text
            for i, result in enumerate(relevancy_results)
            if result == "yes"
        ]
        return "\n".join(relevant_texts)

    def search_with_transformed_query(self, query_str: str) -> str:
        """Search the transformed query with Tavily API"""
        search_results = self.tavily_tool.search(query_str, max_results=2)
        return "\n".join([result.text for result in search_results])

    def get_result(self, relevant_text: str, search_text: str, query_str: str) -> Any:
        """Get result with relevant text"""
        documents = [Document(text=relevant_text + "\n" + search_text)]
        index = SummaryIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        return query_engine.query(query_str)

    def run(self, query_str: str, **kwargs: Any) -> Any:
        """Run the pipeline."""
        # Retrieve nodes based on the input query string.
        retrieved_nodes = self.retrieve_nodes(query_str, **kwargs)

        # Evaluate the relevancy of each retrieved document in relation to the query string.
        relevancy_results = self.evaluate_relevancy(retrieved_nodes, query_str)

        # Extract texts from documents that are deemed relevant based on the evaluation.
        relevant_text = self.extract_relevant_texts(retrieved_nodes, relevancy_results)

        # Initialize search_text variable to handle cases where it might not get defined.
        search_text = ""

        # If any document is found irrelevant, transform the query string for better search results.
        if "no" in relevancy_results:
            transformed_query_str = self.transform_query_pipeline.run(
                query_str=query_str
            ).message.content

            # Conduct a search with the transformed query string and collect the results.
            search_text = self.search_with_transformed_query(transformed_query_str)

        # Compile the final result. If there's additional search text from the transformed query,
        # it's included; otherwise, only the relevant text from the initial retrieval is returned.
        if search_text:
            return self.get_result(relevant_text, search_text, query_str)
        else:
            return self.get_result(relevant_text, "", query_str)
