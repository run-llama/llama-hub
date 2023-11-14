"""LlamaHub utils."""

import importlib
import json
from pathlib import Path
from typing import Type

from llama_index.readers.base import BaseReader

LIBRARY_JSON_PATH = Path(__file__).parent / "library.json"


def import_loader(reader_str: str) -> Type[BaseReader]:
    """Import or download loader."""

    # read library json file
    with open(LIBRARY_JSON_PATH, "r") as json_file:
        json_dict = json.load(json_file)

    dir_name = str(json_dict[reader_str]["id"])

    fmt_dir_name = dir_name.replace("/", ".")
    module = importlib.import_module("llama_hub." + fmt_dir_name + ".base")
    reader_cls = getattr(module, reader_str)
    return reader_cls
