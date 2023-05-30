# ChatGPT Plugin Loader

The ChatGPT Plugin loader returns a set of documents from a server that implements that.
[ChatGPT Retrieval Plugin interface](https://github.com/openai/chatgpt-retrieval-plugin).

## Usage

Here's an example usage of the ChatGPTRetrievalPluginReader.

```python
from llama_index import download_loader

ChatGPTRetrievalPluginReader = download_loader("ChatGPTRetrievalPluginReader")

bearer_token = os.getenv("BEARER_TOKEN")
reader = ChatGPTRetrievalPluginReader(
    endpoint_url="http://localhost:8000",
    bearer_token=bearer_token
)

documents = reader.load_data("text query")
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
