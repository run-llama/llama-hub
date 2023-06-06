# RDF Loader

This loader extracts triples from a local [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) file using the `rdflib` Python package. The loader currently supports the RDF and RDF Schema namespaces. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file.

```python
from pathlib import Path
from llama_index import download_loader

RDFReader = download_loader("RDFReader")

loader = RDFReader()
documents = loader.load_data(file=Path('./knowledge-graph.nt'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
