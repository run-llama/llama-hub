from typing import List, Optional
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from datetime import datetime


class PrometheusReader(BaseReader):
    def __init__(self, endpoint: str, size: Optional[int] = 100):
        try:
            from prometheus_api_client import PrometheusConnect
        except ImportError as err:
            raise ImportError(
                "`prometheus-api-client` package not found, please run `pip install prometheus-api-client`"
            ) from err

        self.prometheus_url = endpoint
        self.prom_client = PrometheusConnect(url=self.prometheus_url)

    def load_data(
        self,
        query: str,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        step: Optional[str],
        get_pararameters: Optional[dict],
        metadata_fields: Optional[list] = [],
        additional_metadata: Optional[dict] = {},
    ) -> List[Document]:

        # Verify if the start_time and end_time is present, to define if is a range query
        if start_time is not None and end_time is not None:
            params = {
                "query": query,
                "start_time": start_time,
                "end_time": end_time,
            }
            if step is not None:
                params["step"] = step
            else:
                params["step"] = "1m"
            if get_pararameters is not None:
                params["params"] = get_pararameters
            result = self.prom_client.custom_query_range(**params)
        else:
            params = {
                "query": query,
            }
            if get_pararameters is not None:
                params["params"] = get_pararameters
            result = self.prom_client.custom_query(**params)

        documents = []
        for row in result:
            metadata = dict()
            # extract the fields identified as metadata for the document
            for key_value in row["metric"]:
                if key_value in metadata_fields:
                    metadata[key_value] = row["metric"][key_value]
            for value in row["values"]:
                # merge the current metadata fields with additional fixed metadata
                current_metadata = metadata | additional_metadata
                current_metadata["timestamp"] = value[0]
                documents.append(
                    Document(text=value[1], extra_info=current_metadata, embedding=None)
                )
        return documents
