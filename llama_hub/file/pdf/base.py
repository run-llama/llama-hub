"""Read PDF files."""

from pathlib import Path
from typing import IO, Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PDFReader(BaseReader):
    """PDF reader."""

    def load_data(
        self, file: Union[IO[bytes], str, Path], extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import pypdf

        # Check if the file is already a Path object, if not, create a Path object from the string
        if not isinstance(file, Path) and isinstance(file, str):
            file = Path(file)

        # Open the file if it's not already open, else use it as it is
        if isinstance(file, Path):
            context = open(file, "rb")
            if extra_info:
                extra_info.update({"file_name": file.name})
            else:
                extra_info = {"file_name": file.name}
        else:
            context = file

        with context as fp:
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
                metadata = {"page_label": page_label}

                if extra_info is not None:
                    metadata.update(extra_info)

                docs.append(Document(text=page_text, extra_info=metadata))
            return docs
