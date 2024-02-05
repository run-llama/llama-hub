# Mintter Publications Reader

This reader loads documents from Mintter Hypermedia App. The user must have a local installation of Mintter App before running this loader. Then they need to specify if it's connecting to `author_publications` or `group_publications`. In case `group_publications` is selected use must specify `group_id` to load in the corresponding Document objects.

Note that this Loader extracts the contents using the Hypermedia structures to extract additional metadata and the hierarchical structure of the documents (blocks, etc). This information is extracted from the Mintter local daemon using gRPC calls. 

The Hypermedia structured data might compromise its use for RAG applications, given a single topic might span over several blocks. Additional care must be taken to retrive the correct context for RAG.

## Usage

Here's an example usage of the MintterPublicationsReader.

```python
from llama_index import download_loader
import os

MintterPublicationsReader = download_loader('MintterPublicationsReader')

access_method = "group_publications"
group_id = "<group_id>"

loader = MintterPublicationsReader(access_method=access_method, group_id="<group_id>")
documents = loader.load_data()
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
