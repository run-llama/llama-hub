# Macrometa GDN Loader

This loader takes in a Macrometa federation URL, API key, and collection name and returns a list of vectors. 

## Usage

To use this loader, you need to pass the URL and API key through the class contructor, and then load the data using an array of collection names.

```python
from llama_index import download_loader

MacrometaGDNLoader = download_loader('MacrometaGDNLoader')

collections = ['test_collection']
loader = MacrometaGDNLoader(url="https://api-macrometa.io",apikey="test")
vectors= loader.load_data(collection_list=collections)
```