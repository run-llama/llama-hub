# Google Keep Loader

This loader takes in IDs of Google Keep and parses their text into `Note`s. You can extract a Google Keep's ID directly from its URL. For example, the ID of `https://docs.google.com/document/d/1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec/edit` is `1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec`.

As a prerequisite, you will need to register with Google and generate a `credentials.json` file in the directory where you run this loader. See [here](https://developers.google.com/workspace/guides/create-credentials) for instructions.

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

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleKeepReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTVectorStoreIndex.from_documents(documents)
index.query('Where did the author go to school?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from llama_index import GPTVectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

GoogleKeepReader = download_loader('GoogleKeepReader')

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTVectorStoreIndex.from_documents(documents)

tools = [
    Tool(
        name="Google Doc Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about the Google Keep Notes.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="Where did the author go to school?")
```
