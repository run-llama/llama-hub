# Microsoft PowerPoint Slide Loader

This loader reads a local Microsoft PowerPoint (.pptx) file and creates a list of Documents, each corresponding to a slide in the presentation.

## Usage

To use this loader, pass either a filename or a `Path` to a local file.

**Parameters:**

- file (required): Path to the PowerPoint file.
- extra_info (optional): Additional information to be merged into the metadata of each document.
- join_char (optional, default='\n'): Character used to join the text of shapes within a slide.
- include_shapes (optional, default=False): If True, includes information about individual shapes in the metadata of each document.

```python
from pathlib import Path
from llama_hub import PptxSlideReader

loader = PptxSlideReader()
documents = loader.load_data(
  file=Path('./deck.pptx'),
  extra_info={"source" : "my-deck.pptx"},
  join_char='\n',
  include_shapes=TRUE
)
# Alternatively: documents = loader.load_data(file='./deck.pptx')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/langchain-ai/langchain) Agent. See [here](https://github.com/run-llama/llama-hub/tree/main/llama_hub) for examples.

## FAQs

### What is the difference with file/pptx loader?

The file/pptx loader creates one Document that joins all the slides. In contrast, this file/pptx-slide loader creates a list of Documents corresponding to slides in the presentation.
