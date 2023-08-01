# Airbyte Shopify Loader

The Airbyte Shopify Loader allows you to access different Shopify objects.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install the shopify source: `pip install airbyte_source_shopify`

## Usage

Here's an example usage of the AirbyteShopifyReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_shopify.base import AirbyteShopifyReader

shopify_config = {
    # ...
}
reader = AirbyteShopifyReader(config=shopify_config)
documents = reader.load_data(stream="Asset")
```

## Configuration

Check out the [Airbyte documentation page](https://docs.airbyte.com/integrations/sources/shopify/) for details about how to configure the reader.
The JSON schema the config object should adhere to can be found on Github: [https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-shopify/source_shopify/spec.json](https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-shopify/source_shopify/spec.json).

The general shape looks like this:
```python
{
    "start_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>",
    "shop": "<name of the shop you want to retrieve documents from>",
    "credentials": {
        "auth_method": "api_password",
        "api_password": "<your api password>"
    }
}
```

## Incremental loads

This loader supports loading data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteShopifyReader(...so many things...)
documents = reader.load_data(stream="Orders")
current_state = reader.last_state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream="Orders", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
