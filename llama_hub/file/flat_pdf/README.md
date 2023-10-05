# Flat PDF Loader

This loader extracts the text from a local flat PDF file using the `PyMuPDF` Python package and image loader. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need:

- Download `ImageReader` and `FlatPdfReader` using `download_loader`
- Init a `ImageReader`
- Init a `FlatPdfReader` and pass `ImageReader` on init
- Pass a `Path` to a local file in method `load_data`.

```python
from pathlib import Path
from llama_index import download_loader


ImageReader = download_loader("ImageReader")
imageLoader = ImageReader(text_type="plain_text")
FlatPdfReader = download_loader("FlatPdfReader")
pdfLoader = FlatPdfReader(image_loader=imageLoader)

document = pdfLoader.load_data(file=Path('./file.pdf'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/llama_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
