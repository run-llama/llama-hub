from airbyte_embed_cdk.tools import parse_json
from config import PokeApiConfig

from llama_hub.airbyte_pokeapi import AirbytePokeApiReader, AirbytePokeApiContainerReader


def main():
    config = parse_json('{ "pokemon_name": "ditto" }')

    # using package
    reader = AirbytePokeApiReader(config=config)
    print(reader.load_data('pokemon'))

    # using package & config object
    config = PokeApiConfig(pokemon_name="ditto")
    reader = AirbytePokeApiReader(config=config)
    print(reader.load_data('pokemon'))

    # show all available streams
    print(reader.available_streams())

    # using image
    reader = AirbytePokeApiContainerReader(config=config)
    print(reader.load_data('pokemon'))

    # using image & config object
    config = PokeApiConfig(pokemon_name="ditto")
    reader = AirbytePokeApiContainerReader(config=config)
    print(reader.load_data('pokemon'))

    # use specific image version
    reader = AirbytePokeApiContainerReader(config=config, version="0.1.5-dev.819dd97d48")
    print(reader.load_data('pokemon'))


if __name__ == "__main__":
    main()
