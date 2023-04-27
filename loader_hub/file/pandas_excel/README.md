# Pandas Excel Loader

This loader extracts the text from a column of a local .xlsx file using the `pandas` Python package. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file, along with a `sheet_name` from which sheet to extract data. You can set `sheet_name=None`, which means it will load all the sheets in the excel file. You can set `sheet_name="Data1` to load only the sheet named "Data1". Or you can set `sheet_name=0` to load the first sheet in the excel file.


```python
from pathlib import Path
from llama_index import download_loader

PandasExcelReader = download_loader("PandasExcelReader")

loader = PandasExcelReader()
documents = loader.load_data(file=Path('./data.xlsx'), sheet_name=None, pandas_config={"sheet_name":"Sheet1"})
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
