from typing import Any, Mapping
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
