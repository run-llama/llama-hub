# Opsgenie Reader

The Opsgenie loader returns all open alerts from Opsgenie.

## Usage

Here's an example of how to use it

```python

from llama_hub.opsgenie import OpsgenieReader

reader = OpsgenieReader(api_key=api_key, api_url=api_url)
documents = reader.load_data()

```

Alternately, you can also use download_loader from llama_index

```python

from llama_index import download_loader
OpsgenieReader = download_loader('OpsgenieReader')

reader = OpsgenieReader(api_key=api_key, api_url=api_url)
documents = reader.load_data()

```

