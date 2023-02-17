# Image Loader

This loader extracts the text from an image that has text in it (e.g. a receipt (key-value pairs) or plain text image). For plain text it uses [pytesseract](https://pypi.org/project/pytesseract/) and for key-value pairs image [Donut](https://huggingface.co/docs/transformers/model_doc/donut) transformer model is used. The file extensions .png, .jpg, and .jpeg are preferred. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from gpt_index import download_loader

ImageReader = download_loader("ImageReader")

# If Image has key-value pairs text, use text_type = "key_value"
# If Image has plain test, use use text_type = "plain_text" for plain text
loader = ImageReader(text_type = "plain_text")
documents = loader.load_data(file=Path('./receipt.png'))
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
