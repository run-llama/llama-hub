# Wikipedia Loader

This loader fetches the text from Wikipedia articles using the [`wikipedia` Python package][1].
The inputs may be page titles or keywords that uniquely identify a Wikipedia page.
In its current form, this loader only extracts text and ignores images, tables, etc.

## Usage

To use this loader, you need to pass in an array of Wikipedia pages.

```python
from llama_index import download_loader

WikipediaReader = download_loader("WikipediaReader")

loader = WikipediaReader()
documents = loader.load_data(pages=['Berlin', 'Rome', 'Tokyo', 'Canberra', 'Santiago'])
```

This loader is designed for loading data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index).

[1]: https://pypi.org/project/wikipedia/
