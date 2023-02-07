# Microsoft PowerPoint Loader

This loader extracts the text from a local Microsoft PowerPoint (.pptx) file. Image elements are automatically captioned and inserted as text into the final `Document` using [GPT2 Image Captioning model](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning). A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from gpt_index import download_loader

PptxReader = download_loader("PptxReader")

loader = PptxReader()
documents = loader.load_data(file=Path('./deck.pptx'))
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
