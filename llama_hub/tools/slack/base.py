"""Slack tool spec."""

import logging
from datetime import datetime
from ssl import SSLContext
from typing import List, Optional, Type

from llama_index.readers.schema.base import Document
from llama_index.readers.slack import SlackReader
from llama_index.tools.tool_spec.base import BaseToolSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DataLoaderOutput(BaseModel):
    result: List[Document]


class MessageSenderOutput(BaseModel):
    # TODO: Once we have a Pydantic definition for `slack_sdk.web.SlackResponse`, we can make this more useful.
    # Today, if we add `slack_response: SlackResponse` here, it will give RuntimeError:
    # no validator found for <class 'slack_sdk.web.slack_response.SlackResponse'>, see `arbitrary_types_allowed` in Config
    pass


class ChannelFetcherOutput(BaseModel):
    channels: List[str]


class SlackToolSpec(BaseToolSpec):
    """Slack tool spec."""

    spec_functions = ["load_data", "send_message", "fetch_channels"]
    fn_schema_map = {
        "load_data": DataLoaderOutput,
        "send_message": MessageSenderOutput,
        "fetch_channels": ChannelFetcherOutput,
    }

    def __init__(
        self,
        slack_token: Optional[str] = None,
        ssl: Optional[SSLContext] = None,
        earliest_date: Optional[datetime] = None,
        latest_date: Optional[datetime] = None,
    ) -> None:
        """Initialize with parameters."""
        self.reader = SlackReader(
            slack_token=slack_token,
            ssl=ssl,
            earliest_date=earliest_date,
            latest_date=latest_date,
        )

    def get_fn_schema_from_fn_name(self, fn_name: str) -> Type[BaseModel]:
        """Returns the schema of the output for the given function, specified by name."""
        return self.fn_schema_map.get(fn_name)

    def load_data(
        self,
        channel_ids: List[str],
        reverse_chronological: bool = True,
    ) -> DataLoaderOutput:
        """Load data from the input directory."""
        result = self.reader.load_data(
            channel_ids=channel_ids,
            reverse_chronological=reverse_chronological,
        )
        return DataLoaderOutput(result=result)

    def send_message(
        self,
        channel_id: str,
        message: str,
    ) -> MessageSenderOutput:
        """Send a message to a channel given the channel ID."""
        slack_client = self.reader.client
        try:
            # TODO: Consider adding the result into `MessageSenderOutput`.
            slack_client.chat_postMessage(
                channel=channel_id,
                text=message,
            )
        except Exception as e:
            logger.error(e)
            raise e
        return MessageSenderOutput()

    def fetch_channels(
        self,
    ) -> ChannelFetcherOutput:
        """Fetch a list of relevant channels."""
        slack_client = self.reader.client
        try:
            msg_result = slack_client.conversations_list()
            logger.info(msg_result)
        except Exception as e:
            logger.error(e)
            raise e

        return ChannelFetcherOutput(channels=msg_result["channels"])
