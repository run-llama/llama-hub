# Weaviate Loader

The Weaviate Loader returns a set of texts corresponding to embeddings retrieved from Weaviate.
The user initializes the WeaviateReader with authentication credentials. 
They then pass in a class_name + properties to fetch documents, or pass in a raw GraphQL query.

## Usage

Here's an example usage of the WeaviateReader.

```python
import weaviate
from llama_index import download_loader
import os

WeaviateReader = download_loader('WeaviateReader')

# See https://weaviate.io/developers/weaviate/current/client-libraries/python.html
# for more details on authentication
resource_owner_config = weaviate.AuthClientPassword(
  username = "<username>", 
  password = "<password>", 
)

# initialize reader
reader = WeaviateReader("https://<cluster-id>.semi.network/", auth_client_secret=resource_owner_config)

# 1) load data using class_name and properties
# docs = reader.load_data(
#    class_name="Author", properties=["name", "description"], separate_documents=True
# )

documents = reader.load_data(
    class_name="<class_name>", 
    properties=["property1", "property2", "..."], 
    separate_documents=True
)

# 2) example GraphQL query
# query = """
# {
#   Get {
#     Author {
#       name
#       description
#     }
#   }
# }
# """
# docs = reader.load_data(graphql_query=query, separate_documents=True)

query = """
{
  Get {
    <class_name> {
      <property1>
      <property2>
      ...
    }
  }
}
"""

documents = reader.load_data(graphql_query=query, separate_documents=True)



```
