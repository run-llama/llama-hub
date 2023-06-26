"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class PDFReader(BaseReader):
    """PDF reader."""

    def load_data(self, file: Path, metadata: Optional[Dict] = None) -> List[Document]:
        """Parse file."""
        import pypdf

        with open(file, "rb") as fp:
            # Create a PDF object
            pdf = pypdf.PdfReader(fp)

            # Get the number of pages in the PDF document
            num_pages = len(pdf.pages)

            # Iterate over every page
            docs = []
            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                page_label = pdf.page_labels[page]
                base_metadata = {"page_label": page_label, "file_name": file.name}

                if metadata is not None:
                    base_metadata.update(metadata)

                docs.append(Document(text=page_text, extra_info=base_metadata))
            return docs
