# playgrounds_subgraph_connector

Playgrounds API is a service provided by [Playgrounds Analytics](https://playgrounds.network) to streamline interfacing with decentralized subgraphs (indexed blockchain datasets).

The `PlaygroundsSubgraphConnector` is a tool designed for LLM agents to seamlessly interface with and query subgraphs on The Graph's decentralized network via Playgrounds API.

This tool is specifically designed to be used alongside [Llama index](https://github.com/jerryjliu/llama_index) or [langchain](https://python.langchain.com/docs/modules/agents/tools/custom_tools)

- To learn more about Playgrounds API, please visit our website : https://playgrounds.network/
- Obtain you Playgrounds API Key and get started for free here: https://app.playgrounds.network/signup
- Find any Subgraph (dataset) you need here: https://thegraph.com/explorer

## Advantages of this tool:

- **Easy access to Decentralized Subgraphs (Datasets)**: No need for wallet or GRT management.
- **LLM x Blockchain data**: Develop Ai applications that leverage blockchain data seamlessly.

## Basic Usage:

To utilize the tool, simply initialize it with the appropriate `identifier` (Subgraph ID or Deployment ID) and `api_key`. Optionally, specify if you're using a deployment ID.

```python
import openai
from llama_index.agent import OpenAIAgent
from llama_hub.tools.playgrounds_subgraph_connector import PlaygroundsSubgraphConnectorToolSpec

def simple_test():
    """
    Run a simple test querying the financialsDailySnapshots from Uniswap V3 subgraph using OpenAIAgent and Playgrounds API.
    """
    # Set the OpenAI API key
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    
    # Initialize the tool specification with the subgraph's identifier and the Playgrounds API key
    connector_spec = PlaygroundsSubgraphConnectorToolSpec(
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER", 
        api_key="YOUR_PLAYGROUNDS_API_KEY", 
        use_deployment_id=False  # Set to True if using Deployment ID
    )
    
    # Setup agent with the tool
    agent = OpenAIAgent.from_tools(connector_spec.to_tool_list())
    
    # Make a query using the agent
    response = agent.chat(
        'query the financialsDailySnapshots for id, timestamp, totalValueLockedUSD, and dailyVolumeUSD. only give me the first 2 rows'
    )
    print(response)

if __name__ == "__main__":
    simple_test()

```

Visit here for more in-depth [Examples](https://github.com/Tachikoma000/playgrounds_subgraph_connector/blob/main/connector_agent_tool/examples.ipynb).

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama_index) 
and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. 


