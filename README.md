# LlamaHub 🦙

This is a simple library of all the data loaders / readers / tools that have been created by the community. The goal is to make it extremely easy to connect large language models to a large variety of knowledge sources. These are general-purpose utilities that are meant to be used in [LlamaIndex](https://github.com/jerryjliu/llama_index) and [LangChain](https://github.com/hwchase17/langchain).

Loaders and readers allow you to easily ingest data for search and retrieval by a large language models, while tools allow the models to both read and write to third party data services and sources. Ultimately, this allows you to create your own customized data agent to intelligently work with you and your data to unlock the full capaibility of next level large language models.

For a variety of examples on data agents, see the [notebooks directory](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks). You can find example Jupyter notebooks for creating data agents that can load and parse data from Google Docs, SQL Databases, Notion, Slack and also manage you Google Calendar, Gmail inbox, or read and use OpenAPI specs. 

For an easier way to browse the integrations available, checkout the website here: https://llamahub.ai/.

<img width="1465" alt="Screenshot 2023-07-17 at 6 12 32 PM" src="https://github.com/ajhofmann/llama-hub/assets/10040285/5e344de4-4aca-4f6c-9944-46c00baa5eb2">

## Usage (Use `llama-hub` as PyPI package)
These general-purpose loaders are designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/llama_index) and/or subsequently used in [LangChain](https://github.com/hwchase17/langchain). 

### Installation
```
pip install llama-hub
```

### LlamaIndex

```python
from llama_index import GPTVectorStoreIndex
from llama_hub.google_docs.base import GoogleDocsReader

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTVectorStoreIndex.from_documents(documents)
index.query('Where did the author go to school?')
```

### LlamaIndex Data Agent

```python
from llama_index.agent import OpenAIAgent
import openai
openai.api_key = 'sk-api-key'

from llama_hub.tools.google_calendar.base import GoogleCalendarToolSpec
tool_spec = GoogleCalendarToolSpec()

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())
agent.chat('what is the first thing on my calendar today')
agent.chat("Please create an event for tomorrow at 4pm to review pull requests")
```

For a variety of examples on creating and using data agents, see the [notebooks directory](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks).

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from llama_index import GPTVectorStoreIndex
from llama_hub.google_docs.base import GoogleDocsReader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# load documents
gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
langchain_documents = [d.to_langchain_format() for d in documents]

# initialize sample QA chain
llm = OpenAI(temperature=0)
qa_chain = load_qa_chain(llm)
question="<query here>"
answer = qa_chain.run(input_documents=langchain_documents, question=question)

```

## Loader Usage (Use `download_loader` from LlamaIndex)

You can also use the loaders with `download_loader` from LlamaIndex in a single line of code.

For example, see the code snippets below using the Google Docs Loader.

```python
from llama_index import GPTVectorStoreIndex, download_loader

GoogleDocsReader = download_loader('GoogleDocsReader')

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTVectorStoreIndex.from_documents(documents)
index.query('Where did the author go to school?')

```

## How to add a loader or tool

Adding a loader or tool simply requires forking this repo and making a Pull Request. The Llama Hub website will update automatically. However, please keep in the mind the following guidelines when making your PR.

### Step 0: Setup virtual environment, install Poetry and dependencies

Create a new Python virtual environment. The command below creates an environment in `.venv`,
and activates it:
```bash
python -m venv .venv
source .venv/bin/activate
```

if you are in windows, use the following to activate your virtual environment:

```bash
.venv\scripts\activate
```

Install poetry:

```bash
pip install poetry
```

Install the required dependencies (this will also install `llama_index`):

```bash
poetry install
```

This will create an editable install of `llama-hub` in your venv.


### Step 1: Create a new directory

For loaders, create a new directory in `llama_hub`, and for tools create a directory in `llama_hub/tools` It can be nested within another, but name it something unique because the name of the directory will become the identifier for your loader (e.g. `google_docs`). Inside your new directory, create a `__init__.py` file, which can be empty, a `base.py` file which will contain your loader implementation, and, if needed, a `requirements.txt` file to list the package dependencies of your loader. Those packages will automatically be installed when your loader is used, so no need to worry about that anymore!

If you'd like, you can create the new directory and files by running the following script in the `llama_hub` directory. Just remember to put your dependencies into a `requirements.txt` file.

```
./add_loader.sh [NAME_OF_NEW_DIRECTORY]
```

### Step 2: Write your README

Inside your new directory, create a `README.md` that mirrors that of the existing ones. It should have a summary of what your loader or tool does, its inputs, and how its used in the context of LlamaIndex and LangChain.

### Step 3: Add your loader to the library.json file

Finally, add your loader to the `llama_hub/library.json` file (for tools, add them to the `llama_hub/tools/library.json`) so that it may be used by others. As is exemplified by the current file, add in the class name of your loader or tool, along with its id, author, etc. This file is referenced by the Llama Hub website and the download function within LlamaIndex.

### Step 4: Make a Pull Request!

Create a PR against the main branch. We typically review the PR within a day. To help expedite the process, it may be helpful to provide screenshots (either in the PR or in
the README directly) showing your data loader or tool in action!

## Running tests

```shell
python3.9 -m venv .venv
source .venv/bin/activate 
pip3 install -r test_requirements.txt

poetry run pytest tests 
```

## Changelog

If you want to track the latest version updates / see which loaders are added to each release, take a look at our [full changelog here](https://github.com/emptycrown/llama-hub/blob/main/CHANGELOG.md)! 

## FAQ

### How do I test my loader before it's merged?

There is an argument called `loader_hub_url` in [`download_loader`](https://github.com/jerryjliu/llama_index/blob/main/llama_index/readers/download.py) that defaults to the main branch of this repo. You can set it to your branch or fork to test your new loader.

### Should I create a PR against LlamaHub or the LlamaIndex repo directly?

If you have a data loader PR, by default let's try to create it against LlamaHub! We will make exceptions in certain cases
(for instance, if we think the data loader should be core to the LlamaIndex repo).

For all other PR's relevant to LlamaIndex, let's create it directly against the [LlamaIndex repo](https://github.com/jerryjliu/llama_index).

### Other questions?

Feel free to hop into the [community Discord](https://discord.gg/dGcwcsnxhU) or tag the official [Twitter account](https://twitter.com/llama_index)!
