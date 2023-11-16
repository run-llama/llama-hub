# Sitemap Index Loader

This loader is an asynchronous web scraper that fetches the text from static websites 
which have multiple sitemaps by using its sitemap index and optionally converting the HTML to text

It is based on the [Sitemap Loader](https://llamahub.ai/l/web-sitemap)

## Usage

To use this loader, you just declare the sitemap_index.xml url like this:

```python
from llama_hub.web.sitemap_index import SitemapIndexReader

# for jupyter notebooks uncomment the following two lines of code:
# import nest_asyncio
# nest_asyncio.apply()

loader = SitemapIndexReader()
documents = loader.load_data(sitemap_index_url='https://docs.aws.amazon.com/sitemap_index.xml')
```

Be sure that the sitemap_index_url contains a proper [Sitemap Index](https://www.sitemaps.org/protocol.html#index)

## Filter option

You can filter sitemaps from the sitemap index that are actually being crawled by adding the *filter* argument to the load_data method

```python
documents = loader.load_data(
    sitemap_index_url='https://docs.aws.amazon.com/sitemap_index.xml', 
    sitemap_url_filters=["AmazonCloudWatch", "amazondynamodb"])
# only crawl sitemaps that contain these strings
```

## Issues Jupyter Notebooks asyncio

If you get a `RuntimeError: asyncio.run() cannot be called from a running event loop` you might be interested in this (solution here)[https://saturncloud.io/blog/asynciorun-cannot-be-called-from-a-running-event-loop-a-guide-for-data-scientists-using-jupyter-notebook/#option-3-use-nest_asyncio]


### Old Usage 

use this syntax for earlier versions of llama_index where llama_hub loaders where loaded via separate download process:

```python
from llama_index import download_loader

SitemapIndexReader = download_loader("SitemapIndexReader")

loader = SitemapIndexReader()
documents = loader.load_data(sitemap_index_url='https://docs.aws.amazon.com/sitemap_index.xml')
```