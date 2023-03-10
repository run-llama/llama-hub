# Gmail Loader

This loader seaches your Gmail account and parses the resulting emails into `Document`s. The search query can include normal query params, like `from: email@example.com label:inbox`.

As a prerequisite, you will need to register with Google and generate a `credentials.json` file in the directory where you run this loader. See [here](https://developers.google.com/workspace/guides/create-credentials) for instructions.

## Usage

To use this loader, you simply need to pass in a search query string.

```python
from llama_index import download_loader

GmailReader = download_loader('GmailReader')
loader = GmailReader(query="from: me label:inbox")
documents = loader.load_data()
```

## Examples

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### LlamaIndex

```python
from llama_index import GPTSimpleVectorIndex, download_loader

GoogleDocsReader = download_loader('GmailReader')
loader = GoogleDocsReader(query="from:me label:sent")

documents = loader.load_data()

index = GPTSimpleVectorIndex(documents)
index.query('What did I write about LLMs?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from llama_index import GPTSimpleVectorIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

GoogleDocsReader = download_loader('GmailReader')
loader = GoogleDocsReader(query="from:me label:sent")

documents = loader.load_data(document_ids=gdoc_ids)

index = GPTSimpleVectorIndex(documents)

tools = [
    Tool(
        name="Gmail Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about emails.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="What have I written about AGI?")
```
