from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

def safe_value(value):
    if isinstance(value, (str, int, float)):
        return value
    elif isinstance(value, list):
        # Convert lists to strings
        return ', '.join(map(str, value))
    elif value is None:
        # Replace None with a default string
        return ''
    else:
        # Convert other types to strings
        return str(value)
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
            # Iterates through only issues and not epics
            if 'parent' in (issue.raw['fields']):
                assignee = ''
                reporter = ''
                epic_key = ''
                epic_summary = ''
                epic_descripton = ''

                if issue.fields.assignee:
                    assignee = issue.fields.assignee.displayName

                if issue.fields.reporter:
                    reporter = issue.fields.reporter.displayName

                if issue.raw['fields']['parent']['key']:
                    epic_key = issue.raw['fields']['parent']['key']

                if issue.raw['fields']['parent']['fields']['summary']:
                    epic_summary = issue.raw['fields']['parent']['fields']['summary']

                if issue.raw['fields']['parent']['fields']['status']['description']:
                    epic_descripton = issue.raw['fields']['parent']['fields']['status']['description']

                issues.append(
                    Document(
                        f"{issue.fields.summary} \n {issue.fields.description}",
                        extra_info = {
                            'id': safe_value(issue.id),
                            'title': safe_value(issue.fields.summary),
                            'url': safe_value(issue.permalink()),
                            'created_at': safe_value(issue.fields.created),
                            'updated_at': safe_value(issue.fields.updated),
                            'labels': safe_value(issue.fields.labels),
                            'status': safe_value(issue.fields.status.name),
                            'assignee': safe_value(assignee),
                            'reporter': safe_value(reporter),
                            'project': safe_value(issue.fields.project.name),
                            'issue_type': safe_value(issue.fields.issuetype.name),
                            'priority': safe_value(issue.fields.priority.name),
                            'epic_key': safe_value(epic_key),
                            'epic_summary': safe_value(epic_summary),
                            'epic_description': safe_value(epic_descripton)}
                    )
                )

        return issues
