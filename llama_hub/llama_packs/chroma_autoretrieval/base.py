"""Chroma Auto-retrieval Pack."""


from typing import Any, Dict, List, Optional

from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.indices.vector_store.retrievers import (
    VectorIndexAutoRetriever,
)
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.schema import TextNode
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.types import VectorStoreInfo


class ChromaAutoretrievalPack(BaseLlamaPack):
    """Chroma auto-retrieval pack."""

    def __init__(
        self,
        collection_name: str,
        vector_store_info: VectorStoreInfo,
        nodes: List[TextNode],
        client: Optional[Any] = None,
    ) -> None:
        """Init params."""
        import chromadb

        chroma_client = client or chromadb.EphemeralClient()
        chroma_collection = chroma_client.create_collection(collection_name)

        self._vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self._storage_context = StorageContext.from_defaults(
            vector_store=self._vector_store
        )
        self._index = VectorStoreIndex(nodes, storage_context=self._storage_context)
        self._retriever = VectorIndexAutoRetriever(
            self._index, vector_store_info=vector_store_info
        )
        self._query_engine = RetrieverQueryEngine(self._retriever)

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "vector_store": self._vector_store,
            "storage_context": self._storage_context,
            "index": self._index,
            "retriever": self._retriever,
            "query_engine": self._query_engine,
        }

    def retrieve(self, query_str: str) -> Any:
        """Retrieve."""
        return self._retriever.retrieve(query_str)

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self._query_engine.query(*args, **kwargs)
