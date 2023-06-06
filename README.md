# LlamaHub 🦙

This is a simple library of all the data loaders / readers that have been created by the community. The goal is to make it extremely easy to connect large language models to a large variety of knowledge sources. These are general-purpose utilities that are meant to be used in [LlamaIndex](https://github.com/jerryjliu/llama_index) (e.g. when building a index) and [LangChain](https://github.com/hwchase17/langchain) (e.g. when building different tools an agent can use). For example, there are loaders to parse Google Docs, SQL Databases, PDF files, PowerPoints, Notion, Slack, Obsidian, and many more. Note that because different loaders produce the same types of Documents, you can easily use them together in the same index.

Check out our website here: https://llamahub.ai/.

![Website screenshot](https://scrabble-dictionary.s3.us-west-2.amazonaws.com/Screen+Shot+2023-02-11+at+12.45.44+PM.png)

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
## Usage (Use `download_loader` from LlamaIndex)

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


## How to add a loader

Adding a loader simply requires forking this repo and making a Pull Request. The Loader Hub website will update automatically. However, please keep in the mind the following guidelines when making your PR.

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

In `llama_hub`, create a new directory for your new loader. It can be nested within another, but name it something unique because the name of the directory will become the identifier for your loader (e.g. `google_docs`). Inside your new directory, create a `__init__.py` file, which can be empty, a `base.py` file which will contain your loader implementation, and, if needed, a `requirements.txt` file to list the package dependencies of your loader. Those packages will automatically be installed when your loader is used, so no need to worry about that anymore!

If you'd like, you can create the new directory and files by running the following script in the `llama_hub` directory. Just remember to put your dependencies into a `requirements.txt` file.

```
./add_loader.sh [NAME_OF_NEW_DIRECTORY]
```

### Step 2: Write your README

Inside your new directory, create a `README.md` that mirrors that of the existing ones. It should have a summary of what your loader does, its inputs, and how its used in the context of LlamaIndex and LangChain.

### Step 3: Add your loader to the library.json file

Finally, add your loader to the `llama_hub/library.json` file so that it may be used by others. As is exemplified by the current file, add in the class name of your loader, along with its id, author, etc. This file is referenced by the Loader Hub website and the download function within LlamaIndex.

### Step 4: Make a Pull Request!

Create a PR against the main branch. We typically review the PR within a day. To help expedite the process, it may be helpful to provide screenshots (either in the PR or in
the README directly) showing your data loader in action!

## Running tests

```shell
python3.9 -m venv .venv
source .venv/bin/activate 
pip3 install -r test_requirements.txt

poetry run pytest tests 
```

## FAQ

### How do I test my loader before it's merged?

There is an argument called `loader_hub_url` in [`download_loader`](https://github.com/jerryjliu/llama_index/blob/main/llama_index/readers/download.py) that defaults to the main branch of this repo. You can set it to your branch or fork to test your new loader.

### Should I create a PR against LlamaHub or the LlamaIndex repo directly?

If you have a data loader PR, by default let's try to create it against LlamaHub! We will make exceptions in certain cases
(for instance, if we think the data loader should be core to the LlamaIndex repo).

For all other PR's relevant to LlamaIndex, let's create it directly against the [LlamaIndex repo](https://github.com/jerryjliu/llama_index).

### Other questions?

Feel free to hop into the [community Discord](https://discord.gg/dGcwcsnxhU) or tag the official [Twitter account](https://twitter.com/llama_index)!
