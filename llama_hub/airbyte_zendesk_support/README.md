# Airbyte ZendeskSupport Loader

The Airbyte ZendeskSupport Loader allows you to access different ZendeskSupport objects.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install the zendesk_support source: `pip install source_zendesk_support`

## Usage

Here's an example usage of the AirbyteZendeskSupportReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_zendesk_support.base import AirbyteZendeskSupportReader

zendesk_support_config = {
    # ...
}
reader = AirbyteZendeskSupportReader(config=zendesk_support_config)
documents = reader.load_data(stream_name="tickets")
```

## Configuration

Check out the [Airbyte documentation page](https://docs.airbyte.com/integrations/sources/zendesk-support/) for details about how to configure the reader.
The JSON schema the config object should adhere to can be found on Github: [https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-zendesk-support/source_zendesk_support/spec.json](https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-zendesk-support/source_zendesk_support/spec.json).

The general shape looks like this:
```python
{
  "subdomain": "<your zendesk subdomain>",
  "start_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>",
  "credentials": {
    "credentials": "api_token",
    "email": "<your email>",
    "api_token": "<your api token>"
  }
}
```

By default all fields are stored as metadata in the documents and the text is set to an empty string. Construct the text of the document by transforming the documents returned by the reader.

## Incremental loads

This loader supports loading data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteZendeskSupportReader(...so many things...)
documents = reader.load_data(stream_name="tickets")
current_state = reader.last_state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream_name="tickets", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
