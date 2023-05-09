# Slack Loader

This loader fetches the text from a list of Slack channels. You will need to initialize the loader with your Slack API Token or have the `SLACK_BOT_TOKEN` environment variable set.

## Usage

To use this loader, you need to pass in a list of Slack channel ids.

```python
from llama_index import download_loader

SlackReader = download_loader("SlackReader")

loader = SlackReader('<Slack API Token>')
documents = loader.load_data(channel_ids=['[slack_channel_id1]', '[slack_channel_id2]'])
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
