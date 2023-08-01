# Airbyte Salesforce Loader

The Airbyte Salesforce Loader allows you to access different Salesforce objects.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install the salesforce source: `pip install source_salesforce`

## Usage

Here's an example usage of the AirbyteSalesforceReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_salesforce.base import AirbyteSalesforceReader

salesforce_config = {
    # ...
}
reader = AirbyteSalesforceReader(config=salesforce_config)
documents = reader.load_data(stream_name="asset")
```

## Configuration

Check out the [Airbyte documentation page](https://docs.airbyte.com/integrations/sources/salesforce/) for details about how to configure the reader.
The JSON schema the config object should adhere to can be found on Github: [https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-salesforce/source_salesforce/spec.yaml](https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-salesforce/source_salesforce/spec.yaml).

The general shape looks like this:
```python
{
  "client_id": "<oauth client id>",
  "client_secret": "<oauth client secret>",
  "refresh_token": "<oauth refresh token>",
  "start_date": "<date from which to start retrieving records from in ISO format, e.g. 2020-10-20T00:00:00Z>",
  "is_sandbox": False, # set to True if you're using a sandbox environment
  "streams_criteria": [ # Array of filters for salesforce objects that should be loadable
    {"criteria": "exacts", "value": "Account"}, # Exact name of salesforce object
    {"criteria": "starts with", "value": "Asset"}, # Prefix of the name
    # Other allowed criteria: ends with, contains, starts not with, ends not with, not contains, not exacts
  ],
}
```

## Incremental loads

This loader supports loading data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteSalesforceReader(...so many things...)
documents = reader.load_data(stream_name="asset")
current_state = reader.last_state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream_name="asset", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
