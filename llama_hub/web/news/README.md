# News Article Loader

This loader makes use of the `newspaper3k` library to parse web page urls which have news
articles in them.

## Usage
Pass in an array of individual page URLs:
```python
from llama_index import download_loader

NewsArticleReader = download_loader("NewsArticleReader")

reader = NewsArticleReader()
documents = reader.load_data([
    'https://www.cnbc.com/2023/08/03/amazon-amzn-q2-earnings-report-2023.html',
    'https://www.theverge.com/2023/8/3/23818388/brave-search-image-video-results-privacy-index'
])
```

# RSS News Loader

This loader allows fetching text from an RSS feed. It uses the `feedparser` module
to fetch the feed and the `NewsArticleLoader` to load each article.

## Usage

To use this loader, pass in an array of URLs of RSS feeds. It will download the pages referenced in each feed and 
combine them:
```python
from llama_index import download_loader

urls = [
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://roelofjanelsinga.com/atom.xml"
]

RSSNewsReader = download_loader("RSSNewsReader")
reader = RSSNewsReader()

documents = reader.load_data(urls=urls)
```

Or OPML content:
```python
with open("./sample_rss_feeds.opml", "r") as f:
    documents = reader.load_data(opml=f.read())
```

We can also pass in args for the NewsArticleLoader which parses each article:
```python
documents = reader.load_data(urls=urls, nlp=True)
```
