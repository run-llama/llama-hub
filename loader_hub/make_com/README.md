# Make Loader

The Make Loader offers a webhook wrapper that can take in a query response as an input.
**NOTE**: The Make Loader does not offer the ability to load in Documents. Currently,
it is designed so that you can plug in GPT Index Response objects into downstream Make workflows.

## Usage

Here's an example usage of the `MakeWrapper`.

```python
from gpt_index import download_loader
import os

MakeWrapper = download_loader('MakeWrapper')

# load index from disk
index = GPTSimpleVectorIndex.load_from_disk('../vector_indices/index_simple.json')

# query index
query_str = "What did the author do growing up?"
response = index.query(query_str, verbose=True)

# Send response to Make.com webhook
wrapper = MakeWrapper()
wrapper.pass_response_to_webhook(
    "<webhook_url>,
    response,
    query_str
)


```
