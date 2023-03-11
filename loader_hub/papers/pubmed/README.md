# Pubmed Papers Loader

This loader fetchs the text from the most relevant scientific papers on Pubmed specified by a search query (e.g. "Alzheimers"). For each paper, the abstract is included in the `Document`. The search query may be any string.

## Usage

To use this loader, you need to pass in the search query. You may also optionally specify the maximum number of papers you want to parse for your search query (default is 10).

```python
from llama_index import download_loader

PubmedReader = download_loader("PubmedReader")

loader = PubmedReader()
documents = loader.load_data(search_query='amyloidosis')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
