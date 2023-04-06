# Azure Cognitive Search Loader

The AzCognitiveSearchReader Loader returns a set of texts corresponding to documents retrieved from specific index of Azure Cognitive Search.
The user initializes the loader with credentials (service name and key) and the index name. 

## Usage

Here's an example usage of the AzCognitiveSearchReader.

```python
from llama_index import download_loader

AzCognitiveSearchReader = download_loader("AzCognitiveSearchReader")

reader = AzCognitiveSearchReader(
    "<Azure_Cognitive_Search_NAME>",
    "<Azure_Cognitive_Search_KEY>,
    "<Index_name>
)


query_sample = ""
documents = reader.load_data(
    query="<search_term>", content_field="<content_field_name>", filter="<azure_search_filter>"
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.