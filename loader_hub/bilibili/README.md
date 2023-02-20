# Bilibili Transcript Loader

This loader utilizes the `bilibili_api` to fetch the text transcript from Bilibili, one of the most beloved long-form video sites in China. 			

With this BilibiliTranscriptReader, users can easily obtain the transcript of their desired video content on the platform.

## Usage

To use this loader, you need to pass in an array of Bilibili video links.

```python
from gpt_index import download_loader

BilibiliTranscriptReader= download_loader("BilibiliTranscriptReader")
loader = BilibiliTranscriptReader()
documents = loader.load_data(video_urls=['https://www.bilibili.com/video/BV1yx411L73B/'])
```


This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
