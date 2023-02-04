# Database Loader

This loader connects to a database (using SQLAlchemy under the hood). The user specifies a query and extracts Document objects corresponding to the results.

## Usage

Here's an example usage of the DatabaseReader.

```python
from gpt_index import download_loader

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
