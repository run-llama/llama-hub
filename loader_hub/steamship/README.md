# Steamship Loader

This loader loads persistent Steamship files and converts them to a Document object. Requires an active Steamship API key.

## Usage

To use this loader, you need to pass in your API key during initialization.

You may then specify a `query` and/or a `file_handles` to fetch files.

```python
from llama_index import download_loader

SteamshipFileReader = download_loader("SteamshipFileReader")

loader = SteamshipFileReader(api_key="<api_key>")
documents = loader.load_data(
    "<workspace>", 
    query="filetag and value(\"import-id\")=\"import-001\"", 
    file_handles=["smooth-valley-9kbdr"]
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
