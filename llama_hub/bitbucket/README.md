# Bilibili Transcript Loader

This loader utilizes the Bitbucket API to load the files inside a Bitbucket repository as Documents in an index.

## Usage

To use this loader, you need to provide as environment variables the `BITBUCKET_API_KEY` and the `BITBUCKET_USERNAME`.

```python
from llama_index import VectorStoreIndex
os.environ['BITBUCKET_USERNAME']='myusername'
base_url = "https://myserver/bitbucket"
project_key = 'mykey'
index = VectorStoreIndex.from_documents(BitbucketReader(base_url=base_url, project_key=project_key, branch='refs/heads/develop').load_data())
```


This loader is designed to be used as a way to load data into [Llama Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
