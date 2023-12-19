"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class PDFReader(BaseReader):
    """PDF parser."""

    def __init__(
        self,
        return_full_document: Optional[bool] = False,
        use_pdfplumber: Optional[bool] = False,
    ) -> None:
        """
        Initialize PDFReader.
        """
        self.return_full_document = return_full_document
        self.use_pdfplumber = use_pdfplumber

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""

        docs = []

        if self.use_pdfplumber:
            # TODO
            try:
                import pdfplumber
            except ImportError:
                raise ImportError(
                    "pdfplumber is required to read PDF files: `pip install pdfplumber`"
                )
            with pdfplumber.open(file) as fp:
                text_list = [page.extract_text() for page in fp.pages]
                text = "\n".join(text_list)
                metadata = {"file_name": fp.stream.name.split("/")[-1]}

                docs.append(Document(text=text, metadata=metadata))
                fp.close()

        else:
            try:
                import pypdf
            except ImportError:
                raise ImportError(
                    "pypdf is required to read PDF files: `pip install pypdf`"
                )
            with open(file, "rb") as fp:
                # Create a PDF object
                pdf = pypdf.PdfReader(fp)

                # Get the number of pages in the PDF document
                num_pages = len(pdf.pages)

                # This block returns a whole PDF as a single Document
                if self.return_full_document:
                    text = ""
                    metadata = {"file_name": fp.name}

                    for page in range(num_pages):
                        # Extract the text from the page
                        page_text = pdf.pages[page].extract_text()
                        text += page_text

                    docs.append(Document(text=text, metadata=metadata))

                # This block returns each page of a PDF as its own Document
                else:
                    # Iterate over every page

                    for page in range(num_pages):
                        # Extract the text from the page
                        page_text = pdf.pages[page].extract_text()
                        page_label = pdf.page_labels[page]

                        metadata = {"page_label": page_label, "file_name": fp.name}
                        if extra_info is not None:
                            metadata.update(extra_info)

                        docs.append(Document(text=page_text, metadata=metadata))

        return docs
