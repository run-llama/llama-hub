"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteShopifyReader(AirbyteCDKReader):
    """AirbyteShopifyReader reader.

    Retrieve documents from Shopify 

    Args:
        config: The config object for the shopify source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import source_shopify

        super().__init__(source_class=source_shopify.SourceShopify, config=config)
