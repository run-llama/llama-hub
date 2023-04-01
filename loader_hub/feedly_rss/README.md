# Feedly Loader

This loader fetches the entries from a list of RSS feeds subscribed in [Feedly](https://feedly.com). You must initialize the loader with your [Feedly API token](https://developer.feedly.com), and the pass the category name which you want to extract.

## Usage
Since `pkg_resources` does not support VCS URLs directly. You need to install the package first.

```bash
pip install git+https://github.com/feedly/python-api-client.git@master#egg=feedly-client
```

```python
from llama_index import download_loader
feedlyRssReader = download_loader("FeedlyRssReader")

loader = feedlyRssReader(bearer_token = "[YOUR_TOKEN]")
documents = loader.load_data(category_name = "news")
```