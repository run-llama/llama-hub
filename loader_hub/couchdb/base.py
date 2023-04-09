"""CouchDB client."""

from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class SimpleCouchDBReader(BaseReader):
    """Simple CouchDB reader.

    Concatenates each CouchDB doc into Document used by LlamaIndex.

    Args:
        couchdb_url (str): CouchDB Full URL.
        max_docs (int): Maximum number of documents to load.

    """

    def __init__(self, user: str, pwd: str, host: str, port: int, couchdb_url: Optional[Dict] = None, max_docs: int = 1000) -> None:
        """Initialize with parameters."""
        import couchdb3;

        if couchdb_url is not None:
            self.client: CouchDBClient = couchdb3.Server(couchdb_url)
        else:
            self.client: CouchDBClient = couchdb3.Server(f'http://{user}:{pwd}@{host}:{port}')
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
        db = self.client.get(db_name)
        if query_dict is None:
            results = db.find()
        else:
            results = db.find(query_dict)

        #results = db.all_docs

        for doc in results['docs']:
            if "doc" not in item:
                raise ValueError("`doc` field not found in CouchDB document.")
            documents.append(Document(item))
        return documents

