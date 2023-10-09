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
            for json_object in data:
                if self.levels_back is None:
                    json_output = json.dumps(json_object, indent=0)
                    lines = json_output.split("\n")
                    useful_lines = [
                        line for line in lines if not re.match(r"^[{}\\[\\],]*$", line)
                    ]
                    documents.append(
                        Document(
                            text="\n".join(useful_lines), extra_info=extra_info or {}
                        )
                    )
                elif self.levels_back is not None:
                    lines = [*_depth_first_yield(json_object, self.levels_back, [])]
                    documents.append(
                        Document(text="\n".join(lines), extra_info=extra_info or {})
                    )
            return documents
