# BoardDocs Loader

This loader retrieves an agenda and associated material from a BoardDocs site.

This loader is not endorsed by, developed by, supported by, or in any way formally affiliated with Diligent Corporation.

## Usage

To use this loader, you'll need to specify which BoardDocs site you want to load.

```python
from llama_index import download_loader

BoardDocsReader = download_loader("BoardDocsReader")
loader = BoardDocsReader()
# For a site URL https://go.boarddocs.com/ca/redwood/Board.nsf/Public
# your boarddocssite should be set to 'ca/redwood'
documents = loader.load_data(boarddocssite=['ca/redwood'])
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
