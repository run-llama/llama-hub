# Image Loader (Blip2)

This loader captions an image file using Blip2 (a multimodal VisionLLM similar to GPT4).

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

ImageVisionLLMReader = download_loader("ImageVisionLLMReader")

loader = ImageVisionLLMReader()
documents = loader.load_data(file=Path('./image.png'))
```
