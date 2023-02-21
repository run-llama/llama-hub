"""Simple Reader for Memos"""

from typing import List, Optional, Any

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class MemosReader(BaseReader):
    """Memos reader.

    Reads content from an Memos.

    """

    def __init__(self, host: str = "https://demo.usememos.com/") -> None:
        """Init params."""
        
        self._memoUrl = host + "api/memo"

    def load_data(self, params: Optional[Any] = 101) -> List[Document]:
        """Load data from RSS feeds.

        Args:
            params (Any): Filtering parameters.

        Returns:
            List[Document]: List of documents.

        """
        import requests
        
        documents = []

        realUrl = self._memoUrl
        if ~params:
            params = {}
            realUrl += "/all"

        req = requests.get(realUrl, params)
        
        if ~req.ok:
            return documents
        
        res = req.json()
        
        memos = res["data"]
        
        for memo in memos:
            content = memo["content"]
            extra_info = {"creator": memo["creator"], "resource_list": memo["resourceList"], id: memo["id"]}
            documents.append(Document(content, extra_info=extra_info))

        return documents
