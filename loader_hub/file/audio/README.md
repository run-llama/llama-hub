# Audio File Loader

This loader uses OpenAI's Whisper model to transcribe the text of an audio file or the audio track of a video file. The file formats .mp3 and .mp4 are preferred. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

AudioTranscriber = download_loader("AudioTranscriber")

loader = AudioTranscriber()
documents = loader.load_data(file=Path('./podcast.mp3'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
