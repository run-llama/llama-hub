"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteTypeformReader(AirbyteCDKReader):
    """AirbyteTypeformReader reader.

    Retrieve documents from Typeform 

    Args:
        config: The config object for the typeform source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import airbyte_source_typeform

        super().__init__(source_class=airbyte_source_typeform.SourceTypeform, config=config)
