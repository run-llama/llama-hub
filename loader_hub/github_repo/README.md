# Github Repository Loader

This loader takes in `owner`, `repo`, `branch`, `commit` and other optional parameters such as for filtering dicrectories or only allowing some files with given extensions etc. It then fetches all the contents of the GitHub repository.

As a prerequisite, you will need to generate a person access token. See [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for instructions.

## Usage

To use this loader, you simply need to pass in the `owner` and `repo` and either `branch` or `commit` for example, you can `owner = jerryjliu` and `repo = gpt_index` and also either branch or commit `branch = main` or `commit = a6c89159bf8e7086bea2f4305cff3f0a4102e370`

```python
import os

from llama_index import download_loader
download_loader("GithubRepositoryReader")

from modules.github_repo import GithubRepositoryReader, GithubClient

github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
loader = GithubRepositoryReader(
    github_client,
    owner =                  "jerryjliu",
    repo =                   "gpt_index",
    filter_directories =     (["gpt_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
    filter_file_extensions = ([".py"], GithubRepositoryReader.FilterType.INCLUDE),
    verbose =                True,
    concurrent_requests =    10,
)

docs_branch = loader.load_data(branch="main")
docs_commit = loader.load_data(commit="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

for doc in docs:
    print(doc.extra_info)
```

## Examples

This loader designed to be used as a way to load data into [Llama Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### Llama Index

```python
import pickle
import os

assert (
    os.getenv("OPENAI_API_KEY") is not None
), "Please set the OPENAI_API_KEY environment variable."

from llama_index import download_loader
download_loader("GithubRepositoryReader")

from modules.github_repo import GithubClient, GithubRepositoryReader

docs = None

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner =                  "jerryjliu",
        repo =                   "gpt_index",
        filter_directories =     (["gpt_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
        filter_file_extensions = ([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose =                True,
        concurrent_requests =    10,
    )

    docs = loader.load_data(branch="main")

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = GPTSimpleVectorIndex(docs)

index.query("Explain each index class?")
```
