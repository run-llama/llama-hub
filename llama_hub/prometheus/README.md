# Prometheus Loader

This loader loads metrics from Prometheus. The user specifies a Prometheus instance to initialize the reader. They then specify the query, the date range, steps, Http parameters and which fields must be used as metadata. Also can be added additional metadata to the values using the parameter additional_metadata.

Automatically adds to the metadata the timestamp value and create a document per value returned by the prometheus query.

## Usage

Here's an example usage of the PrometheusReader.

```python
from llama_index import download_loader
import os

PrometheusReader = download_loader('PrometheusReader')

endpoint = "<endpoint>"
size = "<size>"
# query_dict is passed into db.collection.find()
query = ""
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)
metadata_fields = ['id', "host"]
additional_metadata = {
    "collection_date": datetime.now().isoformat(),
}
reader = PrometheusReader(endpoint, size)
documents = reader.load_data(query=query, 
                             start_time=start_time,
                             end_time=end_time,
                             step="1m",
                             get_pararameters=None,
                             metadata_fields=metadata_fields,
                             additional_metadata=additional_metadata)
```
