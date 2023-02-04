# Notion Loader

This loader loads documents from Notion. The user specifies an API token to initialize
the NotionPageReader. They then specify a set of `page_ids` or `database_id` to load in
the corresponding Document objects.

## Usage

Here's an example usage of the NotionPageReader.

```python
from gpt_index import download_loader
import os

NotionPageReader = download_loader('NotionPageReader')

integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
page_ids = ["<page_id>"]
reader = NotionPageReader(integration_token=integration_token)
documents = reader.load_data(page_ids=page_ids)

```
