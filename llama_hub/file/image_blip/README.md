# Image Loader (Blip)

This loader captions an image file using Blip.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

ImageCaptionReader = download_loader("ImageCaptionReader")

loader = ImageCaptionReader()
documents = loader.load_data(file=Path('./image.png'))
```
