"""
Azure DevOps Client Adapter for BaseGithubClient.

This class is used to interact with Azure DevOps repositories. It uses the azure-devops package.
The implementation is merely a workaround to use the same code for Github and Azure DevOps.
"""

from typing import Any, Dict, List, Optional
from llama_hub.github_repo.github_client import (
    BaseGithubClient, 
    GitBlobResponseModel, 
    GitBranchResponseModel, 
    GitCommitResponseModel, 
    GitTreeResponseModel
)

from azure.devops.v7_0.git.git_client import GitClient
from azure.devops.v7_0.git.models import GitTreeRef
from azure.devops.v7_0.git.models import GitTreeEntryRef
from azure.devops.v7_0.git.models import GitBlobRef
from azure.devops.v7_0.git.models import GitCommit
from azure.devops.v7_0.git.models import GitBranchStats


class AzureDevOpsAdapter(BaseGithubClient):
    """
    Azure DevOps adapter.

    This class is used to interact with Azure DevOps repositories. It uses the azure-devops package.
    Each method is same as the corresponding method in BaseGithubClient. All of the Azure DevOps specific
    response models are converted to the corresponding Github response models.

    Args:
        - `base_url (str)`: Azure DevOps base url. Example: 'https://dev.azure.com/YOURORG'
        - `username (str)`: Azure DevOps username. You can leave this blank if you are using a PAT. ex: ''
        - `password (str)`: Azure DevOps password. Personal Access Token (PAT) is recommended.

    Raises:
        - `ImportError`: If azure-devops package is not installed.
        - `ValueError`: If base_url, username or password is not provided.
    """
    def __init__(self,
                 *args: Any, 
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        try:
            from azure.devops.connection import Connection
            from msrest.authentication import BasicAuthentication
        except ImportError:
            raise ImportError(
                "Please install azure-devops package to use Azure DevOps adapter"
            )
        if kwargs.get("base_url") is None:
            raise ValueError("Azure DevOps base_url is required. Example: 'https://dev.azure.com/YOURORG'")
        if kwargs.get("username") is None:
            raise ValueError("Azure DevOps username is required. You can leave this blank if you are using a PAT. ex: ''")
        if kwargs.get("password") is None:
            raise ValueError("Azure DevOps password is required. Personal Access Token (PAT) is recommended.")


        self.connection = Connection(
            base_url=kwargs.get("base_url"),
            creds=BasicAuthentication(
                username=kwargs.get("username"),
                password=kwargs.get("password"),
            ),
        )
        self._git_client: GitClient = self.connection.clients.get_git_client()

    def get_all_endpoints(self) -> Dict[str, str]:
        raise NotImplementedError

    async def request(
        self,
        endpoint: str,
        method: str,
        headers: Dict[str, Any] = {},
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError

    async def get_tree(
        self,
        owner: str,
        repo: str,
        tree_sha: str,
    ) -> GitTreeResponseModel:
        """
        Get the tree for a given sha.

        Args:
            - `owner (str)`: Project name or project id.
            - `repo (str)`: repository id.
            - `tree_sha (str)`: sha of the tree.

        Returns:
            - `tree (GitTreeResponseModel)`: Tree response model.
        """
        _git_tree_response: GitTreeRef = self._git_client.get_tree(
            repository_id=repo,
            sha1=tree_sha,
            project=owner,
        )

        git_tree_object_list: List[GitTreeResponseModel.GitTreeObject] = []
        tree_entry: GitTreeEntryRef
        for tree_entry in _git_tree_response.tree_entries:
            git_tree_object: GitTreeResponseModel.GitTreeObject = GitTreeResponseModel.GitTreeObject(
                path=tree_entry.relative_path,
                mode=tree_entry.mode,
                type=tree_entry.git_object_type,
                sha=tree_entry.object_id,
                url=tree_entry.url,
                size=tree_entry.size,
            )
            git_tree_object_list.append(git_tree_object)
        return GitTreeResponseModel(
            sha=_git_tree_response.object_id,
            url=_git_tree_response.url,
            tree=git_tree_object_list,
            truncated=False,
        )


    async def get_blob(
        self,
        owner: str,
        repo: str,
        file_sha: str,
    ) -> GitBlobResponseModel:
        """
        Get the blob for a given sha.

        Args:
            - `owner (str)`: Project name or project id.
            - `repo (str)`: repository id.
            - `file_sha (str)`: sha of the blob.

        Returns:
            - `blob (GitBlobResponseModel)`: Blob response model.
        """
        _git_blob_response: GitBlobRef = self._git_client.get_blob(
            repository_id=repo,
            sha1=file_sha,
            project=owner,
            download=False,
            resolve_lfs=False,
        )

        _git_blob_content_iterator = self._git_client.get_blob_content(
            repository_id=repo,
            sha1=file_sha,
            project=owner,
            download=False,
            resolve_lfs=False,
        )

        size = 0
        _git_blob_content: bytes = b""
        for chunk in _git_blob_content_iterator:
            _git_blob_content += chunk
            size += len(chunk)

        return GitBlobResponseModel(
            content=_git_blob_content,
            size=size,
            encoding="utf-8",
            sha=_git_blob_response.object_id,
            url=_git_blob_response.url,
            node_id=None
        )

    async def get_commit(
        self,
        owner: str,
        repo: str,
        commit_sha: str,
    ) -> GitCommitResponseModel:
        """
        Get the commit for a given sha.

        Args:
            - `owner (str)`: Project name or project id.
            - `repo (str)`: repository id.
            - `commit_sha (str)`: sha of the commit.

        Returns:
            - `commit (GitCommitResponseModel)`: Commit response model.
        """
        _git_commit_response: GitCommit = self._git_client.get_commit(
            repository_id=repo,
            commit_id=commit_sha,
            project=owner,
        )

        return GitCommitResponseModel(
            url=_git_commit_response.url,
            sha=_git_commit_response.commit_id,
            commit=GitCommitResponseModel.Commit(
                tree=GitCommitResponseModel.Commit.Tree(
                    sha=_git_commit_response.tree_id,
                ),
            ))

    async def get_branch(
        self,
        owner: str,
        repo: str,
        branch: Optional[str],
        branch_name: Optional[str],
    ) -> GitBranchResponseModel:
        """
        Get the branch for a given branch name.

        Args:
            - `owner (str)`: Project name or project id.
            - `repo (str)`: repository id.
            - `branch (str)`: branch name.

        Returns:
            - `branch (GitBranchResponseModel)`: Branch response model.
        """
        _git_branch_response: GitBranchStats = self._git_client.get_branch(
            repository_id=repo,
            project=owner,
            name=branch
        )

        # get the latest commit for the branch
        _git_commit_response: GitCommit = self._git_client.get_commit(
            repository_id=repo,
            commit_id=_git_branch_response.commit.commit_id,
            project=owner,
        )

        return GitBranchResponseModel(
            name=_git_branch_response.name,
            commit=GitBranchResponseModel.Commit(
                commit=GitBranchResponseModel.Commit.Commit(
                    tree=GitBranchResponseModel.Commit.Commit.Tree(
                        sha=_git_commit_response.tree_id,
                    ),
                ),
            ),
            _links=None,
        )