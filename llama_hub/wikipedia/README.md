# Wikipedia Loader

This loader fetches the text from Wikipedia articles using the [`wikipedia` Python package][2].
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

This loader is designed for loading data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index)
and/or subsequently used as a Tool in a [LangChain](https://github.com/langchain-ai/langchain) Agent.
See [this LlamaIndex tutorial][1] for examples.

[1]: https://gpt-index.readthedocs.io/en/stable/examples/index_structs/knowledge_graph/KnowledgeGraphIndex_vs_VectorStoreIndex_vs_CustomIndex_combined.html#load-data-from-wikipedia
[2]: https://pypi.org/project/wikipedia/
