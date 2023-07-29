from airbyte_embed_cdk.integrations.llama_index import container_airbyte_llamaindex_reader, cdk_airbyte_container_llamaindex_reader
from source_pokeapi import SourcePokeapi

AirbytePokeApiContainerReader = container_airbyte_llamaindex_reader(
    "airbyte/source-pokeapi",
    "0.1.5-dev.819dd97d48")

AirbytePokeApiReader = cdk_airbyte_container_llamaindex_reader(SourcePokeapi)
