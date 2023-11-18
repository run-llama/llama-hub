<center>
    <p style="text-align:center">
        <img alt="phoenix logo" src="https://storage.googleapis.com/arize-assets/phoenix/assets/phoenix-logo-light.svg" width="200"/>
        <br>
        <a href="https://docs.arize.com/phoenix/">Docs</a>
        |
        <a href="https://github.com/Arize-ai/phoenix">GitHub</a>
        |
        <a href="https://join.slack.com/t/arize-ai/shared_invite/zt-1px8dcmlf-fmThhDFD_V_48oU7ALan4Q">Community</a>
    </p>
</center>
<h1 align="center">Arize-Phoenix LlamaPack</h1>

This LlamaPack instruments your LlamaIndex application for LLM application tracing with [Phoenix](https://github.com/Arize-ai/phoenix), an open-source LLM observability product from [Arize AI](https://arize.com/).

## Install and Import Dependencies

Install dependencies.


```python
!pip install "arize-phoenix[llama-index]" llama-hub html2text
```

Import libraries.


```python
import getpass
import os

from llama_hub.llama_packs.arize_phoenix_query_engine import ArizePhoenixQueryEnginePack
from llama_index.node_parser import SentenceSplitter
from llama_index.readers import SimpleWebPageReader
from tqdm.auto import tqdm
```

This LlamaPack builds an index over a list of input nodes using the OpenAI API. Configure your OpenAI API key.


```python
if not (openai_api_key := os.getenv("OPENAI_API_KEY")):
    openai_api_key = getpass("🔑 Enter your OpenAI API key: ")
os.environ["OPENAI_API_KEY"] = openai_api_key
```

Parse your documents into a list of nodes. In this example, use nodes from a Paul Graham essay as input.


```python
documents = SimpleWebPageReader().load_data(
    [
        "http://raw.githubusercontent.com/jerryjliu/llama_index/main/examples/paul_graham_essay/data/paul_graham_essay.txt"
    ]
)
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)
```

Define your LlamaPack.


```python
phoenix_pack = ArizePhoenixQueryEnginePack(nodes=nodes)
```

Run a set of queries via the pack's `run` method, which delegates to the underlying query engine.


```python
queries = [
    "What did Paul Graham do growing up?",
    "When and how did Paul Graham's mother die?",
    "What, in Paul Graham's opinion, is the most distinctive thing about YC?",
    "When and how did Paul Graham meet Jessica Livingston?",
    "What is Bel, and when and where was it written?",
]
for query in tqdm(queries):
    print("Query")
    print("=====")
    print(query)
    print()
    response = phoenix_pack.run(query)
    print("Response")
    print("========")
    print(response)
    print()
```

View your trace data in the Phoenix UI.


```python
phoenix_session_url = phoenix_pack.get_modules()["session_url"]
print(f"Open the Phoenix UI to view your trace data: {phoenix_session_url}")
```

You can access the internals of the LlamaPack, including your Phoenix session and your query engine, via the `get_modules` method.


```python
phoenix_pack.get_modules()
```

Check out the [Phoenix documentation](https://docs.arize.com/phoenix/) for more information!
