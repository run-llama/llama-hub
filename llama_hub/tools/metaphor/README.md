# Metaphor Tool

This tool connects to [Metaphor](https://metaphor.systems/) to allow easily retriving articles from the web on current topics. The articles can then be retrieved and processed by an agent.

As a prerequisite, you will need to register with Metaphor and [generate an API key](https://dashboard.metaphor.systems/overview)

## Usage

This tool has more a extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/metaphor.ipynb)

Here's an example usage of the MetaphorToolSpec.

```python
from llama_hub.tools.metaphor.base import MetaphorToolSpec
from llama_index.agent import OpenAIAgent

metaphor_tool = MetaphorToolSpec(
    api_key='your-key',
)
agent = OpenAIAgent.from_tools(metaphor_tool.to_tool_list())

agent.chat('Can you summarize the news published in the last month on superconductors')
```

`metaphor_search`: Search for a list of articles relating to a natural language query
`retrieve_documents`: Retrieve a list of documents returned from `metaphor_search`.
`find_similar`: Find similar documents to a given URL.
`current_date`: Utility for the Agent to get todays date

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

