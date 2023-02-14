"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Any, Optional

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class JapanesePDFReader(BaseReader):
    """Japanese PDF reader.

    Extract text from PDF including shift-jis encoded characters using pdfminer.six.

    Args:
        concat_pages (bool): whether to concatenate all pages into one document.
            If set to False, a Document will be created for each page.
            True by default.
    """

    def __init__(
        self,
        *args: Any,
        concat_pages: bool = True,
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._concat_pages = concat_pages

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import pdfminer.high_level

        # get pdf page object
        pages = pdfminer.high_level.extract_pages(file)

        text_list = []
        for page in pages:
            # get page text
            text = "".join([obj.get_text() for obj in page if hasattr(obj, "get_text")])
            text_list.append(text)

        if self._concat_pages:
            return [Document("\n".join(text_list), extra_info=extra_info)]
        else:
            return [Document(text, extra_info=extra_info) for text in text_list]



