# PDF Loader

This loader extracts the text from a local PDF file using the `pdfplumber` Python package. Any non-text elements are ignored. A single local file is passed in each time you call `load_data`.
This package often pulls text data much more cleanly than the builtin `pypdf` parser, albeit somewhat slower.

## Usage

To use this loader, you need to pass in the local path to the file, as a string, to the `load_data()` method.

```python
from llama_index import download_loader

PDFPlumberReader = download_loader("PDFPlumberReader")

loader = PDFPlumberReader()
documents = loader.load_data(file='./article.pdf')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
