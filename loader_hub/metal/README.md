# Metal Loader
[Metal](https://getmetal.io)


The Metal Loader returns a set of texts corresponding to embeddings retrieved from a Metal Index.

The user initializes the loader with a Metal index. They then pass in a text query.

## Usage

Here's an example usage of the MetalReader.

```python
from llama_index import download_loader
import os


MetalReader = download_loader('MetalReader')

query_embedding = [n1, n2, n3, ...] # embedding of the search query

reader = MetalReader(
    api_key=api_key,
    client_id=client_id,
    index_id=index_id
)

documents = reader.load_data(
    top_k=3,
    query_embedding=query_embedding,
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
