# Image Loader

This loader extracts the text from an image that has text in it, e.g. a receipt (key-value pairs) or a plain text image. If the image has plain text, the loader uses [pytesseract](https://pypi.org/project/pytesseract/). If image has text in key-value pairs like an invoice, the [Donut](https://huggingface.co/docs/transformers/model_doc/donut) transformer model is used. The file extensions .png, .jpg, and .jpeg are preferred. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

ImageReader = download_loader("ImageReader")

# If the Image has key-value pairs text, use text_type = "key_value"
loader = ImageReader(text_type = "key_value")
documents = loader.load_data(file=Path('./receipt.png'))

# If the Image has plain text, use text_type = "plain_text"
loader = ImageReader(text_type = "plain_text")
documents = loader.load_data(file=Path('./image.png'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
