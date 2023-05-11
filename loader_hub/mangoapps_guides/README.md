# MangoppsGuides Loader

This loader fetches the text from Mangopps Guides.

## Usage

To use this loader, you need to pass base url of the MangoppsGuides installation (e.g. `https://guides.mangoapps.com/`)

```python
from llama_index import download_loader

MangoppsGuidesReader = download_loader("MangoppsGuidesReader")

loader = MangoppsGuidesReader(domain_url="https://guides.mangoapps.com/")
documents = loader.load_data()
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
