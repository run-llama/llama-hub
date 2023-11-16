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

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

## Note
### Microsoft SQL Server database
In order to connect to Microsoft SQL Server database, it is required to install Microsoft ODBC driver. See [here](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16)

After installing the drivers, you should be able to use the DatabaseReader to initiate Microsoft SQL Server connection and the connectionstring uri follow this format ```'mssql+pyodbc://<username>:<Password>@<SQLServer>:<Port>/<Database Name>?driver=<DriverName>'```

```python
from llama_index.utilities.sql_wrapper import SQLDatabase

reader = DatabaseReader(
    sql_database = SQLDatabase.from_uri('mssql+pyodbc://dummyuser:dummypassword@dummysqlserver:1433/dummydb?driver=ODBC+Driver+18+for+SQL+Server')
)
```

After installing the drivers and you are still unsure of the driver package name, run the following code to get the list of installed Microsoft ODBC driver
```python
import pyodbc
pyodbc.drivers()
```