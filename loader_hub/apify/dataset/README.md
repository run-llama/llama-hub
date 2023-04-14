# Apify Dataset Loader

Apify is a cloud platform for web scraping and data extraction,
which provides an [ecosystem](https://apify.com/store) of more than a thousand
ready-made apps called *Actors* for various scraping, crawling, and extraction use cases.

This loader loads documents from an [Apify dataset](https://docs.apify.com/platform/storage/dataset).

## Usage

Here's an example usage of the ApifyDataset loader.

```python
from llama_index import download_loader
from llama_index.readers.schema.base import Document
import os

def tranform_dataset_item(item):
    return Document(
        item.get("text"),
        extra_info={
            "url": item.get("url"),
        },
    )

ApifyDataset = download_loader("ApifyDataset")

reader = ApifyDataset(os.environ.get("APIFY_API_TOKEN"))
documents = reader.load_data(dataset_id="<dataset_id>", dataset_mapping_function=tranform_dataset_item)
```
