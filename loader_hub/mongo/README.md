# Mongo Loader

This loader loads documents from MongoDB. The user specifies a Mongo instance to
initialize the reader. They then specify the collection name and query params to
fetch the relevant docs.

## Usage

Here's an example usage of the SimpleMongoReader.

```python
from gpt_index import download_loader
import os

SimpleMongoReader = download_loader('SimpleMongoReader')

host = "<host>"
port = "<port>"
db_name = "<db_name>"
collection_name = "<collection_name>"
# query_dict is passed into db.collection.find()
query_dict = {}
reader = SimpleMongoReader(host, port)
documents = reader.load_data(db_name, collection_name, query_dict=query_dict)
```
