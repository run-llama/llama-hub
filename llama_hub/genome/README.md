# NCBI genome annotation Loader

This loader fetches the genome annotation from NCBI using the nuccore database through Entrez class of Biopython.

## Usage

To use this loader, simply pass a species name and email to `load_data`:

```python
from llama_hub.genome import GenomeAnnotationReader

species = 'Homo sapiens'
email = 'your_email@example.com'

loader = GenomeAnnotationReader()
documents = loader.load_data(
    email = email,
    species = species
)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
