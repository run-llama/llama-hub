# Airbyte Typeform Loader

The Airbyte Typeform Loader allows you to access different Typeform objects.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install the typeform source: `pip install source_typeform`

## Usage

Here's an example usage of the AirbyteTypeformReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_typeform.base import AirbyteTypeformReader

typeform_config = {
    # ...
}
reader = AirbyteTypeformReader(config=typeform_config)
documents = reader.load_data(stream_name="forms")
```

## Configuration

Check out the [Airbyte documentation page](https://docs.airbyte.com/integrations/sources/typeform/) for details about how to configure the reader.
The JSON schema the config object should adhere to can be found on Github: [https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-typeform/source_typeform/spec.json](https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-typeform/source_typeform/spec.json).

The general shape looks like this:
```python
{
  "credentials": {
    "auth_type": "Private Token",
    "access_token": "<your auth token>"
  },
  "start_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>",
  "form_ids": ["<id of form to load records for>"] # if omitted, records from all forms will be loaded
}
```

## Incremental loads

This loader supports loading data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteTypeformReader(...so many things...)
documents = reader.load_data(stream_name="forms")
current_state = reader.last_state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream_name="forms", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
