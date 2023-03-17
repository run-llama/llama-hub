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

    def _get_stream_name(self, stream_id: str) -> str:
        """Retrieve the stream name given a stream ID."""
        streams_data = self.client.get_streams()["streams"]
        stream_name = None
        for stream in streams_data:
            if str(stream["stream_id"]) == stream_id:
                stream_name = stream["name"]
                break
        if stream_name is None:
            raise ValueError(f"Stream with ID {stream_id} not found.")

        return stream_name

    def _read_stream(self, stream_id: str, reverse_chronological: bool) -> str:
        """Read a stream."""
        # Read stream logic here
        stream_name = self._get_stream_name(stream_id)

        params = {
            "narrow": [{"operator": "stream", "operand": stream_name}],
            "anchor": "newest",
            "num_before": 100,
            "num_after": 0,
        }
        response = self.client.get_messages(params)
        messages = response["messages"]
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
