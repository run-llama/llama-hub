"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PDFReader(BaseReader):
    """PDF reader."""

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import pypdf

        text_list = []
        with open(file, "rb") as fp:
            # Create a PDF object
            pdf = pypdf.PdfReader(fp)

            # Get the number of pages in the PDF document
            num_pages = len(pdf.pages)

            # Iterate over every page
            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                text_list.append(page_text)
                page_label = pdf.page_labels[page]
                metadata = {"page_label": page_label, "file_name":file.name}
                if extra_info is not None:
                    metadata.update(extra_info)
                
        text = "\n".join(text_list)

        return [Document(text, extra_info=extra_info)]
