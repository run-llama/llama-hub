# Preprocess Loader

[Preprocess](https://playground.preprocess.co) is an API service that splits any kind of document into optimal chunks of text for use in language model tasks.
Given documents in input `Preprocess` splits them into chunks of text that respect the layout and semantics of the original document.
We split the content by taking into account sections, paragraphs, lists, images, data tables, text tables, and slides, and following the content semantics for long texts.
We support PDFs, Microsoft Office documents (Word, PowerPoint, Excel), OpenOffice documents (ods, odt, odp), HTML content (web pages, articles, emails), and plain text.

This loader integrates with `Preprocess` API library to provide document conversion and chunking or to load already chunked files inside LlamaIndex.


## Requirements

Install the python `Preprocess` library if it is not already present:

```
pip install pypreprocess
```

## Usage

To use this loader, you need to pass the `Preprocess API Key`. 
When initializing `PreprocessReader`, you should pass your `API Key`, if you don't have it yet, please ask for one at [support@preprocess.co](mailto:support@preprocess.co). Without an `API Key`, the loader will raise an error.

If you want to chunk a file pass a valid filepath and the reader will start converting and chunking it.

```python
from llama_index import download_loader

PreprocessReader = download_loader("PreprocessReader")

#pass a filepath and get the chunks as Documents
loader = PreprocessReader(api_key='your-api-key', filepath='valid/path/to/file')
documents = loader.load_data()
```

Alternatively, if you want to load already chunked files you can do it via `process_id` passing it to the reader.
```python
from llama_index import download_loader

PreprocessReader = download_loader("PreprocessReader")

#pass a process_id obtained from a previous instance and get the chunks as Documents
loader = PreprocessReader(api_key='your-api-key', process_id='your-process-id')
documents = loader.load_data()
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

## Other info

`PreprocessReader` is based on `pypreprocess` from [Preprocess](https://github.com/preprocess-co/pypreprocess) library.
For more information or other integration needs please check the [documentation](https://github.com/preprocess-co/pypreprocess). 
