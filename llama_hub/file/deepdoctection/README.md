# DeepDoctection Loader

This loader extracts the text from a local PDF file or scans using the [**deep**doctection](https://github.com/deepdoctection/deepdoctection) Python package, a library that 
performs doc extraction and document layout. Check the [demo](https://huggingface.co/spaces/deepdoctection/deepdoctection)
at Huggingface.

## Usage

To use this loader, you need to pass in a `Path` to a local PDF-file or to a directory with image scans. 

This setting extracts all text and creates for each page a `Document`:

```python
from pathlib import Path
from llama_index import download_loader

DeepDoctectionReader = download_loader("DeepDoctectionReader")

loader = DeepDoctectionReader()
documents = loader.load_data(file=Path('./article.pdf'))
```

Creating `Document`s for layout sections will return a split based on visual components.

```python
from pathlib import Path
from llama_index import download_loader

DeepDoctectionReader = download_loader("DeepDoctectionReader")

loader = DeepDoctectionReader(split_by_layout=True)
documents = loader.load_data(file=Path('./article.pdf'))
```

Metadata on page level or layout section level can be added. The setting below will add categories like title, text,
table and list to `Document`s metadata.

```python
from pathlib import Path
from llama_index import download_loader

DeepDoctectionReader = download_loader("DeepDoctectionReader")

loader = DeepDoctectionReader(split_by_layout=True,extra_info={"category_name"})
documents = loader.load_data(file=Path('./article.pdf'))
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in 
a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

## Customization

**Deep**doctection allows extensive customizing that affects the output subsequently. 
 - Choice of layout models
 - Selection of four text extraction tools (Pdfplumber and three OCR tools)
 - Text filtering based on layout sections

and many other settings.

E.g. if segmenting a table is not necessary you can disable the function:

```python
from pathlib import Path
from llama_index import download_loader

DeepDoctectionReader = download_loader("DeepDoctectionReader")

loader = DeepDoctectionReader(config_overwrite=['USE_TABLE_SEGMENTATION=False'])
documents = loader.load_data(file=Path('./article.pdf'))
```

Please check the [docs](https://deepdoctection.readthedocs.io/en/latest/tutorials/analyzer_configuration_notebook/) for
more details. 

And if you still need more flexibility, you can compose your own **deep**doctection pipeline.  

## Third party dependencies

The default installation will install the package with minimal dependencies. Tesseract is required and needs to be installed 
separately. If more features are required, consider a more comprehensive setup. Check the options [here](https://deepdoctection.readthedocs.io/en/latest/install/).