# GraphQL Loader

This loader loads documents via GraphQL queries from a GraphQL endpoint. 
The user specifies a GraphQL endpoint URL with optional credentials to initialize the reader. 
By declaring the GraphQL query and optional variables (parameters) the loader can fetch the nested result docs.

## Usage

Here's an example usage of the GraphQLReader.

```python
from llama_index import download_loader
import os

GraphQLReader = download_loader('GraphQLReader')

uri = "<uri>"
headers = {}
query = """
"""
reader = GraphQLReader(uri, headers)
documents = reader.query(query, variables = {})
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) 
and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. 
See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
