# Gmail OpenAI Agent Pack

Create an OpenAI agent pre-loaded with a tool to interact with Gmail. The tool used is the [Gmail LlamaHub tool](https://llamahub.ai/l/tools-gmail).

## Usage

```
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
GmailOpenAIAgentPack = download_llama_pack("GmailOpenAIAgentPack")

gmail_agent_pack = GmailOpenAIAgentPack()

# Use the agent
agent = gmail_agent_pack.agent
response = agent.chat("What is my most recent email?")

# Use the tool spec in another agent
from llama_index.agents import ReActAgent
tool_spec = gmail_agent_pack.tool_spec
agent = ReActAgent.from_tools(tool_spec.to_tool_lost())
```
