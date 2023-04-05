# Audio File Loader

This loader uses OpenAI's Whisper model to transcribe the text of an audio file or the audio track of a video file. The file formats .mp3 and .mp4 are preferred. A single local file is passed in each time you call `load_data`.

You can directly use OpenAI's Whisper by setting `model_type` to `openai_whisper` or indirectly via Gladia OpenAI's Whisper by setting `model_type` to `openai_gladia_whisper` where the response time is usually less.
## Usage

To use this loader, you need to pass in a `Path` to a local file.

If you are using `openai_gladia_whisper`, please check following parameters on [Gladia](https://www.gladia.io/) before proceeding further.

1. gladia_api_key
2. diarization_max_speakers
3. language
4. language_behaviour
5. target_translation_language
6. transcription_hint

You need to signup on [Gladia](https://www.gladia.io/) to get `API-KEY`

```python
from pathlib import Path
from llama_index import download_loader

AudioTranscriber = download_loader("AudioTranscriber")

loader = AudioTranscriber()
documents = loader.load_data(file=Path('./podcast.mp3'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
