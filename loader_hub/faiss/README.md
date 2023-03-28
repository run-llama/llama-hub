# Faiss Loader

The Faiss Loader returns a set of texts corresponding to embeddings retrieved from a [Faiss Index](https://github.com/facebookresearch/faiss), an efficient way to do similar search and clustering, developed by Meta. The user initializes the loader with a Faiss index. They then pass in a query vector.

## Usage

Here's an example usage of the FaissReader.

```python
from llama_index import download_loader
import faiss

FaissReader = download_loader('FaissReader')

id_to_text_map = {
    "id1": "text blob 1",
    "id2": "text blob 2",
}
index = faiss.IndexFlatL2(d)
# add embeddings to the index
index.add(...)

# initialize reader
reader = FaissReader(index)
# To load data from the Faiss index, you must specify:
# k: top nearest neighbors
# query: a 2D embedding representation of your queries (rows are queries)
k = 4
query1 = np.array([...])
query2 = np.array([...])
query=np.array([query1, query2])
documents = reader.load_data(query=query, id_to_text_map=id_to_text_map, k=k)

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
