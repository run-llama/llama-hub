# Chinese/Japanese/Korean PDF Loader

This loader extracts the text from a local PDF file using the `pdfminer.six` Python package, which is used instead of `PyPDF2` in order to load Asian languages, e.g. shift-jis encoded Japanese text. The officially supported characters are those in CJK (Chinese, Japanese, and Korean), though it may work for other languages as well. Any non-text elements are ignored. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

CJKPDFReader = download_loader("CJKPDFReader")

loader = CJKPDFReader()
documents = loader.load_data(file=Path('./article.pdf'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
