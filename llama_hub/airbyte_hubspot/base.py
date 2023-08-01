"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteHubspotReader(AirbyteCDKReader):
    """AirbyteHubspotReader reader.

    Retrieve documents from Hubspot

    Args:
        config: The config object for the hubspot source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import source_hubspot

        super().__init__(source_class=source_hubspot.SourceHubspot, config=config)
