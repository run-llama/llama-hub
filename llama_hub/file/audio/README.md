# Audio File Loader

This loader uses OpenAI's Whisper model to transcribe the text of an audio file or the audio track of a video file. The file formats .mp3 and .mp4 are preferred. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you will need the `whisper` python package installed. You can do so with `pip install whisper`.

Then, simply pass a `Path` to a local file into `load_data`:

```python
from pathlib import Path
from llama_hub.file.audio import AudioTranscriber

loader = AudioTranscriber()
documents = loader.load_data(file=Path('./podcast.mp3'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
