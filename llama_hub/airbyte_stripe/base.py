"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteStripeReader(AirbyteCDKReader):
    """AirbyteStripeReader reader.

    Retrieve documents from Stripe 

    Args:
        config: The config object for the stripe source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import source_stripe

        super().__init__(source_class=source_stripe.SourceStripe, config=config)
