# Airbyte Pokeapi Loader

The Airbyte Pokeapi Loader allows you to access different Pokeapi objects.

## Usage

```python
from llama_index import download_loader
from llama_hub. import AirbyteSalesforceReader


reader = AirbyteSalesforceReader(...so many things...)
documents = reader.load_data(stream="Asset")
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

```
rm -rf .venv && virtualenv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

```
# To run poc:

```