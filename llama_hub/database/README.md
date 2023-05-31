# Database Loader

This loader connects to a database (using SQLAlchemy under the hood). The user specifies a query and extracts Document objects corresponding to the results. For instance, you can use this loader to easily connect to a database on AWS, Snowflake, etc. and pass the documents into a `GPTSQLStructStoreIndex` from LlamaIndex.

## Usage

Here's an example usage of the DatabaseReader.

```python
from llama_index import download_loader

DatabaseReader = download_loader('DatabaseReader')

reader = DatabaseReader(
    scheme = "postgresql", # Database Scheme
    host = "localhost", # Database Host
    port = "5432", # Database Port
    user = "postgres", # Database User
    password = "FakeExamplePassword", # Database Password
    dbname = "postgres", # Database Name
)

query = f"""
SELECT
    CONCAT(name, ' is ', age, ' years old.') AS text
FROM public.users
WHERE age >= 18
"""

documents = reader.load_data(query=query)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
