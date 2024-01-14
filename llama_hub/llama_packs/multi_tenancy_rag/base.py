from typing import Any, Dict, List
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.schema import Document
from llama_index.vector_stores.types import MetadataFilters, ExactMatchFilter


class MultiTenancyRAGPack(BaseLlamaPack):
    def __init__(self) -> None:
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        service_context = ServiceContext.from_defaults(llm=llm)
        self.llm = llm
        self.index = VectorStoreIndex.from_documents(
            documents=[], service_context=service_context
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {"llm": self.llm, "index": self.index}

    def add(self, documents: List[Document], user: Any) -> None:
        """Insert Documents of a user into index"""
        for document in documents:
            document.metadata["user"] = user
            self.index.insert(document)

    def run(self, query_str: str, user: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        query_engine = self.index.as_query_engine(
            filters=MetadataFilters(
                filters=[
                    ExactMatchFilter(
                        key="user",
                        value=user,
                    )
                ]
            ),
            **kwargs
        )
        return query_engine.query(query_str)
