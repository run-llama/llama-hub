# Twitter Loader

This loader converts an iterable (e.g. list) of strings into `Document`s.

## Usage

To use this loader, you need to pass in an iterable of arbitrary strings.

```python
from gpt_index import download_loader

StringIterableReader = download_loader("StringIterableReader")

loader = StringIterableReader()
documents = loader.load_data(texts=['hello!', 'this', 'is', 'an', 'example'])
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/loader-hub/tree/main) for examples.
