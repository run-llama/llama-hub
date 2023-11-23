# Gradio Chat With Your LlamaIndex Agent

Create a LlamaIndex Agent (i.e., `BaseAgent`) and quickly chat with it using
this pack's Gradio Chatbot interface.

## Usage

You can download the pack to a `./gradio_agent_chat_pack` directory:

`sample.py`
```python
from llama_index.llama_packs import download_llama_pack
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_index.tools import FunctionTool


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)

# Works with any BaseAgent
agent = OpenAIAgent.from_tools(
    tools=[multiply_tool, add_tool],
    llm=OpenAI(model="gpt-3.5-turbo-1106"), 
    verbose=True  # thoughts are displayed in the Gradio interface!
)

# download and install dependencies
GradioAgentChatPack = download_llama_pack(
  "GradioAgentChatPack", "./gradio_agent_chat_pack"
)

gradio_agent_chat_pack = GradioAgentChatPack(agent=agent)

if __name__ == "__main__":
    gradio_agent_chat_pack.run()
```

From here, you can use the pack, or inspect and modify the pack in `./gradio_agent_chat_pack`.

The `run()` function is a light wrapper around `gr.demo.launch()`. To run the
app directly, use in your terminal:

```bash
export OPENAI_API_KEY="sk-..."
python ./gradio_agent_chat/sample.py
```
