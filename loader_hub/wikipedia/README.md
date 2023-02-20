# Wikipedia Loader

This loader fetches the text from Wikipedia articles using the `wikipedia` Python package. The inputs may be page titles or keywords that uniquely identify a Wikipedia page. In its current form, this loader only extracts text and ignores images, tables, etc.

## Usage

To use this loader, you need to pass in an array of Wikipedia pages.

```python
from llama_index import download_loader

WikipediaReader = download_loader("WikipediaReader")

loader = WikipediaReader()
documents = loader.load_data(pages=['Berlin', 'Rome', 'Tokyo', 'Canberra', 'Santiago'])
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
