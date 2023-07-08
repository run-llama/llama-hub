"""Simple CSV reader.

A parser for tabular data files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class SimpleCSVReader(BaseReader):
    """CSV parser.

    Args:
        encoding (str): Encoding used to open the file.
            utf-8 by default.
        concat_rows (bool): whether to concatenate all rows into one document.
            If set to False, a Document will be created for each row.
            True by default.

    """

    def __init__(
        self, *args: Any, concat_rows: bool = True, encoding: str = "utf-8", **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._concat_rows = concat_rows
        self._encoding = encoding

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import csv

        text_list = []
        with open(file, "r", encoding=self._encoding) as fp:
            csv_reader = csv.reader(fp)
            for row in csv_reader:
                text_list.append(", ".join(row))
        if self._concat_rows:
            return [Document(text="\n".join(text_list), extra_info=extra_info or {})]
        else:
            return [
                Document(text=text, extra_info=extra_info or {}) for text in text_list
            ]
