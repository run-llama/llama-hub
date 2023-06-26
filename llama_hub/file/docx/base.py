"""Read Microsoft Word files."""

from pathlib import Path
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class DocxReader(BaseReader):
    """Docx Reader."""

    def load_data(self, file: Path, metadata: Optional[Dict] = None) -> List[Document]:
        """Parse file."""
        import docx2txt

        text = docx2txt.process(file)
        base_metadata = {"file_name": file.name}

        if metadata is not None:
            base_metadata.update(metadata)

        return [Document(text=text, extra_info=base_metadata)]
