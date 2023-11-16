# JSON Loader

This loader extracts the text in a formatted manner from a JSON or JSONL file. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file and set the `is_jsonl` parameter to `True` for JSONL files or `False` for regular JSON files.

### JSON

```python
from pathlib import Path
from llama_index import download_loader

JSONReader = download_loader("JSONReader")

loader = JSONReader()
documents = loader.load_data(Path('./data.json'))
```

### JSONL

```python
from pathlib import Path
from llama_index import download_loader

JSONReader = download_loader("JSONReader")

loader = JSONReader()
documents = loader.load_data(Path('./data.jsonl'), is_jsonl=True)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
