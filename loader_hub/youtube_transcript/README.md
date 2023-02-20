# Youtube Transcript Loader

This loader fetches the text transcript of Youtube videos using the `youtube_transcript_api` Python package.

## Usage

To use this loader, you need to pass in an array of Youtube links.

```python
from llama_index import download_loader

YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")

loader = YoutubeTranscriptReader()
documents = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=i3OYlaoj-BM'])
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
