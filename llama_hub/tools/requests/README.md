# Requests Tool

This tool provides the agent the ability to make HTTP requests. It can be combined with the OpenAPIToolSpec to interface with an OpenAPI server.


## Usage

This tool has more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/openapi_and_requests.ipynb)

Here's an example usage of the RequestsToolSpec.

```python
from llama_hub.tools.requests.base import RequestsToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = RequestsToolSpec(headers=headers)

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat("")
```

`get_request`: Performs a get request against the URL
`post_request`: Performs a post request against the URL
`patch_request`: Performs a patch request against the URL

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

