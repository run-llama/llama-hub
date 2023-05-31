# Twitter Loader

This loader fetches the text from the Tweets of a list of Twitter users, using the `tweepy` Python package. You must initialize the loader with your Twitter API token, and then pass in the Twitter handles of the users whose Tweets you want to extract.

## Usage

To use this loader, you need to pass in an array of Twitter handles.

```python
from llama_index import download_loader

TwitterTweetReader = download_loader("TwitterTweetReader")

loader = TwitterTweetReader(bearer_token="[YOUR_TOKEN]")
documents = loader.load_data(twitterhandles=['elonmusk', 'taylorswift13', 'barackobama'])
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
