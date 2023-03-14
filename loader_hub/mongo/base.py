"""Mongo client."""

from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class SimpleMongoReader(BaseReader):
    """Simple mongo reader.

    Concatenates each Mongo doc into Document used by LlamaIndex.

    Args:
        mongo_db_url (str): Mongo Full URL.
        max_docs (int): Maximum number of documents to load.

    """

    def __init__(self, host: str, port: int, mongo_db_url: Optional[Dict] = None, max_docs: int = 1000) -> None:
        """Initialize with parameters."""
        from pymongo import MongoClient  # noqa: F401

        if mongo_db_url is not None:
            self.client: MongoClient = MongoClient(mongo_db_url)
        else:
            self.client: MongoClient = MongoClient(host, port)
        self.max_docs = max_docs

    def load_data(
        self, db_name: str, collection_name: str, query_dict: Optional[Dict] = None
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            query_dict (Optional[Dict]): query to filter documents.
                Defaults to None

        Returns:
            List[Document]: A list of documents.

        """
        documents = []
        db = self.client[db_name]
        if query_dict is None:
            cursor = db[collection_name].find()
        else:
            cursor = db[collection_name].find(query_dict)

        for item in cursor:
            if "text" not in item:
                raise ValueError("`text` field not found in Mongo document.")
            documents.append(Document(item["text"]))
        return documents
