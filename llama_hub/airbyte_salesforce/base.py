"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteSalesforceReader(AirbyteCDKReader):
    """AirbyteSalesforceReader reader.

    Retrieve documents from Salesforce 

    Args:
        config: The config object for the salesforce source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import source_salesforce

        super().__init__(source_class=source_salesforce.SourceSalesforce, config=config)
