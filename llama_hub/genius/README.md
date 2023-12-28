# Genius Loader

This loader connects to the Genius API and loads lyrics, metadata, and album art into `Documents`.

As a prerequisite, you will need to register with [Genius API](https://genius.com/api-clients) and create an app in order to get a `client_id` and a `client_secret`. You should then set a `redirect_uri` for the app. The `redirect_uri` does not need to be functional. You should then generate an access token as an instantiator for the GeniusReader.

## Usage

Here's an example usage of the GeniusReader. It will retrieve songs that match specific lyrics. Acceptable agruments are lyrics (str): The lyric snippet you're looking for and will return List[Document]: A list of documents containing songs with those lyrics.

```python
from llama_index import download_loader

GeniusReader = download_loader('GeniusReader')

access_token = "your_generated_access_token"

loader = GeniusReader(access_token)
documents = loader.search_songs_by_lyrics("Imagine")
```

## Example

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### LlamaIndex

```python
from llama_index import VectorStoreIndex, download_loader

GeniusReader = download_loader('GeniusReader')

loader = GeniusReader()
documents = loader.load_data()
index = VectorStoreIndex.from_documents(documents)
index.query('What songs have the lyrics imagine in them?')
```
