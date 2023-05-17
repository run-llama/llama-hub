# Json Data Loader

This loader extracts the text in a formatted manner from Json data in a Python dictionary. The `data` is passed to `load_data`.  Ideal use case is for consuming REST API JSON data.

## Usage

To use this loader, you need to pass in Json data in a Python dictionary.

```python
import requests
from llama_index import GPTVectorStoreIndex, download_loader
headers = {
    "Authorization": "your_api_token"
}
data = requests.get("your-api-url", headers=headers).json()

JsonDataReader = download_loader("JsonDataReader")
loader = JsonDataReader()
documents = loader.load_data(data)
index = GPTVectorStoreIndex.from_documents(documents)
index.query("Question about your data")
```

