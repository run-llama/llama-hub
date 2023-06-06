# Obsidian (Markdown) Loader

This loader loads documents from a markdown directory (for instance, an Obsidian vault).

## Usage

Here's an example usage of the ObsidianReader.

```python
from llama_index import download_loader
import os

ObsidianReader = download_loader('ObsidianReader')
documents = ObsidianReader('/path/to/dir').load_data() # Returns list of documents
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
