from llama_index import Document
import httpx
import pytest
import asyncio
import base64
import os
from unittest.mock import MagicMock, AsyncMock, call
import unittest
from typing import List, Tuple

# Remove this to test changes to GithubRepositoryReader.
pytest.skip("Skip by default due to network request.", allow_module_level=True)

from loader_hub.github_repo.utils import (
    BufferedAsyncIterator,
    BufferedGitBlobDataIterator,
)

from loader_hub.github_repo.github_client import (
    GithubClient,
    GitBlobResponseModel,
    GitTreeResponseModel,
)

from loader_hub.github_repo.base import GithubRepositoryReader


##    Test BufferedAsyncIterator   ##
## and BufferedGitBlobDataIterator ##


class MockGithubClient:
    async def get_blob(self, owner, repo, sha):
        return f"base64-decoded string blob content {owner}/{repo}/{sha}"


@pytest.mark.asyncio
async def test_buffered_async_iterator():
    class TestIterator(BufferedAsyncIterator):
        def __init__(self, data: List[Tuple[str, str]], buffer_size: int = 2):
            super().__init__(buffer_size)
            self._data = data

        async def _fill_buffer(self):
            del self._buffer[:]
            self._buffer = []
            start = self._index
            end = min(start + self._buffer_size, len(self._data))

            if start >= end:
                return

            self._buffer = self._data[start:end]

    data = [
        ("my-sha-1", "my/path1"),
        ("my-sha-2", "my/path2"),
        ("my-sha-3", "my/path3"),
        ("my-sha-4", "my/path4"),
        ("my-sha-5", "my/path5"),
        ("my-sha-6", "my/path6"),
    ]
    iterator = TestIterator(data, buffer_size=2)
    assert len(iterator._buffer) == 0
    assert iterator._index == 0
    assert iterator._buffer_size == 2
    assert await iterator.__anext__() == ("my-sha-1", "my/path1")
    assert len(iterator._buffer) == 1
    assert iterator._index == 1
    assert await iterator.__anext__() == ("my-sha-2", "my/path2")
    assert len(iterator._buffer) == 0
    assert iterator._index == 2
    assert await iterator.__anext__() == ("my-sha-3", "my/path3")
    assert len(iterator._buffer) == 1
    assert iterator._index == 3
    assert await iterator.__anext__() == ("my-sha-4", "my/path4")
    assert len(iterator._buffer) == 0
    assert iterator._index == 4
    assert await iterator.__anext__() == ("my-sha-5", "my/path5")
    assert len(iterator._buffer) == 1
    assert iterator._index == 5
    assert await iterator.__anext__() == ("my-sha-6", "my/path6")
    assert len(iterator._buffer) == 0
    assert iterator._index == 6
    with pytest.raises(StopAsyncIteration):
        await iterator.__anext__()


@pytest.mark.asyncio
async def test_buffered_git_blob_data_iterator():
    github_client = MockGithubClient()
    owner = "my-owner"
    repo = "my-repo"
    loop = asyncio.get_event_loop()
    blobs_and_paths = [
        (
            GitTreeResponseModel.GitTreeObject(
                sha="my-sha-1",
                path="file1",
                mode="100644",
                type="blob",
                size=123,
                url="https://api.github.com/repos/octocat/Hello-World/git/blobs/my-sha-1",
            ),
            "path/file1",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                sha="my-sha-2",
                path="file2",
                mode="100644",
                type="blob",
                size=321,
                url="https://api.github.com/repos/octocat/Hello-World/git/blobs/my-sha-2",
            ),
            "path/file2",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                sha="my-sha-3",
                path="file3",
                mode="100644",
                type="blob",
                size=456,
                url="https://api.github.com/repos/octocat/Hello-World/git/blobs/my-sha-3",
            ),
            "path/to/file3",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                sha="my-sha-4",
                path="file4",
                mode="100644",
                type="blob",
                size=941,
                url="https://api.github.com/repos/octocat/Hello-World/git/blobs/my-sha-4",
            ),
            "path/to/file4",
        ),
    ]

    it = BufferedGitBlobDataIterator(
        blobs_and_paths,
        github_client,
        owner,
        repo,
        loop,
        buffer_size=3,
        verbose=False,
    )
    assert len(it._buffer) == 0
    assert it._index == 0
    assert it._buffer_size == 3
    assert await it.__anext__() == (
        f"base64-decoded string blob content {owner}/{repo}/my-sha-1",
        "path/file1",
    )
    assert len(it._buffer) == 2
    assert it._index == 1
    assert await it.__anext__() == (
        f"base64-decoded string blob content {owner}/{repo}/my-sha-2",
        "path/file2",
    )
    assert len(it._buffer) == 1
    assert it._index == 2
    assert await it.__anext__() == (
        f"base64-decoded string blob content {owner}/{repo}/my-sha-3",
        "path/to/file3",
    )
    assert len(it._buffer) == 0
    assert it._index == 3
    assert await it.__anext__() == (
        f"base64-decoded string blob content {owner}/{repo}/my-sha-4",
        "path/to/file4",
    )
    assert len(it._buffer) == 0
    assert it._index == 4
    with pytest.raises(StopAsyncIteration):
        await it.__anext__()


