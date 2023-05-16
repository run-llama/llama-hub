# Graph Loader

This loader loads documents via Graph queries from a Graph endpoint. 
The user specifies a Graph endpoint URL with optional credentials to initialize the reader. 
By declaring the Graph query and optional variables (parameters) the loader can fetch the nested result docs.

## Usage

Here's an example usage of the GraphReader.
You can test out queries directly with the demo server: demo.neo4jlabs.com or with a free instance https://neo4j.com/aura

```python
from llama_index import download_loader
import os

GraphReader = download_loader('GraphReader')

uri = "neo4j+s://demo.neo4jlabs.com"
username = "stackoverflow"
password = "stackoverflow"
database = "stackoverflow"

query = """
    MATCH (q:Question)-[:TAGGED]->(:Tag {name:$tag})
    RETURN q.title as title
    ORDER BY q.createdAt DESC LIMIT 10
"""
reader = GraphReader(uri, username, password, database)
documents = reader.load_data(query, parameters = {"tag":"lua"})
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) 
and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. 
See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

It uses the [Neo4j Graph Database](https://neo4j.com/developer) for the Graph queries.