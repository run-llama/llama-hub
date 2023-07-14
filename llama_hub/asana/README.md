# Asana Loader

This loader loads documents from Asana. The user specifies an API token to initialize the AsanaReader. They then specify a `workspace_id` or a `project_id` and the id_type as `workspace` or `project` to load in the corresponding Document objects from the corresponding object.

## Usage

Here's an example usage of the AsanaReader.

```python
from llama_index import download_loader
import os

AsanaReader = download_loader('AsanaReader')

reader = AsanaReader("<ASANA_TOKEN">)
documents = reader.load_data(id="<WORKSPACE_OR_PROJECT_ID">, id_type="<WORKSPACE_OR_PROJECT")

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
