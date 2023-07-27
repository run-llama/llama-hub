"""Chroma Reader."""

import logging
from typing import Any, Dict, List, Mapping, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class AirbyteSalesforceReader(BaseReader):
    """AirbyteSalesforceReader reader.

    Retrieve documents from Salesforce 

    Args:
        config: The config object for the 
        persist_directory: Directory where the collection is persisted.

    """

    def __init__(
        self,
        config: Mapping[str, Any],
        state: Optional[Any] = None,
    ) -> None:
        """Initialize with parameters."""
        import source_salesforce

        self._logger = logging.getLogger(__name__)
        self._source = source_salesforce.SourceSalesforce()
        self._config = config
        self._last_state = state

        self._catalog = self._source.discover(self._logger, self._config)

    def load_data(
        self,
        stream_name: str,
        limit: int = 10,
    ) -> List[Document]:
        from airbyte_protocol.models.airbyte_protocol import ConfiguredAirbyteCatalog, ConfiguredAirbyteStream, SyncMode, DestinationSyncMode, Type, AirbyteStateMessage
        streams_by_name = {stream.name: stream for stream in self._catalog.streams}
        current_stream = streams_by_name[stream_name]

        configured_catalog = ConfiguredAirbyteCatalog(streams = [
            ConfiguredAirbyteStream(
                stream=current_stream,
                sync_mode=SyncMode.incremental,
                destination_sync_mode=DestinationSyncMode.append
            )]
        ) 
        iterator = self._source.read(self._logger, self._config, configured_catalog, state=[self._last_state] if self._last_state else None)
        documents: List[Document] = []
        for message in iterator:
            if message.type is Type.RECORD:
                data = message.record.data
                documents.append(Document(doc_id=self._get_defined_id(current_stream, data),text="", extra_info=data))
            if message.type is Type.STATE:
                self._last_state = message.state
            if len(documents) >= limit:
                break
        
        return documents
    
    @property
    def state(self) -> Optional[Any]:
        return self._last_state
    
    def _get_defined_id(self, stream: Any, data: Dict[str, Any]) -> Optional[str]:
        import dpath

        if not stream.source_defined_primary_key:
            return None
        primary_key = []
        for key in stream.source_defined_primary_key:
            try:
                primary_key.append(str(dpath.util.get(data, key)))
            except KeyError:
                primary_key.append("__not_found__")
        return "_".join(primary_key)
