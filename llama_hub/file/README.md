# File Loader

This loader takes in a local directory containing files and extracts `Document`s from each of the files. By default, the loader will utilize the specialized loaders in this library to parse common file extensions (e.g. .pdf, .png, .docx, etc). You can optionally pass in your own custom loaders. Note: if no loader is found for a file extension, and the file extension is not in the list to skip, the file will be read directly.

## Usage

To use this loader, you simply need to instantiate the `SimpleDirectoryReader` class with a directory, along with other optional settings, such as whether to ignore hidden files. See the code for the complete list.

```python
from llama_hub.file.base import SimpleDirectoryReader

# other way of loading
# from llama_index import download_loader
# SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

loader = SimpleDirectoryReader('./data', recursive=True, exclude_hidden=True)
documents = loader.load_data()
```

## Examples

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### LlamaIndex

```python
from llama_hub.file.base import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex

# other way of loading
# from llama_index import download_loader
# SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

loader = SimpleDirectoryReader('./data', recursive=True, exclude_hidden=True)
documents = loader.load_data()
index = GPTVectorStoreIndex.from_documents(documents)
index.query('What are these files about?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from llama_hub.file.base import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

# other way of loading
# from llama_index import download_loader
# SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

loader = SimpleDirectoryReader('./data', recursive=True, exclude_hidden=True)
documents = loader.load_data()
index = GPTVectorStoreIndex.from_documents(documents)

tools = [
    Tool(
        name="Local Directory Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about the files in your local directory.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="What are these files about?")
```
