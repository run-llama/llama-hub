# Airbyte Pokeapi Loader

The Airbyte Pokeapi Loader allows you to access different Pokeapi objects.

## Usage

```python
from llama_hub.airbyte_pokeapi import AirbytePokeApiReader, AirbytePokeApiContainerReader
from airbyte_embed_cdk.tools import parse_json

config = parse_json('{ "pokemon_name": "ditto" }')

# using package
reader = AirbytePokeApiReader(config=config)
document = reader.load_data('pokemon')

# using image
reader = AirbytePokeApiContainerReader(config=config)
document = reader.load_data('pokemon')
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

## Field notes

```shell
rm -rf .venv && virtualenv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

```shell
# To run poc:
 PYTHONPATH=../.. python poc.py
```

```shell
# Generate config object
(
    rm -rf .genenv && virtualenv .genenv && . .genenv/bin/activate
    pip install datamodel-code-generator==0.17.1
    docker run --rm -it airbyte/source-pokeapi:0.1.5-dev.819dd97d48 spec | jq '.spec.connectionSpecification' > spec.json
    datamodel-codegen --input spec.json --input-file-type jsonschema --disable-timestamp --allow-extra-fields --class-name PokeApiConfig --output config.py
)
```
