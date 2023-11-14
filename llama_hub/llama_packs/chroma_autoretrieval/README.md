# Chroma AutoRetrieval Pack

This LlamaPack inserts your data into chroma and insantiates an auto-retriever, which will use the LLM at runtime to set metadata filtering, top-k, and query string.

## Usage

```
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
ChromaAutoretrievalPack = download_llama_pack("ChromaAutoretrievalPack")

# setup pack arguments
from llama_index.vector_stores.types import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo(
    content_info="brief biography of celebrities",
    metadata_info=[
        MetadataInfo(
            name="category",
            type="str",
            description=(
                "Category of the celebrity, one of [Sports Entertainment, Business, Music]"
            ),
        ),
    ],
)

import chromadb
client = chromadb.EphemeralClient()

nodes = [...]

# create the pack
chroma_pack = ChromaAutoretrievalPack(
  collection_name="test",
  vector_store_info=vector_store_index 
  nodes=nodes,
  client=client
)

# use the retreiver
retriever = chroma_pack.retriever
nodes = retriever.retrieve("query_str")

# use the query engine
query_engine = chroma_pack.query_engine
response = query_engine.query("query_str")
```