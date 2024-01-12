# Github Repository Loader

This loader takes in `owner`, `repo`, `branch`, `commit_sha` and other optional parameters such as for filtering dicrectories or only allowing some files with given extensions etc. It then fetches all the contents of the GitHub repository.

As a prerequisite, you will need to generate a "classic" personal access token with the `repo` and `read:org` scopes. See [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for instructions.

## Usage

To use this loader, you simply need to pass in the `owner` and `repo` and either `branch` or `commit_sha` for example, you can `owner = jerryjliu` and `repo = llama_index` and also either branch or commit `branch = main` or `commit_sha = a6c89159bf8e7086bea2f4305cff3f0a4102e370`.

```shell
export GITHUB_TOKEN='...'
```

```python
import os

from llama_index import download_loader
download_loader("GithubRepositoryReader")

from llama_hub.github_repo import GithubRepositoryReader, GithubClient

github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
loader = GithubRepositoryReader(
    github_client,
    owner =                  "jerryjliu",
    repo =                   "llama_index",
    filter_directories =     (["llama_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
    filter_file_extensions = ([".py"], GithubRepositoryReader.FilterType.INCLUDE),
    verbose =                True,
    concurrent_requests =    10,
)

docs = loader.load_data(branch="main")
# alternatively, load from a specific commit:
# docs = loader.load_data(commit_sha="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

for doc in docs:
    print(doc.extra_info)
```

### Azure DevOps

```bash
export AZURE_DEVOPS_BASEURL='...'
export AZURE_DEVOPS_USERNAME='...'
export AZURE_DEVOPS_PASSWORD='...'
```

```python
import os

from llama_index import download_loader
download_loader("GithubRepositoryReader")

from llama_hub.github_repo import GithubRepositoryReader, AzureDevOpsAdapter

# Example: https://dev.azure.com/ahmetkarapinar/testProject/_git/testProject/commit/08633d3844192a69ab5011c20201dba3aced0a41?refName=refs%2Fheads%2Fmaster
# 'ahmetkarapinar' is organization id
# 'testProject' is project id
# 'testProject' is repository id
# '08633d3844192a69ab5011c20201dba3aced0a41' commit sha
# 'master' branch name


azure_devops_adapter = AzureDevOpsAdapter(
    base_url=os.environ["AZURE_DEVOPS_BASE_URL"], # Ex. 'https://dev.azure.com/YOURORG'
    username=os.environ["AZURE_DEVOPS_USERNAME"],
    password=os.environ["AZURE_DEVOPS_PASSWORD"],
)

loader = GithubRepositoryReader(
    github_client = azure_devops_adapter,
    owner =                  "<your_project_id_goes_here>",
    repo =                   "<your_repository_id_goes_here>",
    filter_directories =     (["llama_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
    filter_file_extensions = ([".py"], GithubRepositoryReader.FilterType.INCLUDE),
    verbose =                True,
    concurrent_requests =    10,
)

docs = loader.load_data(branch="main")
# alternatively, load from a specific commit:
# docs = loader.load_data(commit_sha="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

for doc in docs:
    print(doc.extra_info)
```

## Examples

This loader designed to be used as a way to load data into [Llama Index](https://github.com/run-llama/llama_index/tree/main/llama_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### Llama Index

```shell
export OPENAI_API_KEY='...'
export GITHUB_TOKEN='...'
```

```python
import pickle
import os

from llama_index import download_loader, VectorStoreIndex
download_loader("GithubRepositoryReader")

from llama_hub.github_repo import GithubClient, GithubRepositoryReader

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner =                  "jerryjliu",
        repo =                   "llama_index",
        filter_directories =     (["llama_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
        filter_file_extensions = ([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose =                True,
        concurrent_requests =    10,
    )

    docs = loader.load_data(branch="main")

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()
response = query_engine.query("Explain each LlamaIndex class?")
print(response)
```
