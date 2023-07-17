"""Pandas Excel reader.

Pandas parser for .xlsx files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

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
        pandas_config: Optional[dict] = None,
        concat_rows: bool = True,
        row_joiner: str = "\n",
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._pandas_config = pandas_config or {}
        self._concat_rows = concat_rows
        self._row_joiner = row_joiner if row_joiner else "\n"

    def load_data(
        self,
        file: Path,
        include_sheetname: bool = False,
        sheet_name: Optional[Union[str, int]] = None,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse file and extract values from a specific column.

        Args:
            file (Path): The path to the Excel file to read.
            column_name (str): The name of the column to use when creating the Document objects.
        Returns:
            List[Document]: A list of`Document objects containing the values from the specified column in the Excel file.
        """
        import itertools

        import pandas as pd

        df = pd.read_excel(file, sheet_name=sheet_name, **self._pandas_config)

        keys = df.keys()

        df_sheets = []

        for key in keys:
            sheet = []
            if include_sheetname:
                sheet.append([key])
            sheet.extend(df[key].values.astype(str).tolist())
            df_sheets.append(sheet)

        text_list = list(
            itertools.chain.from_iterable(df_sheets)
        )  # flatten list of lists

        if self._concat_rows:
            return [
                Document(
                    text=(self._row_joiner).join(
                        self._row_joiner.join(sublist) for sublist in text_list
                    ),
                    extra_info=extra_info or {},
                )
            ]
        else:
            return [
                Document(text=text, extra_info=extra_info or {}) for text in text_list
            ]
