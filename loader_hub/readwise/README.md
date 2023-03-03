# Readwise Reader

Use Readwise's export API to fetch your highlights from web articles, epubs, pdfs, Kindle, YouTube, and load the resulting text into LLMs.

## Setup

1. Get your Readwise API key from [readwise.io/access_token](https://readwise.io/access_token).

## Usage

Here is an example usage of the Readwise Reader:

```python
from llama_index import GPTSimpleVectorIndex, download_loader

ReadwiseReader = download_loader("ReadwiseReader")

token = os.getenv("READWISE_API_KEY")
documents = loader.load_data()
index = GPTSimpleVectorIndex(documents)

this_weeks_documents = 

index.query("What was the paper 'Attention is all you need' about?")
```

You can also query for highlights that have been created after a certain time:

```python
import os
import datetime
from llama_index import GPTSimpleVectorIndex, download_loader

ReadwiseReader = download_loader("ReadwiseReader")

token = os.getenv("READWISE_API_KEY")
last_fetch_time = datetime.datetime.now() - datetime.timedelta(days=7)
timestamp = last_fetch_time.isoformat()
documents = loader.load_data(updated_after=timestamp)
index = GPTSimpleVectorIndex(documents)

index.query("What has Elon Musk done this time?")
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
