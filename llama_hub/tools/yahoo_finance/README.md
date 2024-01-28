# Yahoo Finance Tool

This tool connects to Yahoo Finance and allows an Agent to access stock, news, and financial data of a company.

## Usage

Here's an example of how to use this tool:

```python
from llama_hub.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = YahooFinanceToolSpec()
agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat('What is the price of Apple stock?')
agent.chat('What is the latest news about Apple?')

```
The tools available are:
`stock_financials`: A tool that returns the financials of a company.
`stock_news`: A tool that returns the latest news about a company.
`stock_basic_info`: A tool that returns basic information about a company including price.
`stock_analyst_recommendations`: A tool that returns analyst recommendations for a company.

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.
