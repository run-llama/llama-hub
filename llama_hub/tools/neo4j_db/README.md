
---

# Neo4j Schema Query Builder

The `Neo4jQueryToolSpec` class provides a way to query a Neo4j graph database based on a provided schema definition. The class uses a language model to generate Cypher queries from user questions and has the capability to recover from Cypher syntax errors through a self-healing mechanism.

## Table of Contents

- [Usage](#usage)
  - [Initialization](#initialization)
  - [Running a Query](#running-a-query)
- [Features](#features)

## Usage

### Initialization

Initialize the `Neo4jQueryToolSpec` class with:

```python
from llama_hub.tools.neo4j_db.base import Neo4jQueryToolSpec
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key="XXXX-XXXX",
    temperature=0,
    model='gpt-4',
)

query_builder = Neo4jQueryToolSpec('url', 'user', 'password', llm)
```

Where:

- `url`: Connection string for the Neo4j database.
- `user`: Username for the Neo4j database.
- `password`: Password for the Neo4j database.
- `llm`: A language model for generating Cypher queries (any type of LLM).

### Running a Query

To execute a Cypher query:

```python
query_builder.run("What is the city with the most airports?")
```

```
Generated Cypher:

MATCH (p:Port)-[:LOCATED_IN]->(c:City)
RETURN c.city_name AS City, COUNT(p) AS NumberOfAirports
ORDER BY NumberOfAirports DESC
LIMIT 1

Return list of Llama_index documents

```


## Features

- **Schema-Based Querying**: The class extracts the Neo4j database schema to guide the Cypher query generation.
- **Self-Healing**: On a Cypher syntax error, the class corrects itself to produce a valid query.
- **Language Model Integration**: Uses a language model for natural and accurate Cypher query generation.

---