# OpenDAL Loader

This loader parses any file via [OpenDAL](https://github.com/apache/incubator-opendal).

All files are temporarily downloaded locally and subsequently parsed with `SimpleDirectoryReader`. Hence, you may also specify a custom `file_extractor`, relying on any of the loaders in this library (or your own)!

## Usage

`OpendalReader` can read data from any supported storage services including `s3`, `azblob`, `gcs` and so on.

```python
from llama_index import download_loader

OpendalReader = download_loader("OpendalReader")

loader = OpendalReader(
    scheme="s3",
    bucket='bucket',
    path='path/to/data/',
)
documents = loader.load_data()
```

We also provide `Opendal[S3|Gcs|Azblob]Reader` for convenience.

---

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
