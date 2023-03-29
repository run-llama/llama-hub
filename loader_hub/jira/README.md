# JIRA Loader

The Jira loader returns a set of issues based on the query provided to the dataloader. The user intializes the reader with an email, API token and the URL of the server they wish to fetch issues from.

## Usage

Here's an example of how to use it

```python
from llama_index import download_loader
import os

JiraReader = download_reader('JiraReader')

reader = JiraReader(email=email, api_token=api_token, server_url="https://your-jira-server.com")
documents = reader.load_data(query='project = <your-project>')

```
