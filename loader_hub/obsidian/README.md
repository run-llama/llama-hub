# Obsidian (Markdown) Loader

This loader loads documents from a markdown directory (for instance, an Obsidian vault).

## Usage

Here's an example usage of the ObsidianReader.

```python
from gpt_index import download_loader
import os

ObsidianReader = download_loader('ObsidianReader')
documents = ObsidianReader('/path/to/dir').load_data() # Returns list of documents 
```
