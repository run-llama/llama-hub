import base64
import os
import unittest
from typing import List, Tuple
from unittest.mock import MagicMock

import pytest

from llama_hub.github_repo.base import GithubRepositoryReader
from llama_hub.github_repo.github_client import GithubClient

# Remove this to test changes to GithubRepositoryReader.
# pytest.skip(
#     "Skip by default due to dependence on network request and github api token.",
#     allow_module_level=True,
# )


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
    commit_sha = (  # Points to Add spotify reader, https://github.com/emptycrown/llama-hub/commit/0cd691322e5244b48b68e3588d1343eb53f3a112
        "0cd691322e5244b48b68e3588d1343eb53f3a112"
    )

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


@pytest.mark.asyncio
async def test_github_client_get_branch_parameter_exception(github_client):
    branch_data = await github_client.get_branch(
        owner="emptycrown",
        repo="llama-hub",
        branch="main",
    )
    assert branch_data.name == "main"
    branch_data = await github_client.get_branch(
        owner="emptycrown",
        repo="llama-hub",
        branch_name="main",
    )
    assert branch_data.name == "main"
    with pytest.raises(ValueError):
        await github_client.get_branch(
            owner="emptycrown",
            repo="llama-hub",
        )


class TestGithubRepositoryReader(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.github_client = MagicMock()
        self.owner = "owner"
        self.repo = "repo"
        self.reader = GithubRepositoryReader(
            self.github_client,
            self.owner,
            self.repo,
            verbose=True,
            use_parser=False,
        )

    def test__check_filter_directories(self):
        tree_obj_path = "path/to/some/file.py"
        self.reader._filter_directories = (
            ["path/to"],
            GithubRepositoryReader.FilterType.INCLUDE,
        )
        self.assertTrue(self.reader._check_filter_directories(tree_obj_path))

        self.reader._filter_directories = (
            ["path/to"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )
        self.assertFalse(self.reader._check_filter_directories(tree_obj_path))

    def test__check_filter_file_extensions(self):
        tree_obj_path = "path/to/some/file.py"
        self.reader._filter_file_extensions = (
            [".py"],
            GithubRepositoryReader.FilterType.INCLUDE,
        )
        self.assertTrue(self.reader._check_filter_file_extensions(tree_obj_path))

        self.reader._filter_file_extensions = (
            [".txt"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )
        self.assertTrue(self.reader._check_filter_file_extensions(tree_obj_path))

    def test__allow_tree_obj_with_files_only(self):
        tree_obj_paths = [
            ("src", "tree"),
            ("src/file.py", "blob"),
            ("src/file.txt", "blob"),
            ("src/file.md", "blob"),
            ("src/Path.To.Folder", "tree"),
            ("src/Path.To.Folder/file1.js", "blob"),
            ("src/Path.To.Folder/file2.cpp", "blob"),
            ("src/Path.To.Folder/file4.rs", "blob"),
            ("src/Path.To.Folder/file5.ts", "blob"),
            ("src/Path.To.Folder/file6.h", "blob"),
            ("src/Path.To.Folder/file7.c", "blob"),
            ("src/Path.To.Folder/file8.java", "blob"),
            ("src/assets/file.png", "blob"),
            ("src/assets/file.jpg", "blob"),
            ("src/assets/file.jpeg", "blob"),
            ("src/assets/file.gif", "blob"),
            ("src/assets/file.svg", "blob"),
            ("src/assets/file.ico", "blob"),
            ("src/documents", "tree"),
            ("src/documents/file.pdf", "blob"),
            ("src/documents/file.doc", "blob"),
            ("src/documents/file.docx", "blob"),
            ("src/documents/file.xls", "blob"),
            ("src/documents/file.xlsx", "blob"),
            ("src/documents/file.ppt", "blob"),
            ("src/documents/file.pptx", "blob"),
            ("src/documents/file.odt", "blob"),
            ("src/documents/file.ods", "blob"),
            ("src/dir1", "tree"),
            ("src/dir1/file.js", "blob"),
            ("src/dir2", "tree"),
            ("src/dir2/file.py", "blob"),
            ("src/dir2/foo.cc", "blob"),
            ("src/dir2/foo.svg", "blob"),
            ("src/dir2/subdir", "tree"),
            ("src/dir2/subdir/file.cpp", "blob"),
            ("src/dir2/subdir/file.c", "blob"),
            ("src/dir2/subdir/file.h", "blob"),
            ("src/dir2/subdir/file.hpp", "blob"),
            ("src/dir2/subdir/file.java", "blob"),
            ("src/dir2/subdir/file.go", "blob"),
            ("src/sub", "tree"),
            ("src/sub/folder", "tree"),
            ("src/sub/folder/loading.svg", "blob"),
            ("src/sub/folder/loading.ico", "blob"),
            ("out", "tree"),
            ("out/file.py", "blob"),
            ("out/assets", "tree"),
            ("out/assets/file.png", "blob"),
            ("out/Path.To.Folder", "tree"),
            ("out/Path.To.Folder/file1.js", "blob"),
            ("out/sub", "tree"),
            ("out/sub/folder", "tree"),
            ("out/sub/folder/loading.svg", "blob"),
        ]
        self.reader._filter_directories = (
            ["src/assets", "src/documents"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )
        self.reader._filter_file_extensions = (
            [".svg", ".ico", ".cpp", ".c", ".h"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )

        expected_tree_obj_paths = [
            "src",
            "src/file.py",
            "src/file.txt",
            "src/file.md",
            "src/Path.To.Folder",
            "src/Path.To.Folder/file1.js",
            # "src/Path.To.Folder/file2.cpp",   # It should be excluded because of the extension in the filter
            "src/Path.To.Folder/file4.rs",
            "src/Path.To.Folder/file5.ts",
            # "src/Path.To.Folder/file6.h",
            # "src/Path.To.Folder/file7.c",
            "src/Path.To.Folder/file8.java",
            # "src/assets",                     # The whole directory should be excluded because of the filter
            # "src/assets/file.png",
            # "src/assets/file.jpg",
            # "src/assets/file.jpeg",
            # "src/assets/file.gif",
            # "src/assets/file.svg",
            # "src/assets/file.ico"
            # "src/documents",                  # The whole directory should be excluded because of the filter
            # "src/documents/file.pdf",
            # "src/documents/file.doc",
            # "src/documents/file.docx",
            # "src/documents/file.xls",
            # "src/documents/file.xlsx",
            # "src/documents/file.ppt",
            # "src/documents/file.pptx",
            # "src/documents/file.odt",
            # "src/documents/file.ods",
            "src/dir1",
            "src/dir1/file.js",
            "src/dir2",
            "src/dir2/file.py",
            "src/dir2/foo.cc",
            # "src/dir2/foo.svg",               # It should be excluded because of the extension in the filter
            "src/dir2/subdir",
            # "src/dir2/subdir/file.cpp",       # It should be excluded because of the extension in the filter
            # "src/dir2/subdir/file.c",         # It should be excluded because of the extension in the filter
            # "src/dir2/subdir/file.h",         # It should be excluded because of the extension in the filter
            "src/dir2/subdir/file.hpp",
            "src/dir2/subdir/file.java",
            "src/dir2/subdir/file.go",
            "src/sub",
            "src/sub/folder",
            # "src/sub/folder/loading.svg",     # It should be excluded because of the extension in the filter
            # "src/sub/folder/loading.ico",     # It should be excluded because of the extension in the filter
            "out",
            "out/file.py",
            "out/assets",
            "out/assets/file.png",
            "out/Path.To.Folder",
            "out/Path.To.Folder/file1.js",
            "out/sub",
            "out/sub/folder",
            # "out/sub/folder/loading.svg",     # It should be excluded because of the extension in the filter
        ]

        actual_tree_obj_paths = [
            tree_obj_path
            for tree_obj_path, tree_obj_type in tree_obj_paths
            if self.reader._allow_tree_obj(tree_obj_path, tree_obj_type)
        ]

        self.assertCountEqual(
            expected_tree_obj_paths, actual_tree_obj_paths
        ), "Tree object paths are incorrect"

        self.reader._filter_directories = (
            [
                "src/dir2/subdir",
                "src/documents",
                "src/Path.To.Folder",
                "out/assets",
                "out/sub/folder",
            ],
            GithubRepositoryReader.FilterType.INCLUDE,
        )
        self.reader._filter_file_extensions = (
            [".png", ".svg", ".ico", "jpg", ".java", ".doc", ".pptx"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )

        expected_tree_obj_paths = [
            "out",
            "out/assets",
            # "out/assets/file.png",  # It should be excluded by extension
            "out/sub",
            "out/sub/folder",
            "src",
            # "out/sub/folder/loading.svg", # It should be excluded by extension
            "src/Path.To.Folder",
            "src/Path.To.Folder/file1.js",
            "src/Path.To.Folder/file2.cpp",
            "src/Path.To.Folder/file4.rs",
            "src/Path.To.Folder/file5.ts",
            "src/Path.To.Folder/file6.h",
            "src/Path.To.Folder/file7.c",
            # "src/Path.To.Folder/file8.java", # It should be excluded by extension
            "src/dir2",
            "src/dir2/subdir",
            "src/dir2/subdir/file.cpp",
            "src/dir2/subdir/file.c",
            "src/dir2/subdir/file.h",
            "src/dir2/subdir/file.hpp",
            # "src/dir2/subdir/file.java", # It should be excluded by extension
            "src/dir2/subdir/file.go",
            "src/documents",
            "src/documents/file.pdf",
            # "src/documents/file.doc", # It should be excluded by extension
            "src/documents/file.docx",
            "src/documents/file.xls",
            "src/documents/file.xlsx",
            "src/documents/file.ppt",
            # "src/documents/file.pptx", # It should be excluded by extension
            "src/documents/file.odt",
            "src/documents/file.ods",
        ]

        actual_tree_obj_paths = [
            tree_obj_path
            for tree_obj_path, tree_obj_type in tree_obj_paths
            if self.reader._allow_tree_obj(tree_obj_path, tree_obj_type)
        ]

        self.assertCountEqual(
            expected_tree_obj_paths, actual_tree_obj_paths
        ), "Tree object paths are incorrect"
