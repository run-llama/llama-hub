# Youtube Channel Transcript Loader

This loader fetches the text transcript of all YouTube videos for a given YouTube channel.

It is based on the [Youtube Transcript Loader](https://llamahub.ai/l/youtube_transcript)

## Requirements

### Google API Credentials
To use this loader, you'll need Google API credentials.

This requires to have a Google Cloud Platform (GCP) project set up, enable the YouTube Data API v3, 
and obtain API credentials before proceeding.

1. **Set Up a GCP Project**:
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Create a new project or select an existing one. 
2. **Enable the YouTube Data API v3**:
    * In the Google Cloud Console, navigate to the [APIs & Services](https://console.cloud.google.com/apis) > [Library](https://console.cloud.google.com/apis/library) page. 
    * Search for "YouTube Data API v3" and enable it for your project.
3. **Create API Credentials**:
    * Still in the [APIs & Services](https://console.cloud.google.com/apis) section, navigate to [Credentials](https://console.cloud.google.com/apis/credentials).
    * Create API credentials by clicking on "Create Credentials" and selecting "API Key."

### Python packages

You will then need to install youtube_transcript_api and google-api-python-client

```
pip install youtube_transcript_api
pip install google-api-python-client
```


## Usage

You instantiate the loader and then pass the Google API key and YouTube channel id into `load_data`:

```python
from llama_hub.youtube_channel_transcript import YoutubeChannelTranscriptReader

loader = YoutubeChannelTranscriptReader()
documents = loader.load_data(google_api_key='YOUR_API_KEY', yt_channel_id='UCeRjipR4_SsCddq9VZ2AeKg')
```

If the channel contains any YouTube videos that do not have a transcript, it will ignore and log them as warning.


### Old Usage

Use this syntax for earlier versions of llama_index where llama_hub loaders where loaded via separate download process:

```python
from llama_index import download_loader

YoutubeChannelTranscriptReader = download_loader("YoutubeChannelTranscriptReader")

loader = YoutubeChannelTranscriptReader()
documents = loader.load_data(google_api_key='YOUR_API_KEY', yt_channel_id='UCeRjipR4_SsCddq9VZ2AeKg')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/run-llama/llama-hub/tree/main) for examples.
