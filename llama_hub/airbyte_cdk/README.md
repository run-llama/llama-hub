# Airbyte CDK Loader

The Airbyte CDK Loader is a shim for sources created using the [Airbyte Python CDK](https://docs.airbyte.com/connector-development/cdk-python/). It allows you to load data from any Airbyte source into LlamaIndex.

## Installation

* Install llama_hub: `pip install llama_hub`
* Install airbyte-cdk: `pip install airbyte-cdk`
* Install a source via git (or implement your own): `pip install git+https://github.com/airbytehq/airbyte.git@master#egg=source_github&subdirectory=airbyte-integrations/connectors/source-github`

## Usage

Here's an example usage of the AirbyteCdkReader.

```python
from llama_index import download_loader
from llama_hub.airbyte_cdk.base import AirbyteCDKReader
from source_github.source import SourceGithub


github_config = {
    # ...
}
reader = AirbyteCDKReader(source_class=SourceGithub,config=github_config)
documents = reader.load_data(stream_name="issues")
```

By default all fields are stored as metadata in the documents and the text is set to an empty string. Construct the text of the document by transforming the documents returned by the reader:
```python
for doc in documents:
  doc.text = doc.extra_info["title"]
```

## Incremental loads

If a stream supports it, this loader can be used to load data incrementally (only returning documents that weren't loaded last time or got updated in the meantime):
```python

reader = AirbyteCDKReader(source_class=SourceGithub,config=github_config)
documents = reader.load_data(stream_name="issues")
current_state = reader.last_state # can be pickled away or stored otherwise

updated_documents = reader.load_data(stream_name="issues", state=current_state) # only loads documents that were updated since last time
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
