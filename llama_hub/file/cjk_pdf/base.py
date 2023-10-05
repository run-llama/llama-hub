"""Read PDF files."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class CJKPDFReader(BaseReader):
    """CJK PDF reader.

    Extract text from PDF including CJK (Chinese, Japanese and Korean) languages using pdfminer.six.

    Args:
        concat_pages (bool): whether to concatenate all pages into one document.
            If set to False, a Document will be created for each page.
            True by default.
    """

    def __init__(self, *args: Any, concat_pages: bool = True, **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._concat_pages = concat_pages

    # Define a function to extract text from PDF
    def _extract_text_by_page(self, pdf_path: Path) -> List[str]:
        # Import pdfminer
        from io import StringIO

        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
        from pdfminer.pdfpage import PDFPage

        # Create a resource manager
        rsrcmgr = PDFResourceManager()
        # Create an object to store the text
        retstr = StringIO()
        # Create a text converter
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # Create a PDF interpreter
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Open the PDF file
        fp = open(pdf_path, "rb")
        # Create a list to store the text of each page
        text_list = []
        # Extract text from each page
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            # Get the text
            text = retstr.getvalue()
            # Add the text to the list
            text_list.append(text)
            # Clear the text
            retstr.truncate(0)
            retstr.seek(0)
        # Close the file
        fp.close()
        # Close the device
        device.close()
        # Return the text list
        return text_list

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""

        text_list = self._extract_text_by_page(file)

        if self._concat_pages:
            return [Document(text="\n".join(text_list), extra_info=extra_info or {})]
        else:
            return [
                Document(text=text, extra_info=extra_info or {}) for text in text_list
            ]
