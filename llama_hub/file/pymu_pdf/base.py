"""Read PDF files using PyMuPDF library."""
from pathlib import Path
from typing import Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class PyMuPDFReader(BaseReader):
    """Read PDF files using PyMuPDF library."""

    def load(
        self,
        file_path: Union[Path, str],
        include_metadata: bool = True,
        metadata: Optional[Dict] = None,
    ) -> List[Document]:
        """Loads list of documents from PDF file and also accepts extra information in dict format.

        Args:
            file_path (Union[Path, str]): file path of PDF file (accepts string or Path).
            include_metadata (bool, optional): if metadata to be included or not. Defaults to True.
            metadata (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

        Raises:
            TypeError: if metadata is not a dictionary.
            TypeError: if file_path is not a string or Path.

        Returns:
            List[Document]: list of documents.
        """
        import fitz

        # check if file_path is a string or Path
        if not isinstance(file_path, str) and not isinstance(file_path, Path):
            raise TypeError("file_path must be a string or Path.")

        # open PDF file
        doc = fitz.open(file_path)

        # if metadata is not None, check if it is a dictionary
        if metadata:
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be a dictionary.")

        # if metadata is True, add metadata to each document
        if include_metadata:
            if not metadata:
                metadata = {}
            metadata["total_pages"] = len(doc)
            metadata["file_path"] = file_path

            # return list of documents
            return [
                Document(
                    text=page.get_text().encode("utf-8"),
                    metadata=dict(
                        metadata,
                        **{
                            "source": f"{page.number+1}",
                        },
                    ),
                )
                for page in doc
            ]

        else:
            return [
                Document(text=page.get_text().encode("utf-8"), metadata=metadata)
                for page in doc
            ]
