# Azure Storage Blob Loader

This loader parses any file stored as an Azure Storage blob or the entire container (with an optional prefix / attribute filter) if no particular file is specified. When initializing `AzStorageBlobReader`, you may pass in your account url with a SAS token or crdentials to authenticate.

All files are temporarily downloaded locally and subsequently parsed with `SimpleDirectoryReader`. Hence, you may also specify a custom `file_extractor`, relying on any of the loaders in this library (or your own)!

## Usage

To use this loader, you need to pass in the name of your Azure Storage Container. After that, if you want to just parse a single file, pass in its blob name. Note that if the file is nested in a subdirectory, the blob name should contain that, so like `subdirectory/input.txt`.

Otherwise, you may specify a prefix filter or additional attributes if you only want to parse certain files in the Container, or a subdirectory. 

### Using a Storage Accout SAS URL
```python
from llama_index import download_loader

AzStorageBlobReader = download_loader("AzStorageBlobReader")

loader = AzStorageBlobReader(container='scrabble-dictionary', blob='dictionary.txt', account_url='<SAS_URL>')

documents = loader.load_data()
```

### Using Azure AD
Ensure the Azure Identity library is available ```pip install azure-identity```

The sample below downloads all files in the container using the default credential, alternative credential options are avaible such as a service principal ```ClientSecretCredential``` 

```python
from llama_index import download_loader
from azure.identity import DefaultAzureCredential

default_credential = DefaultAzureCredential()

AzStorageBlobReader = download_loader("AzStorageBlobReader")

loader = AzStorageBlobReader(container_name='scrabble-dictionary', account_url='https://<storage account name>.blob.core.windows.net', credential=default_credential)

documents = loader.load_data()
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
