# Confluence Loader

This loader loads pages from a given Confluence cloud instance. The user needs to specify the base URL for a Confluence 
instance to initialize the ConfluenceReader - base URL needs to end with `/wiki`. The user can optionally specify 
OAuth 2.0 credentials to authenticate with the Confluence instance. If no credentials are specified, the loader will
look for `CONFLUENCE_API_TOKEN` or `CONFLUENCE_USERNAME`/`CONFLUENCE_PASSWORD` environment variables to proceed with basic authentication.

For more on authenticating using OAuth 2.0, checkout:
- https://atlassian-python-api.readthedocs.io/index.html
- https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/

User then specify a list of `page_ids` and/or `space_key` to load in the corresponding pages into Document objects, if 
both are specified the union of both sets will be returned. User can also specify a boolean `include_attachments` to 
include attachments, this is set to `False` by default, if set to `True` all attachments will be downloaded and 
ConfluenceReader will extract the text from the attachments and add it to the Document object. Currently supported attachment types are: PDF, PNG, JPEG/JPG, SVG, Word and Excel. 

Hint: `space_key` and `page_id` can both be found in the URL of a page in Confluence - https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>

## Usage

Here's an example usage of the ConfluenceReader.

```python
from llama_index import download_loader

ConfluenceReader = download_loader('ConfluenceReader')

token = {
    access_token: "<access_token>",
    token_type: "<token_type>"
}
oauth2_dict = {
    "client_id": "<client_id>",
    "token": token
}

base_url = "https://yoursite.atlassian.com/wiki"

page_ids = ["<page_id_1>", "<page_id_2>", "<page_id_3"]
space_key = "<space_key>"

reader = ConfluenceReader(base_url=base_url, oauth2=oauth2_dict)
documents = reader.load_data(space_key=space_key, page_ids=page_ids, include_attachments=True)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