########################

## GithubClient tests ##


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
        branch_data._links.html
        == f"https://github.com/{owner}/{repo}/tree/{branch}"
    ), "Branch html link is incorrect"

    # test get_commit
    commit_data = await github_client.get_commit(owner, repo, commit_sha)
    assert commit_data.sha == commit_sha, "Commit sha is incorrect"
    assert (
        commit_data.url
        == f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    ), "Commit url is incorrect"

    # test get_tree
    tree_data = await github_client.get_tree(
        owner, repo, commit_data.commit.tree.sha
    )
    assert (
        tree_data.url
        == f"https://api.github.com/repos/{owner}/{repo}/git/trees/{commit_data.commit.tree.sha}"
    ), "Tree url is incorrect"
    assert (
        tree_data.sha == commit_data.commit.tree.sha
    ), "Tree sha is incorrect"
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
    blob_data = await github_client.get_blob(
        owner, repo, test_requirements_txt.sha
    )
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


class TestGithubRepositoryReader(unittest.TestCase):
    def setUp(self):
        self.github_client = MagicMock()
        self.owner = "owner"
        self.repo = "repo"
        self.reader = GithubRepositoryReader(
            self.github_client, self.owner, self.repo
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
        self.assertTrue(
            self.reader._check_filter_file_extensions(tree_obj_path)
        )

        self.reader._filter_file_extensions = (
            [".txt"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )
        self.assertTrue(
            self.reader._check_filter_file_extensions(tree_obj_path)
        )

    def test__allow_tree_obj(self):
        tree_obj_paths = [
            "src/file.py",
            "src/file.txt",
            "src/dir1/file.js",
            "src/assets/file.png",
            "src/assets/file.jpg",
            "src/assets/file.jpeg",
            "src/assets/file.gif",
            "src/assets/file.svg",
            "src/assets/file.ico",
            "src/documents/file.pdf",
            "src/documents/file.doc",
            "src/documents/file.docx",
            "src/documents/file.xls",
            "src/documents/file.xlsx",
            "src/documents/file.ppt",
            "src/documents/file.pptx",
            "src/documents/file.odt",
            "src/documents/file.ods",
            "src/dir2/subdir/file.cpp",
            "src/dir2/subdir/file.c",
            "src/dir2/subdir/file.h",
            "src/dir2/subdir/file.hpp",
            "src/dir2/subdir/file.java",
            "src/dir2/foo.cc",
            "src/dir2/foo.svg",
            "src/dir2/subdir/file.go",
            "src/sub/folder/loading.svg",
            "src/sub/folder/loading.ico",
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
            "src/file.py",
            "src/file.txt",
            "src/dir1/file.js",
            "src/dir2/subdir/file.hpp",
            "src/dir2/subdir/file.java",
            "src/dir2/foo.cc",
            "src/dir2/subdir/file.go",
        ]

        actual_tree_obj_paths = [
            tree_obj_path
            for tree_obj_path in tree_obj_paths
            if self.reader._allow_tree_obj(tree_obj_path)
        ]

        print(f"Expected: {expected_tree_obj_paths}")
        print(f"Actual: {actual_tree_obj_paths}")
        self.assertCountEqual(
            expected_tree_obj_paths, actual_tree_obj_paths
        ), "Tree object paths are incorrect"

        self.reader._filter_directories = (
            ["src/dir2/subdir", "src/documents"],
            GithubRepositoryReader.FilterType.INCLUDE,
        )
        self.reader._filter_file_extensions = (
            [".png", ".svg", ".ico", "jpg", ".java"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        )

        expected_tree_obj_paths = [
            "src/documents/file.pdf",
            "src/documents/file.doc",
            "src/documents/file.docx",
            "src/documents/file.xls",
            "src/documents/file.xlsx",
            "src/documents/file.ppt",
            "src/documents/file.pptx",
            "src/documents/file.odt",
            "src/documents/file.ods",
            "src/dir2/subdir/file.cpp",
            "src/dir2/subdir/file.c",
            "src/dir2/subdir/file.h",
            "src/dir2/subdir/file.hpp",
            "src/dir2/subdir/file.go",
        ]

        actual_tree_obj_paths = [
            tree_obj_path
            for tree_obj_path in tree_obj_paths
            if self.reader._allow_tree_obj(tree_obj_path)
        ]

        print(f"Expected: {expected_tree_obj_paths}")
        print(f"Actual: {actual_tree_obj_paths}")
        self.assertCountEqual(
            expected_tree_obj_paths, actual_tree_obj_paths
        ), "Tree object paths are incorrect"


## Test GithubRepositoryReader's _recurse_tree method


@pytest.mark.asyncio
async def test__recurse_tree():
    github_client = MagicMock()
    owner = "owner"
    repo = "repo"
    reader = GithubRepositoryReader(github_client, owner, repo)

    # return value for the first call to get_tree (the root tree)
    tree_sha = "1234"
    tree_data = GitTreeResponseModel(
        sha=tree_sha,
        tree=[
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file1.py",
                sha="5678",
                mode="100644",
                size=1111,
                url="https://api.github.com/repos/owner/repo/git/blobs/5678",
            ),
            GitTreeResponseModel.GitTreeObject(
                type="tree",
                path="folder1",
                sha="91011",
                mode="040000",
                size=None,
                url="https://api.github.com/repos/owner/repo/git/blobs/91011",
            ),
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file2.py",
                sha="1213",
                mode="100644",
                size=3333,
                url="https://api.github.com/repos/owner/repo/git/blobs/1213",
            ),
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file3.py",
                sha="1415",
                mode="100644",
                size=4444,
                url="https://api.github.com/repos/owner/repo/git/blobs/1415",
            ),
        ],
        truncated=False,
        url="https://api.github.com/repos/owner/repo/git/trees/1234",
    )

    def get_tree_side_effect(owner, repo, sha):
        if sha == tree_sha:
            return tree_data
        elif sha == "91011":
            # return value for the second call to get_tree (the tree for folder1)
            return GitTreeResponseModel(
                tree=[
                    GitTreeResponseModel.GitTreeObject(
                        type="blob",
                        path="file4.py",
                        sha="1617",
                        mode="100644",
                        size=6666,
                        url="https://api.github.com/repos/owner/repo/git/blobs/1617",
                    ),
                    GitTreeResponseModel.GitTreeObject(
                        type="tree",
                        path="folder3",
                        sha="1819",
                        mode="040000",
                        size=None,
                        url="https://api.github.com/repos/owner/repo/git/blobs/1819",
                    ),
                ],
                sha="91011",
                truncated=False,
                url="https://api.github.com/repos/owner/repo/git/trees/91011",
            )
        elif sha == "1819":
            # return value for the third call to get_tree (the tree for folder3)
            return GitTreeResponseModel(
                tree=[
                    GitTreeResponseModel.GitTreeObject(
                        type="blob",
                        path="file5.py",
                        sha="2021",
                        mode="100644",
                        size=8888,
                        url="https://api.github.com/repos/owner/repo/git/blobs/2021",
                    ),
                ],
                sha="1819",
                truncated=False,
                url="https://api.github.com/repos/owner/repo/git/trees/1819",
            )
        else:
            raise httpx.HTTPError(
                f"404 Client Error: Not Found for url: https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}"
            )

    github_client.get_tree = AsyncMock(side_effect=get_tree_side_effect)

    expected_blobs_and_full_paths = [
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file1.py",
                sha="5678",
                mode="100644",
                size=1111,
                url="https://api.github.com/repos/owner/repo/git/blobs/5678",
            ),
            "file1.py",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file2.py",
                sha="1213",
                mode="100644",
                size=3333,
                url="https://api.github.com/repos/owner/repo/git/blobs/1213",
            ),
            "file2.py",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file4.py",
                sha="1617",
                mode="100644",
                size=6666,
                url="https://api.github.com/repos/owner/repo/git/blobs/1617",
            ),
            "folder1/file4.py",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file5.py",
                sha="2021",
                mode="100644",
                size=8888,
                url="https://api.github.com/repos/owner/repo/git/blobs/2021",
            ),
            "folder1/folder3/file5.py",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file3.py",
                sha="1415",
                mode="100644",
                size=4444,
                url="https://api.github.com/repos/owner/repo/git/blobs/1415",
            ),
            "file3.py",
        ),
    ]

    blobs_and_full_paths = await reader._recurse_tree(tree_sha)

    # make sure get_tree was called the expected number of times
    assert (
        github_client.get_tree.call_count == 3
    ), "There should be only 3 calls to get_tree (one for the root tree, and one for each subfolder folder1 and folder3)"

    # sort the expected and actual results by full path so we can compare them
    for (blob, full_path), (expected_blob, expected_full_path) in zip(
        sorted(blobs_and_full_paths, key=lambda x: x[1]),
        sorted(expected_blobs_and_full_paths, key=lambda x: x[1]),
    ):
        assert (
            blob == expected_blob
        ), "actual blob info does not match expected blob info"
        assert (
            full_path == expected_full_path
        ), "actual full path does not match expected full path"

    with pytest.raises(
        httpx.HTTPError,
        match="404 Client Error: Not Found for url: https://api.github.com/repos/owner/repo/git/trees/12345",
    ):
        await reader._recurse_tree("12345")


