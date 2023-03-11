# Pandas Excel Loader

This loader extracts the text from a column of a local .xlsx file using the `pandas` Python package. A single local file is passed in each time you call `load_data`.

## Usage

To use this loader, you need to pass in a `Path` to a local file, along with a `column_name` from where to extract data.


```python
from pathlib import Path
from llama_index import download_loader

PandasExcelReader = download_loader("PandasExcelReader")

loader = PandasExcelReader()
documents = loader.load_data(file=Path('./data.xlsx'), column_name="text_column",pandas_config={"sheet_name":"Sheet1"})
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
