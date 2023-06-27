# GitHub Repository Issues Loader

A loader that fetches issues of a GitHub repository. It expects an `owner` and `repo` as parameters. 

To use it, a "classic" personal access token with the `read:org` and `read:project` scopes is required for public repos, for private repos you also need `repo`. 
See [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for instructions.

## Usage

To use this loader, pass an `owner` and `repo` for which the GitHub token has permissions. An example, for 
https://github.com/jerryjliu/llama_index, use `owner = jerryjliu` and `repo = llama_index`.

```shell
export GITHUB_TOKEN='...'
```

```python
import os

from llama_hub.github_repo_issues import GitHubRepositoryIssuesReader, GitHubIssuesClient

github_client = GitHubIssuesClient()
loader = GitHubRepositoryIssuesReader(
    github_client,
    owner =                  "jerryjliu",
    repo =                   "llama_index",
    verbose =                True,
)

docs = loader.load_data()

for doc in docs:
    print(doc.extra_info)
```

## Examples

This loader designed to be used as a way to load data into [Llama Index](https://github.com/jerryjliu/llama_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.
### Llama Index

```shell
export OPENAI_API_KEY='...'
export GITHUB_TOKEN='...'
```

```python
import pickle
import os

from llama_index import download_loader, VectorStoreIndex
from llama_hub.github_repo_issues import GitHubIssuesClient, GitHubRepositoryIssuesReader

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    loader = GitHubRepositoryIssuesReader(
        GitHubIssuesClient(),
        owner =                  "jerryjliu",
        repo =                   "llama_index",
        verbose =                True,
    )

    docs = loader.load_data()

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()
response = query_engine.query("Summarize issues that mention stream")
print(response)
```
