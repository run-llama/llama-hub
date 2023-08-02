from typing import Any, Mapping
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
        import source_zendesk_support

        super().__init__(source_class=source_zendesk_support.SourceZendeskSupport, config=config)
