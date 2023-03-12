import unittest
from typing import List, Tuple
from unittest.mock import AsyncMock, MagicMock

import pytest

# Remove this to test changes to GithubRepositoryReader.
pytest.skip("Skip by default due to network request.", allow_module_level=True)

import base64
import os

import pytest
from gpt_index import Document

from loader_hub.github_repo import GithubClient, GithubRepositoryReader


@pytest.fixture
def github_client():
    return GithubClient(
        github_token=os.getenv("GITHUB_API_TOKEN"),
        verbose=True,
    )


@pytest.mark.asyncio
async def test_github_client(github_client):
    owner = "emptycrown"
    repo = "llama-hub"
    branch = "main"
    commit_sha = "0cd691322e5244b48b68e3588d1343eb53f3a112"  # Points to Add spotify reader, https://github.com/emptycrown/llama-hub/commit/0cd691322e5244b48b68e3588d1343eb53f3a112

    # test get_branch
    branch_data = await github_client.get_branch(owner, repo, branch)
    assert branch_data.name == branch
    assert (
        branch_data._links.self
        == f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    ), "Branch self link is incorrect"
    assert (
        branch_data._links.html == f"https://github.com/{owner}/{repo}/tree/{branch}"
    ), "Branch html link is incorrect"

    # test get_commit
    commit_data = await github_client.get_commit(owner, repo, commit_sha)
    assert commit_data.sha == commit_sha, "Commit sha is incorrect"
    assert (
        commit_data.url
        == f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    ), "Commit url is incorrect"

    # test get_tree
    tree_data = await github_client.get_tree(owner, repo, commit_data.commit.tree.sha)
    assert (
        tree_data.url
        == f"https://api.github.com/repos/{owner}/{repo}/git/trees/{commit_data.commit.tree.sha}"
    ), "Tree url is incorrect"
    assert tree_data.sha == commit_data.commit.tree.sha, "Tree sha is incorrect"
    print(tree_data.tree[0].sha)
    assert 1 == 1

    # test get_blob
    expected_files_in_first_depth_of_the_tree: List[Tuple[str, str]] = [
        ("test_requirements.txt", "blob"),
        ("README.md", "blob"),
        ("Makefile", "blob"),
        (".gitignore", "blob"),
        ("tests", "tree"),
        ("loader_hub", "tree"),
        (".github", "tree"),
    ]
    # check if the first depth of the tree has the expected files. All the expected files should be in the first depth of the tree and vice versa
    assert len(tree_data.tree) == len(
        expected_files_in_first_depth_of_the_tree
    ), "The number of files in the first depth of the tree is incorrect"
    for file in expected_files_in_first_depth_of_the_tree:
        assert file in [
            (tree_file.path, tree_file.type) for tree_file in tree_data.tree
        ], f"{file} is not in the first depth of the tree"
    # checking the opposite
    for tree_obj in tree_data.tree:
        assert (
            tree_obj.path,
            tree_obj.type,
        ) in expected_files_in_first_depth_of_the_tree, (
            f"{tree_obj.path} is not in the expected files"
        )

    # find test_reqirements.txt in the tree
    test_requirements_txt = [
        tree_obj
        for tree_obj in tree_data.tree
        if tree_obj.path == "test_requirements.txt"
    ][0]

    # test get_blob
    blob_data = await github_client.get_blob(owner, repo, test_requirements_txt.sha)
    assert blob_data.encoding == "base64", "Blob encoding is incorrect"
    assert (
        blob_data.url
        == f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{test_requirements_txt.sha}"
    ), "Blob url is incorrect"
    assert blob_data.sha == test_requirements_txt.sha, "Blob sha is incorrect"

    # decode blob content base64-decoded string to utf-8
    decoded_blob_content = base64.b64decode(blob_data.content).decode("utf-8")

    expected_decoded_blob_content = """

# For testing
pytest==7.2.1
pytest-dotenv==0.5.2
# TODO: remove gpt_index after migration
https://github.com/jerryjliu/gpt_index/archive/master.zip

llama-index

# For linting
# linting stubs
types-requests==2.28.11.8
# formatting
black==22.12.0
isort==5.11.4
"""
    # check if the decoded blob content is correct
    for dbc in zip(
        filter(lambda x: x != "", decoded_blob_content.splitlines()),
        filter(lambda x: x != "", expected_decoded_blob_content.splitlines()),
    ):
        assert dbc[0] == dbc[1], f"{dbc[0]} is not equal to {dbc[1]}"
