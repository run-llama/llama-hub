import logging
from typing import List, Optional
from datetime import datetime

import zulip
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

class ZulipReader(BaseReader):
    """Zulip reader."""

    def __init__(
        self,
        zulip_token: Optional[str] = None,
        zulip_email: Optional[str] = None,
        zulip_domain: Optional[str] = None,
        earliest_date: Optional[datetime] = None,
        latest_date: Optional[datetime] = None,
    ) -> None:
        """Initialize with parameters."""
        # Initialize Zulip client here with provided parameters
        self.client = zulip.Client(api_key=zulip_token, email=zulip_email, site=zulip_domain)

    def _read_message(self, stream_id: str, message_id: str) -> str:
        """Read a message."""
        # Read message logic here
        message = self.client.get_message(message_id)
        return message["content"]

    def _read_stream(self, stream_id: str, reverse_chronological: bool) -> str:
        """Read a stream."""
        # Read stream logic here
        messages = self.client.get_messages({"stream_id": stream_id, "num_before": 100})
        if reverse_chronological:
            messages.reverse()
        return " ".join([message["content"] for message in messages])

    def load_data(
        self, stream_ids: List[str], reverse_chronological: bool = True
    ) -> List[Document]:
        """Load data from the input streams."""
        # Load data logic here
        data = []
        for stream_id in stream_ids:
            stream_content = self._read_stream(stream_id, reverse_chronological)
            data.append(Document(stream_id, content=stream_content))
        return data

if __name__ == "__main__":
    reader = ZulipReader(zulip_token="your_token", zulip_email="your_email", zulip_domain="your_domain")
    logging.info(reader.load_data(stream_ids=["12345"]))
