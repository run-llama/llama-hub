# S3 Loader

This loader parses any file stored on S3. When initializing `S3Reader`, you may pass in your [AWS Access Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html). If none are found, the loader assumes they are stored in `~/.aws/credentials`.

All files are temporarily downloaded locally and subsequently parsed with `SimpleDirectoryReader`. Hence, you may also specify a custom `file_extractor`, relying on any of the loaders in this library (or your own)!

> S3 loader is based on `OpendalReader`.

## Usage

```python
from llama_index import download_loader

OpendalS3Reader = download_loader("OpendalS3Reader")

loader = OpendalS3Reader(
    bucket='bucket',
    path='path/to/data/',
    access_key_id='[ACCESS_KEY_ID]',
    secret_access_key='[ACCESS_KEY_SECRET]',
)
documents = loader.load_data()
```

Note: if `access_key_id` or `secret_access_key` is not provided, this loader to try to load from env.

Possible arguments includes:

- `endpoint`: Specify the endpoint of s3 service.
- `region`: Specify the region of s3 service.

---

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
