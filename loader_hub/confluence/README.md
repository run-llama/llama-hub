# Confluence Loader

This loader loads pages from a given Confluence site/instance. The user specifies a username, API token and the base URL for a Confluence instance to initialize
the ConfluenceReader. They then specify a set of `page_ids` and/or `space_id` to load in
the corresponding Document objects, if both are specified the union of both sets will be returned. 

## Usage

Here's an example usage of the ConfluenceReader.

```python
from llama_index import download_loader
import os

ConfluenceReader = download_loader('ConfluenceReader')

user_name = os.getenv("CONFLUENCE_USERNAME")
api_token = os.getenv("CONFLUENCE_API_TOKEN")
base_url = "https://yoursite.atlassian.com/wiki"

page_ids = ["<page_id>"]
space_id = "<space_id>"

reader = ConfluenceReader(user_name=user_name, api_token=api_token, base_url=base_url)
documents = reader.load_data(space_id=space_id, page_ids=page_ids)

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
