# Make Loader

The Make Loader offers a webhook wrapper that can take in a query response as an input.
**NOTE**: The Make Loader does not offer the ability to load in Documents. Currently,
it is designed so that you can plug in LlamaIndex Response objects into downstream Make workflows.

## Usage

Here's an example usage of the `MakeWrapper`.

```python
from llama_index import download_loader
import os

MakeWrapper = download_loader('MakeWrapper')

# load index from disk
index = GPTVectorStoreIndex.load_from_disk('../vector_indices/index_simple.json')

# query index
query_str = "What did the author do growing up?"
response = index.query(query_str)

# Send response to Make.com webhook
wrapper = MakeWrapper()
wrapper.pass_response_to_webhook(
    "<webhook_url>,
    response,
    query_str
)

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
