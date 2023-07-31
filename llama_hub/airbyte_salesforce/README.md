# Airbyte Salesforce Loader

The Airbyte Salesforce Loader allows you to access different Salesforce objects.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install the salesforce source: `pip install airbyte_source_salesforce`

## Usage

Here's an example usage of the AirbyteSalesforceReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_salesforce.base import AirbyteSalesforceReader

salesforce_config = {
    # ...
}
reader = AirbyteSalesforceReader(config=salesforce_config)
documents = reader.load_data(stream="Asset")
```

## Incremental loads

This loader supports loading data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteSalesforceReader(...so many things...)
documents = reader.load_data(stream="Asset")
current_state = reader.state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream="Asset", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
