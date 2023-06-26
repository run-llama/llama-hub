# JIRA Reader

The Jira loader returns a set of issues based on the query provided to the dataloader. The user intializes the reader with an email, API token and the URL of the server they wish to fetch issues from.

## Usage

Here's an example of how to use it

```python

from llama_hub.jira.base import JiraReader

reader = JiraReader(email=email, api_token=api_token, server_url="https://your-jira-server.com")
documents = reader.load_data(query='project = <your-project>')

```

Alternately, you can also use download_loader from llama_index

```python

from llama_index import download_loader
JiraReader = download_loader('JiraReader')

reader = JiraReader(email=email, api_token=api_token, server_url="https://your-jira-server.com")
documents = reader.load_data(query='project = <your-project>')

```
