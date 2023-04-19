# DeepLake Reader

The DeepLake loader returns a set of texts corresponding to embeddings retrieved from a DeepLake vector store.
The user initializes the loader with an auth token. They then pass in a query vector.

## Usage

Here's an example usage of the DeepLake reader.

```python
from llama_index import download_loader
import os

DeepLakeReader = download_loader("DeepLakeReader")

reader = DeepLakeReader(token="<token>")
# the query_vector is an embedding representation of your query_vector
# Example query vector:
#   query_vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]

query_vector=[n1, n2, n3, ...]

# NOTE: Required args are query_vector, dataset_path.
documents = reader.load_data(
    query_vector=query_vector,
    dataset_path="<dataset_path>",
    limit=5
)

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
