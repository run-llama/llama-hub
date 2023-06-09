# PDF Loader

This loader extracts the text from a local PDF file using the `pdfminer.six` Python package. Any non-text elements are ignored. A single local file is passed in each time you call `load_data`.
This package often performs better than the builtin pdf parser based on the `pypdf` package.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

PDFMinerReader = download_loader("PDFMinerReader")

loader = PDFMinerReader()
documents = loader.load_data(file=Path('./article.pdf'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
