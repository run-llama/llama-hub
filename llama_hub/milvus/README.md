# Milvus Loader

The Milvus Loader returns a set of texts corresponding to embeddings retrieved from a Milvus collection.
The user initializes the loader with parameters like host/port. 

During query-time, the user passes in the collection name, query vector, and a few other parameters.

## Usage

Here's an example usage of the MilvusReader.

```python
from llama_index import download_loader
import os

MilvusReader = download_loader("MilvusReader")

reader = MilvusReader(
    host="localhost", port=19530, user="<user>", password="<password>", use_secure=False
)
# the query_vector is an embedding representation of your query_vector
# Example query vector:
#   query_vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]

query_vector=[n1, n2, n3, ...]

documents = reader.load_data(
    query_vector=query_vector,
    collection_name="demo",
    limit=5
)

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
