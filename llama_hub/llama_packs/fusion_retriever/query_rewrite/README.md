# Query Rewriting Retriever Pack
This LlamaPack provides an example of query rewriting through our fusion retriever.

This specific template takes in a single retriever, and generates multiple queries against the retriever, and then fuses the results together.

## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack QueryRewritingRetrieverPack --download-dir ./query_rewriting_retriever_pack
```

You can then inspect the files at `./query_rewriting_retriever_pack` and use them as a template for your own project.

## Code Usage

You can download the pack to a the `./query_rewriting_retriever_pack` directory:

```python
from llama_index.llama_pack import download_llama_pack

# download and install dependencies
 QueryRewritingRetrieverPack = download_llama_pack(
  "QueryRewritingRetrieverPack", "./query_rewriting_retriever_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./query_rewriting_retriever_pack`.

Then, you can set up the pack like so:

```python
# create the pack
query_rewriting_retriever_pack = QueryRewritingRetrieverPack(
  nodes,
  chunk_size=256,
  vector_similarity_top_k=2,
  bm25_similarity_top_k=2
)
```

The `run()` function is a light wrapper around `query_engine.query()`.

```python
response = query_rewriting_retriever_pack.run("Tell me a bout a Music celebritiy.")
```

You can also use modules individually.

```python
# use the fusion retreiver
nodes = query_rewriting_retriever_pack.fusion_retriever.retrieve("query_str")

# use the vector retriever
nodes = query_rewriting_retriever_pack.vector_retriever.retrieve("query_str")
# use the bm25 retriever
nodes = query_rewriting_retriever_pack.bm25_retriever.retrieve("query_str")

# get the query engine
query_engine = query_rewriting_retriever_pack.query_engine
```