# SDL Loader

This loader extracts definitions from a Schema Definition Language file, used to specify the data for a GraphQL endpoint

## Usage

To use this loader, pass in the filename for the SDL file.

This tool has a more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/shopify.ipynb) and [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/shopify.ipynb)

```python
from llama_hub.file.sdl import SDLReader

loader = SDLReader()
documents = loader.load_data('./data/shopify.graphql')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
