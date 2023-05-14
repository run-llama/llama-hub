"""Reader that pulls in a BoardDocs site."""
from typing import Any, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class BoardDocsReader(BaseReader):
    """BoardDocs doc reader.

    Read public agendas included on a BoardDocs site.

    Args:
      None
    """

    def __init__(
        self,
    ) -> None:
        """Initialize with parameters."""
        super().__init__()

    def load_data(
        self, site: str, **load_kwargs: Any
    ) -> List[Document]:
        """Load BoardDoc site data.

        Args:
            site (str): The BoardDocs site you'd like to index.

        """

        results = []
        results.append(Document("Test BoardDoc Document"))
        return results