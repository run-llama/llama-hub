"""Read PDF files using PyMuPDF library."""
from pathlib import Path
from typing import Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PyMuPDFReader(BaseReader):
    """Read PDF files using PyMuPDF library."""

    def __init__(self, file_path: Union[Path, str], metadata: bool = True) -> None:
        """Initializes PyMuPDFReader.

        Args:
            file_path (Union[Path, str]): file path of PDF file (accepts string or Path)
            metadata (bool, optional): if metadata to be included or not. Defaults to True.
        """
        super().__init__(file_path)
        self._metadata = metadata

    def load(self, extra_info: Optional[Dict] = None) -> List[Document]:
        """Loads list of documents from PDF file and also accepts extra information in dict format.

        Args:
            extra_info (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

        Raises:
            TypeError: if extra_info is not a dictionary.

        Returns:
            List[Document]: list of documents.
        """
        import fitz
        
        # open PDF file
        doc = fitz.open(self.file_path)

        # if extra_info is not None, check if it is a dictionary
        if extra_info:
            if not isinstance(extra_info, dict):
                raise TypeError("Extra_info must be a dictionary.")

        # if metadata is True, add metadata to each document
        if self._metadata:
            metadata_dict = {}
            metadata_dict["total_pages"] = len(doc)
            metadata_dict["file_path"] = self.file_path

            # add extra_info to metadata_dict
            if not extra_info:
                extra_info = metadata_dict
            else:
                extra_info = dict(extra_info, **metadata_dict)

            # return list of documents
            return [
                Document(
                    page_content=page.get_text().encode("utf-8"),
                    extra_info=dict(
                        extra_info,
                        **{
                            metadata_dict["source"]: f"{page.number+1}",
                        },
                    ),
                )
                for page in doc
            ]

        else:
            return [
                Document(
                    page_content=page.get_text().encode("utf-8"), extra_info=extra_info
                )
                for page in doc
            ]
