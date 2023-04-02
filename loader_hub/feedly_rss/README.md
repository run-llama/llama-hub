# Feedly Loader

This loader fetches the entries from a list of RSS feeds subscribed in [Feedly](https://feedly.com). You must initialize the loader with your [Feedly API token](https://developer.feedly.com), and the pass the category name which you want to extract.

## Usage
```python
from llama_index import download_loader
feedlyRssReader = download_loader("FeedlyRssReader")

loader = feedlyRssReader(bearer_token = "[YOUR_TOKEN]")
documents = loader.get_feedly_feeds(category_name = "news", max_count = 100)
```

## Dependencies
[feedly-client](https://pypi.org/project/feedly-client/)