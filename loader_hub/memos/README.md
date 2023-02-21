# Memos Loader

This loader fetchs memos from self-host memos

## Usage

To use this loader, you need to pass in an array of Bilibili video links.

```python
from gpt_index import download_loader

MemosReader = download_loader("MemosReader")
loader = MemosReader()
documents = loader.load_data(creator_id=101)
```


This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.