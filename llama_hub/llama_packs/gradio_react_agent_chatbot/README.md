# Gradio ReActAgent Chatbot Pack

Create a ReActAgent Chatbot equipped with two LlamaHub tools, namely: 
[ArxivToolSpec](https://llamahub.ai/l/tools-arxiv) and Wikipedia tool and
[WikipediaToolSpec](https://llamahub.ai/l/tools-wikipedia).

<img src="gradio-react-agent.png" width="75%">

This pack's Gradio app is built using Gradio `Blocks`. User messages are submitted
via a `TextBox` Block, which are then handled by a LlamaIndex `ReActAgent` to generate a
response (calling required tools). The result is then sent to a `Chatbot` Block —
additionally the agent's thoughts are captured in an `HTML` Block.

## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack GradioReactAgentPack --download-dir ./gradio_react_agent_chatbot
```

You can then inspect the files at `./gradio_react_agent_chatbot` and use them as a template for your own project!

To run the app directly, use in your terminal:

```bash
python ./gradio_react_agent_pack/base.py
```
