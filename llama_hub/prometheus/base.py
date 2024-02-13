from typing import List, Optional, Any
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


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

    def load_data(self, query: str, **load_kwargs: Any) -> List[Document]:
        """Load metrics data from prometheus

        Args:
            query (str): Prometheus Query Language (PromQL) string
            start_time (Optional[datetime], optional): Start time of the query. Defaults to None.
            end_time (Optional[datetime], optional): End time of the query. Defaults to None.
            step (Optional[str], optional): Step of the query. Defaults to None.
            get_pararameters (Optional[dict], optional): Additional parameters to pass to the query. Defaults to None.
            metadata_fields (Optional[list], optional): List of metadata fields to include in the response. Defaults to None.
            additional_metadata (Optional[dict], optional): Additional metadata to include in the response. Defaults to None.
        """
        start_time = load_kwargs.get("start_time", None)
        end_time = load_kwargs.get("end_time", None)
        step = load_kwargs.get("step", None)
        get_pararameters = load_kwargs.get("get_pararameters", None)
        metadata_fields = load_kwargs.get("metadata_fields", dict())
        additional_metadata = load_kwargs.get("additional_metadata", dict())
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
