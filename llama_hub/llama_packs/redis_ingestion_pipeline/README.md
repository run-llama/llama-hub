# Redis Ingestion Pipeline Pack

This LlamaPack creates an [ingestion pipeline](https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/root.html), with both a cache and vector store backed by Redis.

## Usage

You can download the pack to a `./redis_ingestion_pack` directory:

```python
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
RedisIngestionPipelinePack = download_llama_pack(
  "RedisIngestionPipelinePack", "./redis_ingestion_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./redis_ingestion_pack`.

Then, you can set up the pack like so:

```python
from llama_index.text_splitter import SentenceSplitter
from llama_index.embeddings import OpenAIEmbedding

transformations = [
  SentenceSplitter(),
  OpenAIEmbedding()
]

# create the pack
ingest_pack = RedisIngestionPipelinePack(
  transformations,
  hostname="localhost",
  port=6379,
  cache_collection_name="ingest_cache",
  vector_collection_name="vector_store",
)
```

The `run()` function is a light wrapper around `pipeline.run()`. 

You can use this to ingest data and then create an index from the vector store.

```python
pipeline.run(documents)

index = VectorStoreIndex.from_vector_store(inget_pack.vector_store)
```

You can learn more about the ingestion pipeline at the [LlamaIndex documentation](https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/root.html).