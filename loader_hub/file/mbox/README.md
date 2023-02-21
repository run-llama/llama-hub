# Mailbox Loader

This loader extracts the text from a local .mbox dump of emails.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

MboxReader = download_loader("MboxReader")
documents = MboxReader().load_data(file='./email.mbox') # Returns list of documents

```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
