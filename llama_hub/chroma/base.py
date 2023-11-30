"""Chroma Reader."""

from typing import Any, Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class ChromaReader(BaseReader):
    """Chroma reader.

    Retrieve documents from existing persisted Chroma collections.

    Args:
        collection_name: Name of the peristed collection.
        persist_directory: Directory where the collection is persisted.

    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: Optional[str] = None,
        client: Optional[Any] = None,
    ) -> None:
        """Initialize with parameters."""
        import chromadb  # noqa: F401
        from chromadb.config import Settings

        if (collection_name is None) or (persist_directory is None and client is None):
            raise ValueError(
                "Please provide a collection name and persist directory or Chroma client."
            )
        if client is not None:
            self._client = client
        else:
            self._client = chromadb.Client(
                Settings(is_persistent=True, persist_directory=persist_directory)
            )
        self._collection = self._client.get_collection(collection_name)

    def load_data(
        self,
        query_vector: List[Union[List[float], List[int]]],
        limit: int = 10,
        where: Optional[Dict[Any, Any]] = None,
        where_document: Optional[Dict[Any, Any]] = None,
    ) -> Any:
        """Load data from Chroma.

        Args:
            query_vector (Any): Query
            limit (int): Number of results to return.
            where (Dict): Metadata where filter.
            where_document (Dict): Document where filter.

        Returns:
            List[Document]: A list of documents.
        """
        results = self._collection.query(
            query_embeddings=query_vector,
            include=["documents", "metadatas", "embeddings"],  # noqa: E501
            n_results=limit,
            where=where,
            where_document=where_document,
        )
        print(results)
        documents: List[Document] = []
        # early return if no results
        if results is None or len(results["ids"][0]) == 0:
            return documents
        for i in range(len(results["ids"])):
            for result in zip(
                results["ids"][i], results["documents"][i], results["embeddings"][i]
            ):
                document = Document(
                    doc_id=result[0],
                    text=result[1],
                    embedding=result[2],
                )
                documents.append(document)

        return documents
