"""Pandas Excel reader.

Pandas parser for .xlsx files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PandasExcelReader(BaseReader):
    r"""Pandas-based CSV parser.

    Parses CSVs using the separator detection from Pandas `read_csv`function.
    If special parameters are required, use the `pandas_config` dict.

    Args:

        pandas_config (dict): Options for the `pandas.read_excel` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
            for more information. Set to empty dict by default, this means defaults will be used.

    """

    def __init__(
        self,
        *args: Any,
        pandas_config: dict = {},
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._pandas_config = pandas_config

    def load_data(
        self, file: Path, column_name: str, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file and extract values from a specific column.

        Args:
            file (Path): The path to the Excel file to read.
            column_name (str): The name of the column to use when creating the Document objects.
        Returns:
            List[Document]: A list of`Document objects containing the values from the specified column in the Excel file.
        """
        import pandas as pd

        df = pd.read_excel(file, **self._pandas_config)

        text_list = df[column_name].astype(str).tolist()

        if self._concat_rows:
            return [Document((self._row_joiner).join(text_list), extra_info=extra_info)]
        else:
            return [Document(text, extra_info=extra_info) for text in text_list]
