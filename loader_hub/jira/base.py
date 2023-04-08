from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

class JiraReader(BaseReader):
    """Jira reader. Reads data from Jira issues from passed query.

    Args:
        email (str): Jira email.
        api_token (str): Jira API token.
        server_url (str): Jira server url.
    """

    def __init__(self, email: str, api_token: str, server_url: str) -> None:

        from jira import JIRA

        self.jira = JIRA(
            basic_auth=(email, api_token),
            server=f'https://{server_url}'
        )

    def load_data(self, query: str) -> List[Document]:
        relevant_issues = self.jira.search_issues(query)

        issues = []

        for issue in relevant_issues:
            assignee = ''
            reporter = ''
            epic = ''

            if issue.fields.assignee:
              assignee = issue.fields.assignee.displayName

            if issue.fields.reporter:
              reporter = issue.fields.reporter.displayName

            if issue.raw['fields']['customfield_10009']['showField']:
              epic = issue.raw['fields']['customfield_10009']['data']['summary']

            issues.append(
                Document(
                    issue.fields.summary + " " + issue.fields.description,
                    extra_info={
                      'id': issue.id,
                      'title': issue.fields.summary,
                      'url': issue.permalink(),
                      'created_at': issue.fields.created,
                      'updated_at': issue.fields.updated,
                      'labels': issue.fields.labels,
                      'status': issue.fields.status.name,
                      'assignee': assignee,
                      'reporter': reporter,
                      'project': issue.fields.project.name,
                      'issue_type': issue.fields.issuetype.name,
                      'priority': issue.fields.priority.name,
                      'epic': epic
                    }
                )
            )

        return issues
