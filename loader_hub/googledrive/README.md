# Google Drive Loader

This loader currently reads files from google drive folder/ file ids.

## Usage

To use this loader, you need to pass in a List of file id's or folder id.

You need to get your `credentials.json` file by following the steps mentioned [here](https://developers.google.com/drive/api/v3/quickstart/python) and create duplicate file of `credentials.json` with name `client_secrets.json` which will be used by pydrive for downloading files before proceeding further.

```python
from gpt_index import download_loader

GoogleDriveReader = download_loader("GoogleDriveReader")

loader = GoogleDriveReader()

#### Using folder id
documents = loader.load_data(folder_id="folderid")

#### Using file ids
documents = loader.load_data(file_ids=["fileid1", "fileid2"])
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
