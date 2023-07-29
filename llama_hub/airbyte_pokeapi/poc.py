from airbyte_embed_cdk.tools import parse_json

from base import AirbytePokeApiReader, AirbytePokeApiContainerReader


def main():
    config = parse_json('{ "pokemon_name": "ditto" }')

    # using package
    reader = AirbytePokeApiReader(config=config)
    print(reader.load_data('pokemon'))

    # using image
    reader = AirbytePokeApiContainerReader(config=config)
    print(reader.load_data('pokemon'))


if __name__ == "__main__":
    main()
