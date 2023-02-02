# GPT Index Loader Hub

This is a simple library of all the data loaders / readers that have been created by the community in GPT Index. The goal is to make it extremely easy to connect large language models to a large variety of knowledge sources. These are general-purpose utilities that can be used in [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) (e.g. when building a index), [LangChain](https://github.com/hwchase17/langchain) (e.g. when building different tools an agent can use), and more. For example, there are loaders to parse Google Docs, PDF files, Powerpoints, and many more. Note that because the loaders produce the same types of Documents, you can easily use them together in the same index.

## Usage

These general-purpose loaders are designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. For example, see the code snippets below using the Google Docs Loader.

### GPT Index

```python
from loader_hub import GoogleDocsReader
from gpt_index import GPTSimpleVectorIndex

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTSimpleVectorIndex(documents)
index.query('Where did the author go to school?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from loader_hub import GoogleDocsReader
from gpt_index import GPTSimpleVectorIndex
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTSimpleVectorIndex(documents)

tools = [
    Tool(
        name="Google Doc Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about the Google Documents.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="Where did the author go to school?")
```

## How to add a loader

Adding a loader simply requires forking this repo and making a Pull Request. The Loader Hub website will update automatically. However, please keep in the mind the following policies when making your PR.

### Step 1: Create a new directory

In this directory, create a new directory for your new loader. It can be nested within another, but name it something unique because the name of the directory will become the identifier for your loader (e.g. `google_docs`).

### Step 2: Fill the directory

Inside your new directory, create a `__init__.py` file, which can be empty. Next, put your loader implementation into the `base.py` file. Finally, create a `README.md` that mirrors that of the existing ones. It should have a summary of what your loader does, its inputs, and how its used in the context of GPT Index and LangChain.

### Step 3: Add your loader to the package

Finally, add your loader to the `__init__.py` file in this directory so that it may be imported and used by others. As is exemplified by the current file, import your loader directly from the `base.py` file that it's in. You may add your name as a comment on the same row to denote that you are the author.
