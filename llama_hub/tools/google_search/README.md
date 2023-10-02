# Google Search Tool

This tool connects to a Google account and allows an Agent to perform google searches 

You will need to provide an api key and engine id after setting up the resources in Google Console: https://developers.google.com/custom-search/v1/overview

## Usage

This tool has more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/google_search.ipynb) and [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/advanced_tools_usage.ipynb)

Here's an example usage of the GoogleSearchToolSpec.

```python
from llama_hub.tools.google_search.base import GoogleSearchToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = GoogleSearchToolSpec()

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat("Please create an event on june 15th, 2023 at 5pm for 1 hour and invite xyz@abc.com to discuss tax laws")
agent.chat('What is on my calendar for today?')
```

`google_search`: Use the provided google search engine to explore the web

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

