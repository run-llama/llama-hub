"""Json Data Reader."""

import json
import re
from typing import Dict, Generator, List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

def _depth_first_yield(json_data: Dict, path: List[str]) -> Generator[str, None, None]:
    """Do depth first yield of all of the leaf nodes of a JSON.

    Combines keys in the JSON tree using spaces.

    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_path = path[:]
            new_path.append(key)
            yield from _depth_first_yield(value, new_path)
    elif isinstance(json_data, list):
        for _, value in enumerate(json_data):
            yield from _depth_first_yield(value, path)
    else:
        path.append(str(json_data))
        yield " ".join(path)


class JsonDataReader(BaseReader):
    """Json Data reader.

    Reads in Json Data.

    Args:
        data: Json data to read.

    """

    def __init__(self) -> None:
        """Initialize with arguments."""
        super().__init__()

    def load_data(self, data) -> List[Document]:
        if isinstance(data, str):
            data = json.loads(data)
        """Load data from the input file."""
        json_output = json.dumps(data, indent=0)
        lines = json_output.split("\n")
        useful_lines = [
            line for line in lines if not re.match(r"^[{}\[\],]*$", line)
        ]
        return [Document("\n".join(useful_lines))]
