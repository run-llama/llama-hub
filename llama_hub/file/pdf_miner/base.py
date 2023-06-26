"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class PDFMinerReader(BaseReader):
    """PDF parser based on pdfminer.six."""

    def load_data(self, file: Path, metadata: Optional[Dict] = None) -> List[Document]:
        """Parse file."""
        try:
            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.pdfpage import PDFPage as PDF_Page
            from pdfminer.converter import TextConverter
            from pdfminer.layout import LAParams
            from io import StringIO

            def _extract_text_from_page(page):
                resource_manager = PDFResourceManager()
                output_string = StringIO()
                codec = "utf-8"
                laparams = LAParams()
                device = TextConverter(
                    resource_manager, output_string, codec=codec, laparams=laparams
                )
                interpreter = PDFPageInterpreter(resource_manager, device)
                interpreter.process_page(page)
                text = output_string.getvalue()
                device.close()
                output_string.close()
                return text

        except ImportError:
            raise ImportError(
                "pdfminer.six is required to read PDF files: `pip install pypdf`"
            )
        with open(file, "rb") as fp:
            reader = PDF_Page.get_pages(fp)

            # Iterate over every page
            docs = []
            for i, page in enumerate(reader):
                # Extract the text from the page
                page_text = _extract_text_from_page(page)

                base_metadata = {"page_label": i, "file_name": file.name}
                if metadata is not None:
                    base_metadata.update(metadata)

                docs.append(Document(text=page_text, extra_info=base_metadata))
            return docs
