"""Paged CSV reader.

A parser for tabular data files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PagedCSVReader(BaseReader):
    """Paged CSV parser.

    Displayed each row in an LLM-friendly format on a separate document.
    """

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import csv

        docs = []
        with open(file, "r") as fp:
            csv_reader = csv.DictReader(fp)  # type: ignore
            for row in csv_reader:
                docs.append(
                    Document(
                        "\n".join(f"{k.strip()}: {v.strip()}" for k, v in row.items()),
                        extra_info=extra_info,
                    )
                )
        return docs
