from typing import List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

class AsanaReader(BaseReader):
    """Asana reader. Reads data from an Asana workspace.

    Args:
        asana_token (str): Asana token.
    """

    def __init__(self, asana_token: str) -> None:
        """Initialize Asana reader."""
        import asana

        self.client = asana.Client.access_token(asana_token)

    def load_data(self, id: str, id_type: str) -> List[Document]:
        """Load data from the workspace.

        Args:
            id (str): Workspace ID or Project ID based on id_type.
            id_type (str): Type of the ID, either "workspace" or "project".
        Returns:
            List[Document]: List of documents.
        """
        results = []

        if id_type == "workspace":
            workspace_id = id
            workspace_name = self.client.workspaces.find_by_id(workspace_id)['name']
            projects = self.client.projects.find_all({"workspace": workspace_id})
        elif id_type == "project":
            project_id = id
            projects = [self.client.projects.find_by_id(project_id)]
            workspace_name = projects[0]["workspace"]["name"]
        else:
            raise ValueError("id_type must be either 'workspace' or 'project'")

        for project in projects:
            tasks = self.client.tasks.find_all(
                {
                    "project": project["gid"],
                    "opt_fields": "name,notes,completed,completed_at,completed_by,assignee,followers",
                }
            )
            for task in tasks:
                stories = self.client.tasks.stories(task["gid"], opt_fields="type,text")
                comments = "\n".join(
                    [story["text"] for story in stories if story["type"] == "comment"]
                )

                # Get followers' names
                followers = [f.get('name', '') for f in task.get('followers', []) if f.get('name', '') != "Unknown"]

                results.append(
                    Document(
                        text=task.get("name", "") + " " + task.get("notes", "") + " " + comments,
                        extra_info={
                            "task_id": task.get("gid", ""),
                            "name": task.get("name", ""),
                            "assignee": (task.get("assignee") or {}).get("name", ""),
                            "completed_on": task.get("completed_at", ""),
                            "completed_by": (task.get("completed_by") or {}).get("name", ""),
                            "project_name": project.get("name", ""),
                            "workspace_name": workspace_name,
                            "followers": followers,
                        },
                    )
                )

        return results
