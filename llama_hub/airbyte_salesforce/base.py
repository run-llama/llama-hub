from typing import Any, Mapping
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
