# Shopify Tool

This tool acts as a custom app for Shopify stores, allowing the Agent to execute GraphQL queries to gather information or perform mutations against the Shopify store.

## Usage

This tool has more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/shopify.ipynb)

In particular, the tool is very effective when combined with a method of retriving data from the GraphQL schema defintion.

```python
from llama_hub.tools.shopify.base import ShopifyToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = ShopifyToolSpec('your-store.myshopify.com', '2023-04', 'your-api-key')

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat('What products are in my store?')
```

`run_graphql_query`: Executes a GraphQL query against the Shopify store

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
