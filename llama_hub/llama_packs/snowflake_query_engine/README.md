# Snowflake Query Engine Pack

This LlamaPack uses `snowflake-sqlalchemy` to connect to Snowflake, then calls `NLSQLTableQueryEngine` to query data.

## Usage

You can download the pack to a the `./snowflake_pack` directory:

```python
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
SnowflakeQueryEnginePack = download_llama_pack(
  "SnowflakeQueryEnginePack", "./snowflake_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./snowflake_pack`.

First, add the Snowflake DB connection details in a file named `credentials.json` at your project root, the same directory where your main python file is located. See below the sample file content, replace the placeholder values with your actual Snowflake DB connection details.

```
{
  "account": "<YOUR-ORG>-<YOUR-ACCOUNT>",
  "user": "<YOUR-USER-NAME>",
  "role": "<USER-ROLE>",
  "password": "<USER-PASSWORD>",
  "warehouse": "<WAREHOUSE>",
  "database": "<DATABASE>",
  "schema": "<SCHEMA>"
}

```
`NLSQLTableQueryEngine` uses OpenAI models by default, ensure you set your OpenAI API key.

Then, you can set up the pack by passing in the table(s):

```python
# create the pack
snowflake_pack = SnowflakeQueryEnginePack(
  tables=["<TABLE1>", "<TABLE2>",...]
)
```

The `run()` function is a light wrapper around `query_engine.query()`.  See below a sample query run. You can add additional prompt in the query text.

```python
response = snowflake_pack.run("Give me the repo id with the most stars on 2023-12-01.")
```
