"""Json Data Reader."""

import json
import re
from typing import Dict, Generator, List, Union
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


class JSONDataReader(BaseReader):
    """Json Data reader.

    Reads in Json Data.

    Args:
        data(Union[str, Dict]): Json data to read. Can be either a JSON
            string or dictionary.

    """

    def __init__(self) -> None:
        """Initialize with arguments."""
        super().__init__()

    def load_data(self, input_data: Union[str, Dict]) -> List[Document]:
        """Load data from the input file."""
        if isinstance(input_data, str):
            data = json.loads(input_data)
        else:
            data = input_data
        json_output = json.dumps(data, indent=0)
        lines = json_output.split("\n")
        useful_lines = [line for line in lines if not re.match(r"^[{}\[\],]*$", line)]
        return [Document(text="\n".join(useful_lines))]
