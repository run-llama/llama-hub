# Pinecone Loader

The Pinecone Loader returns a set of texts corresponding to embeddings retrieved from a Pinecone Index.
The user initializes the loader with a Pinecone index. They then pass in a query vector.

## Usage

Here's an example usage of the PineconeReader.

```python
from llama_index import download_loader
import os

PineconeReader = download_loader('PineconeReader')

# the id_to_text_map specifies a mapping from the ID specified in Pinecone to your text.
id_to_text_map = {
    "id1": "text blob 1",
    "id2": "text blob 2",
}

# the query_vector is an embedding representation of your query_vector
# Example query vector:
#   query_vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]

query_vector=[n1, n2, n3, ...]

reader = PineconeReader(api_key=api_key, environment="us-west1-gcp")
documents = reader.load_data(
    index_name='quickstart',
    id_to_text_map=id_to_text_map,
    top_k=3,
    vector=query_vector,
    separate_documents=True
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
