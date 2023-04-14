# Apify Actor Loader

Apify is a cloud platform for web scraping and data extraction,
which provides an [ecosystem](https://apify.com/store) of more than a thousand
ready-made apps called *Actors* for various scraping, crawling, and extraction use cases.

This loader runs an Apify Actor and when it is finished loads its results.

## Usage

Here's an example usage:

```python
from llama_index import download_loader
from llama_index.readers.schema.base import Document
import os

def tranform_dataset_item(item):
    return Document(
        item.get('text'),
        extra_info={
            "url": item.get('url'),
        },
    )

ApifyCallActor = download_loader('ApifyCallActor')

reader = ApifyCallActor(os.environ.get('APIFY_API_TOKEN'))
documents = reader.load_data(
    actor_id="apify/website-content-crawler",
    run_input={"startUrls": [{"url": "https://gpt-index.readthedocs.io/en/latest"}]}
    dataset_mapping_function=tranform_dataset_item,
)
```
