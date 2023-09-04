# Gmail Tool

This tool connects to a GMail account and allows an Agent to read emails, create and update drafts, and send emails.

As a prerequisite, you will need to register with Google and generate a `credentials.json` file in the directory where you run this loader. See [here](https://developers.google.com/workspace/guides/create-credentials) for instructions.

## Usage

This tool has more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/gmail.ipynb) and [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/advanced_tools_usage.ipynb)

Here's an example usage of the GmailToolSpec.

```python
from llama_hub.tools.gmail.base import GmailToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = GmailToolSpec()

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat('What is my most recent email')
agent.chat('Create a draft email about a new contract lead')
agent.chat('Update the draft to mention that we need a response by tuesday')
agent.chat('Send the email')
```

`load_data`: Load the most recent emails from your inbox
`search_messages`: Search your inbox for emails
`create_draft`: Create a new draft email
`update_draft`: Update a draft email
`get_draft`: Retreieve the content of a draft
`send_draft`: Send a draft

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

