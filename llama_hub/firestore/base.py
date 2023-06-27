"""Firestore Reader."""

from typing import Any, List, Optional
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class FirestoreReader(BaseReader):
    """Simple Firestore reader.

    Args:
        project_id (str): The Google Cloud Project ID.
        *args (Optional[Any]): Additional arguments.
        **kwargs (Optional[Any]): Additional keyword arguments.

    Returns:
        FirestoreReader: A FirestoreReader object.
    """

    def __init__(
        self,
        project_id: str,
        *args: Optional[Any],
        **kwargs: Optional[Any],
    ) -> None:
        """Initialize with parameters."""
        from google.cloud import firestore

        self.db = firestore.Client(project=project_id)

    def load_data(self, collection: str) -> List[Document]:
        """Load data from a Firestore collection, returning a list of Documents.

        Args:
            collection (str): The name of the Firestore collection to read from.

        Returns:
            List[Document]: A list of Document objects.
        """
        documents = []
        col_ref = self.db.collection(collection)
        for doc in col_ref.stream():
            doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
            documents.append(Document(text=doc_str))
        return documents

    def load_document(self, document_url: str) -> Document:
        """Load a single document from Firestore.

        Args:
            document_url (str): The absolute path to the Firestore document to read.

        Returns:
            Document: A Document object.
        """
        parts = document_url.split("/")
        if len(parts) % 2 != 0:
            raise ValueError(f"Invalid document URL: {document_url}")

        ref = self.db.collection(parts[0])
        for i in range(1, len(parts)):
            if i % 2 == 0:
                ref = ref.collection(parts[i])
            else:
                ref = ref.document(parts[i])

        doc = ref.get()
        if not doc.exists:
            raise ValueError(f"No such document: {document_url}")
        doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
        return Document(text=doc_str)
