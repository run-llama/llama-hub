"""Read Microsoft Word files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class DocxReader(BaseReader):
    """Docx Reader."""

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import docx2txt

        text = docx2txt.process(file)

        return [Document(text, extra_info=extra_info)]
