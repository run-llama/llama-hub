# Image Loader (Blip2)

This loader captions an image file containing a tabular graph (bar chart, line charts) using deplot.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

ImageTabularGraphReader = download_loader("ImageTabularGraphReader")

loader = ImageTabularGraphReader()
documents = loader.load_data(file=Path('./image.png'))
```
