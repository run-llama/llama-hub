"""JSON Reader."""

import json
import re
from pathlib import Path
from typing import Dict, Generator, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


def _depth_first_yield(
    json_data: Dict, levels_back: int, path: List[str]
) -> Generator[str, None, None]:
    """Do depth first yield of all of the leaf nodes of a JSON.

    Combines keys in the JSON tree using spaces.

    If levels_back is set to 0, prints all levels.

    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_path = path[:]
            new_path.append(key)
            yield from _depth_first_yield(value, levels_back, new_path)
    elif isinstance(json_data, list):
        for _, value in enumerate(json_data):
            yield from _depth_first_yield(value, levels_back, path)
    else:
        new_path = path[-levels_back:]
        new_path.append(str(json_data))
        yield " ".join(new_path)


class JSONReader(BaseReader):
    """JSON reader.

    Reads JSON documents with options to help suss out relationships between nodes.

    Args:
        levels_back (int): the number of levels to go back in the JSON tree, 0
        if you want all levels. If levels_back is None, then we just format the
        JSON and make each line an embedding

    """

    def __init__(self, levels_back: Optional[int] = None) -> None:
        """Initialize with arguments."""
        super().__init__()
        self.levels_back = levels_back

    def _parse_jsonobj_to_document(
        self, json_data_object: Dict, extra_info: Optional[Dict] = None
    ) -> Document:
        """Parse the json object into a Document.

        Args:
            json_data_object: The Json Object to be converted.
            extra_info (Optional[Dict]): Additional information. Default is None.

        Returns:
            Document: The document.
        """
        if self.levels_back is None:
            json_output = json.dumps(json_data_object, indent=0)
            lines = json_output.split("\n")
            useful_lines = [
                line for line in lines if not re.match(r"^[{}\\[\\],]*$", line)
            ]
            return Document(text="\n".join(useful_lines), extra_info=extra_info or {})

        else:
            lines = [*_depth_first_yield(json_data_object, self.levels_back, [])]
            return Document(text="\n".join(lines), extra_info=extra_info or {})

    def load_data(
        self,
        file: Path,
        is_jsonl: Optional[bool] = False,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Load data from the input file.

        Args:
            file (Path): Path to the input file.
            is_jsonl (Optional[bool]): If True, indicates that the file is in JSONL format. Defaults to False.
            extra_info (Optional[Dict]): Additional information. Default is None.

        Returns:
            List[Document]: List of documents.
        """
        if not isinstance(file, Path):
            file = Path(file)
        with open(file, "r") as f:
            data = []
            if is_jsonl:
                for line in f:
                    data.append(json.loads(line.strip()))
            else:
                data = json.load(f)
            documents = []

            # For a dictionary JSON object, pass the entire data to be parsed as document
            if isinstance(data, dict):
                documents.append(self._parse_jsonobj_to_document(data, extra_info))
            # For a List or Non-Dictionary JSON object loop through and pass each item
            else:
                for json_object in data:
                    documents.append(
                        self._parse_jsonobj_to_document(json_object, extra_info)
                    )

            return documents
