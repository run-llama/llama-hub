""""Read PDF files using pdfplumber"""
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class PDFPlumberReader(BaseReader):
    """PDF parser."""

    def load_data(self, file: str, extra_info: Optional[Dict] = None) -> List[Document]:
        """Parse file."""

        docs = []

        try:
            import pdfplumber
        except ImportError:
            raise ImportError(
                "pdfplumber is required to read PDF files: `pip install pdfplumber`"
            )
        with pdfplumber.open(file) as fp:
            text_list = [page.extract_text() for page in fp.pages]
            text = "\n".join(text_list)
            metadata = {"file_path": fp.stream.name}

            if extra_info is not None:
                metadata.update(extra_info)

            docs.append(Document(text=text, metadata=metadata))
            fp.close()

        return docs
