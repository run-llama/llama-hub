from typing import Any, Mapping
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
        import source_typeform

        super().__init__(source_class=source_typeform.SourceTypeform, config=config)