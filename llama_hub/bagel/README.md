# Bagel Loader

The Bagel Loader returns a set of texts corresponding to query embeddings or query texts retrieved from a BagelDB.
The user initializes the loader with a BagelDB. They then pass in a query vector or a query text along with optional query parameters like metadata, where, where documents and include.

## Usage

Here's an example usage of the BagelReader.

```python
from llama_hub.bagel import BagelReader

# The chroma reader loads data from a persisted Chroma collection.
# This requires a collection name and a persist directory.
reader = BagelReader(
    collection_name="my_bagel_collection"
)

query_embeddings=[x1, x2, x3, ....]

documents = reader.load_data(collection_name="demo", query_vector=query_embeddings, n_results=5)


reader = BagelReader(
    collection_name="my_bagel_collection_2"
)

query_texts = ["some text"]

documents = reader.load_data(collection_name="demo", query_texts = query_texts, n_results=5)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
