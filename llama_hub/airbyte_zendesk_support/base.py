"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteZendeskSupportReader(AirbyteCDKReader):
    """AirbyteZendeskSupportReader reader.

    Retrieve documents from ZendeskSupport 

    Args:
        config: The config object for the zendesk_support source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import airbyte_source_zendesk_support

        super().__init__(source_class=airbyte_source_zendesk_support.SourceZendeskSupport, config=config)
