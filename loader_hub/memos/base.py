"""Memos"""

from typing import List, Optional

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class MemosReader(BaseReader):
    """Memos reader.

    Reads content from an Memos.

    """

    def __init__(self, host: str = "https://demo.usememos.com/") -> None:
        """Initialize with parameters.
        """
        import requests
        
        self._memoUrl = host + "api/memo"

    def load_data(self, creator_id: Optional[int] = 101) -> List[Document]:
        """Load data from RSS feeds.

        Args:
            urls (List[str]): List of RSS URLs to load.

        Returns:
            List[Document]: List of documents.

        """

        documents = []

        realUrl = self._memoUrl
        if creator_id:
            realUrl += "?creatorId=" + creator_id + "&rowStatus=NORMAL"
        else:
            realUrl += "/all"

        req = requests.get(realUrl)
        res = req.json()
        
        memos = res["data"]
        
        for memo in memos:
            
            content = memo["content"]
            extra_info = {"creator": memo["creator"], "resource_list": memo["resourceList"], id: memo["id"]}
            documents.append(Document(content, extra_info=extra_info))

        return documents
