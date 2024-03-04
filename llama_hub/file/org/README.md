# Org Loader

This loader extracts the text from a local Org mode file. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file. You can split the headings into separated documents by specifying `split_depth` > 1. When `split_depth` is 0, the whole file becomes a single document.

```python
from pathlib import Path
from llama_index import download_loader

OrgReader = download_loader("OrgReader")

loader = OrgReader(split_depth=1)
documents = loader.load_data(file=Path('./inbox.org))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
