# Google Drive Loader

This loader currently fetches the text from `.txt` files from google drive folder/ file id.

## Usage

To use this loader, you need to pass in a List of file id's or folder id.

You need to get your `credentials.json` file by following the steps mentioned [here](https://developers.google.com/drive/api/v3/quickstart/python) before proceeding further.

```python
from gpt_index import download_loader

YoutubeTranscriptReader = download_loader("GoogleDriveReader")

loader = GoogleDriveReader()
documents = loader.load_data(folder_id="folderid")
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