@pytest.mark.asyncio
async def test__generate_documents():
    github_client = MagicMock()
    owner = "owner"
    repo = "repo"
    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=False,
        verbose=False,
    )

    blobs_and_paths: List[Tuple[GitTreeResponseModel.GitTreeObject, str]] = [
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file1.py",
                sha="5678",
                mode="100644",
                size=1111,
                url="https://api.github.com/repos/owner/repo/git/blobs/5678",
            ),
            "file1.py",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file2.ts",
                sha="1213",
                mode="100644",
                size=3333,
                url="https://api.github.com/repos/owner/repo/git/blobs/1213",
            ),
            "folder1/file2.ts",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file3.rs",
                sha="1415",
                mode="100644",
                size=4444,
                url="https://api.github.com/repos/owner/repo/git/blobs/1415",
            ),
            "folder1/folder2/file3.rs",
        ),
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file4.cc",
                sha="1617",
                mode="100644",
                size=6666,
                url="https://api.github.com/repos/owner/repo/git/blobs/1617",
            ),
            "folder1/folder2/folder3/file4.cc",
        ),
        (
            GitTreeResponseModel.GitTreeObject(  # this file should not end up in the generated documents since it should fail to decode as utf-8
                type="blob",
                path="file5.png",
                sha="2021",
                mode="100644",
                size=8888,
                url="https://api.github.com/repos/owner/repo/git/blobs/2021",
            ),
            "folder1/folder2/folder3/file5.png",
        ),
    ]

    async def get_blob_side_effect(owner: str, repo: str, sha: str):
        if sha == "5678":
            return GitBlobResponseModel(
                content="cHJpbnQoJ2hlbGxvIHdvcmxkJyk=",
                encoding="base64",
                sha="5678",
                size=1111,
                url="https://api.github.com/repos/owner/repo/git/blobs/5678",
                node_id="1234",
            )
        elif sha == "1213":
            return GitBlobResponseModel(
                content="Y29uc29sZS5sb2coJ2hlbGxvIHdvcmxkJyk=",
                encoding="base64",
                sha="1213",
                size=3333,
                url="https://api.github.com/repos/owner/repo/git/blobs/1213",
                node_id="2345",
            )
        elif sha == "1415":
            return GitBlobResponseModel(
                content="cHJpbnRsbiEoImhlbGxvIHdvcmxkIik=",
                encoding="base64",
                sha="1415",
                size=4444,
                url="https://api.github.com/repos/owner/repo/git/blobs/1415",
                node_id="3456",
            )
        elif sha == "1617":
            return GitBlobResponseModel(
                content="c3RkOjpjb3V0IDw8ICJoZWxsbyB3b3JsZCIgPDwgc3RkOjplbmRsOw==",
                encoding="base64",
                sha="1617",
                size=6666,
                url="https://api.github.com/repos/owner/repo/git/blobs/1617",
                node_id="4567",
            )
        elif sha == "2021":
            return GitBlobResponseModel(
                content="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                encoding="base64",
                sha="2021",
                size=8888,
                url="https://api.github.com/repos/owner/repo/git/blobs/2021",
                node_id="5678",
            )
        else:
            raise httpx.HTTPError(
                f"404 Client Error: Not Found for url: https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}"
            )

    github_client.get_blob = AsyncMock(side_effect=get_blob_side_effect)

    documents = await reader._generate_documents(blobs_and_paths)

    assert (
        github_client.get_blob.await_count == 5
    ), "get_blob should be awaited 5 times for each blob"

    github_client.get_blob.assert_has_awaits(
        [
            call(owner, repo, "5678"),
            call(owner, repo, "1213"),
            call(owner, repo, "1415"),
            call(owner, repo, "1617"),
            call(owner, repo, "2021"),
        ]
    ), "get_blob should be awaited with the correct arguments"

    assert (
        len(documents) == 4
    ), "There should be 4 documents generated from the blobs_and_paths"

    expected_documents = [
        Document(
            text="print('hello world')",
            extra_info={
                "file_path": "file1.py",
                "file_name": "file1.py",
            },
        ),
        Document(
            text="console.log('hello world')",
            extra_info={
                "file_path": "folder1/file2.ts",
                "file_name": "file2.ts",
            },
        ),
        Document(
            text='println!("hello world")',
            extra_info={
                "file_path": "folder1/folder2/file3.rs",
                "file_name": "file3.rs",
            },
        ),
        Document(
            text='std::cout << "hello world" << std::endl;',
            extra_info={
                "file_path": "folder1/folder2/folder3/file4.cc",
                "file_name": "file4.cc",
            },
        ),
    ]

    for document, expected_document in zip(
        sorted(documents, key=lambda x: x.extra_info["file_path"]),
        sorted(expected_documents, key=lambda x: x.extra_info["file_path"]),
    ):
        assert (
            document.text == expected_document.text
        ), "The text of the document should be the decoded content of the blob"
        assert (
            document.extra_info == expected_document.extra_info
        ), "The extra_info of the document should be the file_path and file_name"

    with pytest.raises(
        httpx.HTTPError,
        match="404 Client Error: Not Found for url: https://api.github.com/repos/owner/repo/git/blobs/12345",
    ):
        await reader._generate_documents(
            [
                (
                    GitTreeResponseModel.GitTreeObject(
                        type="blob",
                        path="file1.py",
                        sha="12345",
                        mode="100644",
                        size=1111,
                        url="https://api.github.com/repos/owner/repo/git/blobs/12345",
                    ),
                    "file1.py",
                )
            ]
        )
