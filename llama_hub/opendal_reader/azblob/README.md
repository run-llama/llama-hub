# Azblob Loader

This loader parses any file stored on Azblob.

All files are temporarily downloaded locally and subsequently parsed with `SimpleDirectoryReader`. Hence, you may also specify a custom `file_extractor`, relying on any of the loaders in this library (or your own)!

> Azblob loader is based on `OpendalReader`.

## Usage

```python
from llama_index import download_loader

OpendalAzblobReader = download_loader("OpendalAzblobReader")

loader = OpendalAzblobReader(
    container='container',
    path='path/to/data/',
    endpoint='[endpoint]',
    account_name='[account_name]',
    account_key='[account_key]',
)
documents = loader.load_data()
```

---

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
