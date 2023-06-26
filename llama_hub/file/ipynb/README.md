# IPynb Loader

This loader extracts text from `.ipynb` (jupyter notebook) files.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

IPYNBReader = download_loader("IPYNBReader")

# specify concatenate to determine whether to concat cells into one Document
loader = IPYNBReader(concatenate=True)
documents = loader.load_data(file=Path('./image.png'))
```
