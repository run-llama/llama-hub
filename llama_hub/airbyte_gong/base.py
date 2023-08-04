from typing import Any, Mapping
from llama_hub.airbyte_cdk.base import AirbyteCDKReader


class AirbyteGongReader(AirbyteCDKReader):
    """AirbyteGongReader reader.

    Retrieve documents from Gong 

    Args:
        config: The config object for the gong source.
    """

    def __init__(
        self,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""
        import source_gong

        super().__init__(source_class=source_gong.SourceGong, config=config)