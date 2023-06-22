# Sitemap Loader

This loader is an asynchronous web scraper that fetches the text from static websites by using its sitemap and optionally converting the HTML to text.

It is based on the [Async Website Loader](../async_web/README.md)

## Usage

To use this loader, you just declare the sitemap.xml url like this:

```python
from llama_index import download_loader

AsyncWebPageReader = download_loader("SitemapReader")

loader = AsyncWebPageReader()
documents = loader.load_data(sitemap_url=['https://gpt-index.readthedocs.io/sitemap.xml'])
```

Be sure that the sitemap_url contains a proper [Sitemap](https://www.sitemaps.org/protocol.html)