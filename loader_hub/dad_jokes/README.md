# DadJoke Loader

This loader fetches a joke from icanhazdadjoke.

## Usage

To use this loader, load it.

```python
from gpt_index import download_loader

DadJokeReader = download_loader("DadJokeReader")

loader = DadJokeReader()
documents = loader.load_data()
```

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
