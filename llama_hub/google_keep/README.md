# Google Keep Loader

This loader takes in IDs of Google Keep and parses their text into `Document`s. You can extract a Google Keep's ID directly from its URL. For example, the ID of `https://keep.google.com/u/6/#NOTE/1OySsaIrx_pvQaJJk3VPQfYQvSuxTQuPndEEGl7qvrhFaN8VnO4K8Bti0SL2YklU` is `1OySsaIrx_pvQaJJk3VPQfYQvSuxTQuPndEEGl7qvrhFaN8VnO4K8Bti0SL2YklU`.

As a prerequisite, you will need to register with Google and generate a `service_account.json` file in the directory where you run this loader. In addition, due to the limitation of current Google Keep API, your account has to be an Enterprise (Google Workspace) account. You will need to enable Domain-wide Delegation to enable the service account with Google Read APIs. See [here](https://issuetracker.google.com/issues/210500028) for details.

## Usage

To use this loader, you simply need to pass in an array of Google Keep IDs.

```python
from llama_index import download_loader

GoogleKeepReader = download_loader('GoogleKeepReader')

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleKeepReader()
documents = loader.load_data(document_ids=gdoc_ids)
```

## Examples

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### LlamaIndex

```python
from llama_index import GPTVectorStoreIndex, download_loader

GoogleKeepReader = download_loader('GoogleKeepReader')

gkeep_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleKeepReader()
notes = loader.load_data(note_ids=gkeep_ids)
index = GPTVectorStoreIndex.from_documents(notes)
index.query('What are my current TODOs?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from llama_index import GPTVectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

GoogleKeepReader = download_loader('GoogleKeepReader')

gkeep_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
notes = loader.load_data(note_ids=gkeep_ids)
index = GPTVectorStoreIndex.from_documents(notes)

tools = [
    Tool(
        name="Google Keep Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about the Google Keep Notes.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="What are my current TODOs?")
```
