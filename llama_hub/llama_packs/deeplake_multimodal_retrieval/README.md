# DeepLake DeepMemory Pack

This LlamaPack inserts your multimodal data (texts, images) into deeplake and insantiates an deeplake retriever, which will use clip for embedding images and GPT4-V during runtime.
## Usage

You can download the pack to a `./deeplake_multimodal_pack` directory:

```python
from llama_hub.llama_packs import download_llama_pack

# download and install dependencies
DeepLakeMultimodalRetreiver = download_llama_pack(
  "DeepLakeMultimodalRetrieverPack", "./deeplake_multimodal_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./deepmemory_pack`.

Then, you can set up the pack like so:

```python
# setup pack arguments
from llama_index.vector_stores.types import MetadataInfo, VectorStoreInfo

nodes = [...]

# create the pack
deelake_pack = DeepLakeMultimodalRetreiver(
  collection_name="test",
  vector_store_info=vector_store_index 
  nodes=nodes,
)
```

The `run()` function is a light wrapper around `SimpleMultiModalQueryEngine`.

```python
response = deelake_pack.run("Tell me a bout a Music celebritiy.")
```

You can also use modules individually.

```python
# use the retreiver
retriever = deelake_pack.retriever
nodes = retriever.retrieve("query_str")

# use the query engine
query_engine = deelake_pack.query_engine
response = query_engine.query("query_str")
```