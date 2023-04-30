# Async Website Loader

This loader is an asynchronous web scraper that fetches the text from static websites by converting the HTML to text.

## Usage

To use this loader, you need to pass in an array of URLs.

```python
from llama_index import download_loader

AsyncWebPageReader = download_loader("AsyncWebPageReader")

loader = AsyncWebPageReader()
documents = loader.load_data(urls=['https://google.com'])
```
