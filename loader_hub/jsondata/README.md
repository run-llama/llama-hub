# Json Data Loader

This loader extracts the text in a formatted manner from Json data in a Python dictionary. The `data` is passed to `load_data`.

## Usage

To use this loader, you need to pass in Json data in a Python dictionary.

```python
import requests
from llama_index import download_loader
headers = {
    "Authorization": "your_api_token"
}
data = requests.get("your-api-url", headers=headers).json()
JsonDataReader = download_loader("JsonDataReader")

loader = JsonDataReader()
documents = loader.load_data(data)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
