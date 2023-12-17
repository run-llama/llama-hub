# LlamaHub 🦙

**Original creator**: Jesse Zhang (GH: [emptycrown](https://github.com/emptycrown), Twitter: [@thejessezhang](https://twitter.com/thejessezhang)), who courteously donated the repo to LlamaIndex!

> 👥 **Contributing**
> 
> Interested in contributing? Skip over to our [Contribution Section](https://github.com/run-llama/llama-hub#how-to-add-a-loadertoolllama-pack) below for more details.

This is a simple library of all the data loaders / readers / tools / llama-packs / llama-datasets that have been created by the community. The goal is to make it extremely easy to connect large language models to a large variety of knowledge sources. These are general-purpose utilities that are meant to be used in [LlamaIndex](https://github.com/run-llama/llama_index), [LangChain](https://github.com/hwchase17/langchain) and more!.

Loaders and readers allow you to easily ingest data for search and retrieval by a large language model, while tools allow the models to both read and write to third party data services and sources. Ultimately, this allows you to create your own customized data agent to intelligently work with you and your data to unlock the full capability of next level large language models.

For a variety of examples of data agents, see the [notebooks directory](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks). You can find example Jupyter notebooks for creating data agents that can load and parse data from Google Docs, SQL Databases, Notion, and Slack, and also manage your Google Calendar, and Gmail inbox, or read and use OpenAPI specs. 

For an easier way to browse the integrations available, check out the website here: https://llamahub.ai/.

<img width="1465" alt="Screenshot 2023-07-17 at 6 12 32 PM" src="https://github.com/ajhofmann/llama-hub/assets/10040285/5e344de4-4aca-4f6c-9944-46c00baa5eb2">

## Usage (Use `llama-hub` as PyPI package)
These general-purpose loaders are designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/llama_index) and/or subsequently used in [LangChain](https://github.com/hwchase17/langchain). 

### Installation
```
pip install llama-hub
```

### LlamaIndex

```python
from llama_index import VectorStoreIndex
from llama_hub.google_docs import GoogleDocsReader

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = VectorStoreIndex.from_documents(documents)
index.query('Where did the author go to school?')
```

### LlamaIndex Data Agent

```python
from llama_index.agent import OpenAIAgent
import openai
openai.api_key = 'sk-api-key'

from llama_hub.tools.google_calendar import GoogleCalendarToolSpec
tool_spec = GoogleCalendarToolSpec()

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())
agent.chat('what is the first thing on my calendar today')
agent.chat("Please create an event for tomorrow at 4pm to review pull requests")
```

For a variety of examples of creating and using data agents, see the [notebooks directory](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks).

### LangChain

Note: Make sure you change the description of the `Tool` to match your use case.

```python
from llama_index import VectorStoreIndex
from llama_hub.google_docs import GoogleDocsReader
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
from llama_index import VectorStoreIndex, download_loader

GoogleDocsReader = download_loader('GoogleDocsReader')

gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = VectorStoreIndex.from_documents(documents)
index.query('Where did the author go to school?')

```

## Llama-Pack Usage

Llama-packs can be downloaded using the `llamaindex-cli` tool that comes with `llama-index`:

```bash
llamaindex-cli download-llamapack ZephyrQueryEnginePack --download-dir ./zephyr_pack
```

Or with the `download_llama_pack` function directly:

```python
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
LlavaCompletionPack = download_llama_pack(
  "LlavaCompletionPack", "./llava_pack"
)
```

## Llama-Dataset Usage

The primary use of llama-dataset is for evaluating the performance of a RAG system.
In particular, it serves as a new test set (in traditional machine learning speak)
for one to build a RAG over, predict on, and subsequently perform evaluations
comparing the predicted response versus the reference response. To perform the
evaluation, the recommended usage pattern involves the application of the
`RagEvaluatorPack`. We recommend reading the [docs](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/root.html) for the "Evaluation" module for
more information.

```python
from llama_index.llama_dataset import download_llama_dataset
from llama_index.llama_pack import download_llama_pack
from llama_index import VectorStoreIndex

# download and install dependencies for benchmark dataset
rag_dataset, documents = download_llama_dataset(
  "PaulGrahamEssayDataset", "./data"
)

# build basic RAG system
index = VectorStoreIndex.from_documents(documents=documents)
query_engine = VectorStoreIndex.as_query_engine()

# evaluate using the RagEvaluatorPack
RagEvaluatorPack = download_llama_pack(
  "RagEvaluatorPack", "./rag_evaluator_pack"
)
rag_evaluator_pack = RagEvaluatorPack(
    rag_dataset=rag_dataset,
    query_engine=query_engine
)
benchmark_df = rag_evaluate_pack.run()  # async arun() supported as well
```

Llama-datasets can also be downloaded directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamadataset PaulGrahamEssayDataset --download-dir ./data
```

After downloading them from `llamaindex-cli`, you can inspect the dataset and
it source files (stored in a directory `/source_files`) then load them into python:

```python
from llama_index import SimpleDirectoryReader
from llama_index.llama_dataset import LabelledRagDataset

rag_dataset = LabelledRagDataset.from_json("./data/rag_dataset.json")
documents = SimpleDirectoryReader(
    input_dir="./data/source_files"
).load_data()
```

## How to add a loader/tool/llama-pack

Adding a loader/tool/llama-pack simply requires forking this repo and making a Pull Request. The Llama Hub website will update automatically when a new `llama-hub` release is made. However, please keep in mind the following guidelines when making your PR.

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

For loaders, create a new directory in `llama_hub`, for tools create a directory in `llama_hub/tools`, and for llama-packs create a directory in `llama_hub/llama_packs` It can be nested within another, but name it something unique because the name of the directory will become the identifier for your loader (e.g. `google_docs`). Inside your new directory, create a `__init__.py` file specifying the module's public interface with `__all__`, a `base.py` file which will contain your loader implementation, and, if needed, a `requirements.txt` file to list the package dependencies of your loader. Those packages will automatically be installed when your loader is used, so no need to worry about that anymore!

If you'd like, you can create the new directory and files by running the following script in the `llama_hub` directory. Just remember to put your dependencies into a `requirements.txt` file.

```
./add_loader.sh [NAME_OF_NEW_DIRECTORY]
```

### Step 2: Write your README

Inside your new directory, create a `README.md` that mirrors that of the existing ones. It should have a summary of what your loader or tool does, its inputs, and how it is used in the context of LlamaIndex and LangChain.

### Step 3: Add your loader to the library.json file

Finally, add your loader to the `llama_hub/library.json` file (or for the equivilant `library.json` under `tools/` or `llama-packs/`) so that it may be used by others. As is exemplified by the current file, add the class name of your loader or tool, along with its ID, author, etc. This file is referenced by the Llama Hub website and the download function within LlamaIndex.

### Step 4: Make a Pull Request!

Create a PR against the main branch. We typically review the PR within a day. To help expedite the process, it may be helpful to provide screenshots (either in the PR or in
the README directly) Show your data loader or tool in action!

## How to add a llama-dataset

Similar to the process of adding a tool / loader / llama-pack, adding a llama-
datset also requires forking this repo and making a Pull Request. However, for a
llama-dataset, only its metadata is checked into this repo. The actual dataset
and it's source files are instead checked into another Github repo, that is the
[llama-datasets repository](https://github.com/run-llama/llama-datasets). You will need to fork and clone that repo in addition to forking and cloning this one. 

Please ensure that when you clone the llama-datasets repository, that you set
the environment variable `GIT_LFS_SKIP_SMUDGE` prior to calling the `git clone`
command:

```bash
# for bash
GIT_LFS_SKIP_SMUDGE=1 git clone git@github.com:<your-github-user-name>/llama-datasets.git  # for ssh
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/<your-github-user-name>/llama-datasets.git  # for https

# for windows its done in two commands
set GIT_LFS_SKIP_SMUDGE=1  
git clone git@github.com:<your-github-user-name>/llama-datasets.git  # for ssh

set GIT_LFS_SKIP_SMUDGE=1  
git clone https://github.com/<your-github-user-name>/llama-datasets.git  # for https
```

The high-level steps for adding a llama-dataset are as follows:

1. Create a `LabelledRagDataset` (the initial class of llama-dataset made available on llama-hub)
2. Generate a baseline result with a RAG system of your own choosing on the
`LabelledRagDataset`
3. Prepare the dataset's metadata (`card.json` and `README.md`)
4. Submit a Pull Request to this repo to check in the metadata
5. Submit a Pull Request to the [llama-datasets repository](https://github.com/run-llama/llama-datasets) to check in the `LabelledRagDataset` and the source files

To assist with the submission process, we have prepared a [submission template
notebook](https://github.com/run-llama/llama_index/blob/main/docs/examples/llama_dataset/ragdataset_submission_template.ipynb) that walks you through the above-listed steps. We highly recommend
that you use this template notebook.

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

### How can I get a verified badge on LlamaHub? 
We have just started offering badges to our contributors. At the moment, we're focused on our early adopters and official partners, but we're gradually opening up badge consideration to all submissions. If you're interested in being considered, please review the criteria below and if everything aligns, feel free to contact us via [community Discord](https://discord.gg/dGcwcsnxhU).

We are still refining our criteria but here are some aspects we consider:

**Quality**
- Code Quality illustrated by the use of coding standards and style guidelines.
- Code readability and proper documentation.

**Usability**
- Self-contained module with no external links or libraries, and it is easy to run.
- Module should not break any existing unit tests.

**Safety**
- Safety considerations, such as proper input validation, avoiding SQL injection, and secure handling of user data.

**Community Engagement & Feedback**
- The module's usefulness to the library's users as gauged by the number of likes, downloads, etc.
- Positive feedback from module users.
 
Note: 
* It's possible that we decide to award a badge to a subset of your submissions based on the above criteria. 
* Being a regular contributor doesn't guarantee a badge, we will still look at each submission individually. 

### Other questions?

Feel free to hop into the [community Discord](https://discord.gg/dGcwcsnxhU) or tag the official [Twitter account](https://twitter.com/llama_index)!
