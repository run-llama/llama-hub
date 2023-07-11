"""SingleStore reader."""

from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from llama_index import download_loader, ListIndex

import openai
from openai.embeddings_utils import get_embedding
import pymysql
import os
import json

SingleStoreReader = download_loader(loader_hub_url="https://raw.githubusercontent.com/apeng-singlestore/llama-hub/main/llama-hub", loader_class="SingleStoreReader")


# Example usage:

single_store_reader = SingleStoreReader(
    scheme="mysql",
    host="svc-1581bd74-8c1f-4de2-b3c0-c72858bb7a02-dml.aws-london-1.svc.singlestore.com",
    port="3306",
    user="admin",
    password="vyyjV2yBIRaWHIBUAAiFxAO88mSkjvRR",
    dbname="winter_wikipedia",
    table_name="winter_olympics_2022",
    content_field="text",
    vector_field="embedding"
)

# Example search_embedding as JSON string
query_text = "What countries won medals for curling?"

search_embedding = json.dumps(get_embedding(query_text, engine="text-embedding-ada-002"))

documents = single_store_reader.load_data(search_embedding=search_embedding)

index = ListIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query(query_text)

print(response)