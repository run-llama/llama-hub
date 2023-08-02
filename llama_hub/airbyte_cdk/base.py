from typing import Any, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from airbyte_protocol.models.airbyte_protocol import AirbyteRecordMessage
from airbyte_cdk.sources.embedded.base_integration import BaseEmbeddedIntegration
from airbyte_cdk.sources.embedded.runner import CDKRunner


class AirbyteCDKReader(BaseReader, BaseEmbeddedIntegration):
    """AirbyteCDKReader reader.

    Retrieve documents from an Airbyte source implemented using the CDK.

    Args:
        source_class: The Airbyte source class.
        config: The config object for the Airbyte source.
    """

    def __init__(
        self,
        source_class: Any,
        config: Mapping[str, Any],
    ) -> None:
        """Initialize with parameters."""

        super().__init__(config=config, runner=CDKRunner(source=source_class(), name=source_class.__name__))
    
    def _handle_record(self, record: AirbyteRecordMessage, id: Optional[str]) -> Document:
        return Document(doc_id=id,text="", extra_info=record.data)

    def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
        return list(self._load_data(*args, **load_kwargs))