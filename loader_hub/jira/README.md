# JIRA Loader

The Jira loader returns a set of issues based on the query provided to the dataloader.
We can follow to methods to initialize the loader-
1- basic_auth -> this takes a dict with the following keys
`basic_auth:{
"email": "email",
"api_token": "token",
"server_url": "server_url"
}`
2- Oauth2 -> this takes a dict with the following keys
`oauth:{
"cloud_id": "cloud_id",
"api_token": "token"
}`

You can follow this link for more information regarding Oauth2 -> https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/

## Usage

Here's an example of how to use it

```python
from llama_index import download_loader
import os

JiraReader = download_reader('JiraReader')

reader = JiraReader(email=email, api_token=api_token, server_url="https://your-jira-server.com")
documents = reader.load_data(query='project = <your-project>')

```
