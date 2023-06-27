from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


def safe_value_dict(dict_obj):
    for key, value in dict_obj.items():
        if isinstance(value, (str, int, float)):
            dict_obj[key] = value
        elif isinstance(value, list):
            # Convert lists to strings
            dict_obj[key] = ", ".join(map(str, value))
        elif value is None:
            # Replace None with a default string
            dict_obj[key] = ""
        else:
            # Convert other types to strings
            dict_obj[key] = str(value)
    return dict_obj


class JiraReader(BaseReader):
    """Jira reader. Reads data from Jira issues from passed query.

    Args:
        email (str): Jira email.
        api_token (str): Jira API token.
        server_url (str): Jira server url.
    """

    def __init__(self, email: str, api_token: str, server_url: str) -> None:

        from jira import JIRA

        self.jira = JIRA(basic_auth=(email, api_token), server=f"https://{server_url}")

    def load_data(self, query: str) -> List[Document]:
        relevant_issues = self.jira.search_issues(query)

        issues = []

        for issue in relevant_issues:
            # Iterates through only issues and not epics
            if "parent" in (issue.raw["fields"]):
                assignee = ""
                reporter = ""
                epic_key = ""
                epic_summary = ""
                epic_descripton = ""

                if issue.fields.assignee:
                    assignee = issue.fields.assignee.displayName

                if issue.fields.reporter:
                    reporter = issue.fields.reporter.displayName

                if issue.raw["fields"]["parent"]["key"]:
                    epic_key = issue.raw["fields"]["parent"]["key"]

                if issue.raw["fields"]["parent"]["fields"]["summary"]:
                    epic_summary = issue.raw["fields"]["parent"]["fields"]["summary"]

                if issue.raw["fields"]["parent"]["fields"]["status"]["description"]:
                    epic_descripton = issue.raw["fields"]["parent"]["fields"]["status"][
                        "description"
                    ]

                issues.append(
                    Document(
                        text=f"{issue.fields.summary} \n {issue.fields.description}",
                        extra_info=safe_value_dict(
                            {
                                "id": issue.id,
                                "title": issue.fields.summary,
                                "url": issue.permalink(),
                                "created_at": issue.fields.created,
                                "updated_at": issue.fields.updated,
                                "labels": issue.fields.labels,
                                "status": issue.fields.status.name,
                                "assignee": assignee,
                                "reporter": reporter,
                                "project": issue.fields.project.name,
                                "issue_type": issue.fields.issuetype.name,
                                "priority": issue.fields.priority.name,
                                "epic_key": epic_key,
                                "epic_summary": epic_summary,
                                "epic_description": epic_descripton,
                            }
                        ),
                    )
                )

        return issues
