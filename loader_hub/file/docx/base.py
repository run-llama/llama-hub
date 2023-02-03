"""Read Microsoft Word files."""

from pathlib import Path
from typing import Dict, Optional, List

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class DocxReader(BaseReader):
    """Docx Reader."""

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        try:
            import docx2txt
        except ImportError:
            raise ValueError("docx2txt is required to read Microsoft Word files.")

        text = docx2txt.process(file)

        return [Document(text, extra_info=extra_info)]
