from typing import List, Tuple
from unittest.mock import AsyncMock, MagicMock, call

import httpx
import pytest
from llama_index import Document

from llama_hub.github_repo.base import GithubRepositoryReader
from llama_hub.github_repo.github_client import (
    GitBlobResponseModel,
    GitBranchResponseModel,
    GithubClient,
    GitTreeResponseModel,
)

## Test GithubRepositoryReader's _recurse_tree method


@pytest.mark.asyncio
async def test__recurse_tree():
    github_client = MagicMock()
    owner = "owner"
    repo = "repo"
    reader = GithubRepositoryReader(github_client, owner, repo, verbose=True)

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
                    GitTreeResponseModel.GitTreeObject(
                        type="blob",
                        path="file6.json",
                        sha="2223",
                        mode="100644",
                        size=9999,
                        url="https://api.github.com/repos/owner/repo/git/blobs/2223",
                    ),
                ],
                sha="1819",
                truncated=False,
                url="https://api.github.com/repos/owner/repo/git/trees/1819",
            )
        else:
            raise httpx.HTTPError(
                "404 Client Error: Not Found for url:"
                f" https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}"
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
        (
            GitTreeResponseModel.GitTreeObject(
                type="blob",
                path="file6.json",
                sha="2223",
                mode="100644",
                size=9999,
                url="https://api.github.com/repos/owner/repo/git/blobs/2223",
            ),
            "folder1/folder3/file6.json",
        ),
    ]

    blobs_and_full_paths = await reader._recurse_tree(tree_sha)

    # make sure get_tree was called the expected number of times
    assert github_client.get_tree.call_count == 3, (
        "There should be only 3 calls to get_tree (one for the root tree, and one for"
        " each subfolder folder1 and folder3)"
    )

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
        match=(
            "404 Client Error: Not Found for url:"
            " https://api.github.com/repos/owner/repo/git/trees/12345"
        ),
    ):
        await reader._recurse_tree("12345")

    reader._filter_directories = (
        ["folder1/folder3"],
        GithubRepositoryReader.FilterType.INCLUDE,
    )

    reader._filter_file_extensions = (
        [".json"],
        GithubRepositoryReader.FilterType.EXCLUDE,
    )

    expected_blobs_and_full_paths = [
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
    ]

    blobs_and_full_paths = await reader._recurse_tree(tree_sha)

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
                "404 Client Error: Not Found for url:"
                f" https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}"
            )

    github_client.get_blob = AsyncMock(side_effect=get_blob_side_effect)

    documents = await reader._generate_documents(blobs_and_paths, id="1234")

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
                "url": "https://github.com/owner/repo/blob/1234/file1.py",
            },
        ),
        Document(
            text="console.log('hello world')",
            extra_info={
                "file_path": "folder1/file2.ts",
                "file_name": "file2.ts",
                "url": "https://github.com/owner/repo/blob/1234/folder1/file2.ts",
            },
        ),
        Document(
            text='println!("hello world")',
            extra_info={
                "file_path": "folder1/folder2/file3.rs",
                "file_name": "file3.rs",
                "url": (
                    "https://github.com/owner/repo/blob/1234/folder1/folder2/file3.rs"
                ),
            },
        ),
        Document(
            text='std::cout << "hello world" << std::endl;',
            extra_info={
                "file_path": "folder1/folder2/folder3/file4.cc",
                "file_name": "file4.cc",
                "url": "https://github.com/owner/repo/blob/1234/folder1/folder2/folder3/file4.cc",
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
        match=(
            "404 Client Error: Not Found for url:"
            " https://api.github.com/repos/owner/repo/git/blobs/12345"
        ),
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


def get_mocked_github_client():
    github_client = GithubClient()

    async def get_branch_side_effect(
        owner: str, repo: str, branch: str
    ) -> GitBranchResponseModel:
        if branch == "test-branch-name":
            return GitBranchResponseModel(
                name="test-branch-name",
                commit=GitBranchResponseModel.Commit(
                    commit=GitBranchResponseModel.Commit.Commit(
                        tree=GitBranchResponseModel.Commit.Commit.Tree(
                            sha="1234",
                        )
                    )
                ),
                _links=MagicMock(),
            )
        else:
            raise httpx.HTTPError(
                "404 Client Error: Not Found for url:"
                f" https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
            )

    github_client.get_branch = AsyncMock(side_effect=get_branch_side_effect)

    async def get_tree_side_effect(
        owner: str,
        repo: str,
        sha: str,
    ) -> GitTreeResponseModel:
        #
        #  The mocked github repo structure:
        #   .
        #   ├───.github
        #   │   ├───workflows
        #   │   │   ├────lint.yml
        #   │   │   └────build_package.yml
        #   ├───.vscode
        #   │   ├────settings.json
        #   ├───docs
        #   │   ├────gallery
        #   │   │    └────example_picture.png
        #   │   ├────guides
        #   │   │    └────example_guide.md
        #   │   ├────index.rst
        #   ├───src
        #   │   ├────package
        #   │   │    ├─── subpackage
        #   │   │    │    └────example_subpackage.py
        #   │   │    └───example_package.py
        #   │   ├────tests
        #   │   │    ├────test_file1.py
        #   │   │    └────test_file2.js
        #   │   └────__init__.py
        #   ├───README.md
        #   ├───LICENSE
        #   └───setup.py
        mocked_tree_responses = {
            "1234": [  # root tree
                {
                    "type": "tree",
                    "path": ".github",
                    "sha": "5678",
                },
                {
                    "type": "tree",
                    "path": ".vscode",
                    "sha": "1213",
                },
                {
                    "type": "tree",
                    "path": "docs",
                    "sha": "1415",
                },
                {
                    "type": "tree",
                    "path": "src",
                    "sha": "1617",
                },
                {
                    "type": "blob",
                    "path": "README.md",
                    "sha": "2021",
                },
                {
                    "type": "blob",
                    "path": "LICENSE",
                    "sha": "2324",
                },
                {
                    "type": "blob",
                    "path": "setup.py",
                    "sha": "2627",
                },
            ],
            "5678": [  # .github
                {
                    "type": "tree",
                    "path": "workflows",
                    "sha": "9091",
                },
            ],
            "1213": [  # .vscode
                {
                    "type": "blob",
                    "path": "settings.json",
                    "sha": "3031",
                },
            ],
            "1415": [  # docs
                {
                    "type": "tree",
                    "path": "gallery",
                    "sha": "3233",
                },
                {
                    "type": "tree",
                    "path": "guides",
                    "sha": "3435",
                },
                {
                    "type": "blob",
                    "path": "index.rst",
                    "sha": "3637",
                },
            ],
            "1617": [  # src
                {
                    "type": "tree",
                    "path": "package",
                    "sha": "3839",
                },
                {
                    "type": "tree",
                    "path": "tests",
                    "sha": "4041",
                },
                {
                    "type": "blob",
                    "path": "__init__.py",
                    "sha": "4243",
                },
            ],
            "9091": [  # .github/workflows
                {
                    "type": "blob",
                    "path": "lint.yml",
                    "sha": "4445",
                },
                {
                    "type": "blob",
                    "path": "build_package.yml",
                    "sha": "4647",
                },
            ],
            "3233": [  # docs/gallery
                {
                    "type": "blob",
                    "path": "example_picture.png",
                    "sha": "4849",
                },
            ],
            "3435": [  # docs/guides
                {
                    "type": "blob",
                    "path": "example_guide.md",
                    "sha": "5051",
                },
            ],
            "3839": [  # src/package
                {
                    "type": "tree",
                    "path": "subpackage",
                    "sha": "5253",
                },
                {
                    "type": "blob",
                    "path": "example_package.py",
                    "sha": "5455",
                },
            ],
            "4041": [  # src/tests
                {
                    "type": "blob",
                    "path": "test_file1.py",
                    "sha": "5657",
                },
                {
                    "type": "blob",
                    "path": "test_file2.js",
                    "sha": "5859",
                },
            ],
            "5253": [  # src/package/subpackage
                {
                    "type": "blob",
                    "path": "example_subpackage.py",
                    "sha": "6061",
                },
            ],
        }

        if sha in mocked_tree_responses:
            trees = [
                GitTreeResponseModel.GitTreeObject(
                    **item,
                    mode="040000" if item["type"] == "tree" else "100644",
                    size=None if item["type"] == "tree" else 8888,
                    url=f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{item['sha']}",
                )
                for item in mocked_tree_responses[sha]
            ]
            return GitTreeResponseModel(
                sha=sha,
                url=f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}",
                tree=trees,
                truncated=False,
            )
        else:
            raise httpx.HTTPError(
                "404 Client Error: Not Found for url:"
                f" https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}"
            )

    github_client.get_tree = AsyncMock(side_effect=get_tree_side_effect)

    async def get_blob_side_effect(
        owner: str, repo: str, sha: str
    ) -> GitBlobResponseModel:
        mocked_blob_responses = {
            "2021": "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBSRUFETUUubWQ=",  # README.md
            "2324": "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBMSUNFTlNF",  # LICENSE
            "2627": "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBzZXR1cC5weQ==",  # setup.py
            "3031": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBzZXR0aW5ncy5qc29u"
            ),  # settings.json
            "3637": "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBpbmRleC5yc3Q=",  # index.rst
            "4243": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBfX2luaXRfXy5weQ=="
            ),  # __init__.py
            "4445": "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBsaW50LnltbA==",  # lint.yml
            "4647": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBidWlsZF9wYWNrYWdlLnltbA=="
            ),  # build_package.yml
            "4849": "aGVsbG8gd29ybGQ=",  # example_picture.png
            "5051": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBleGFtcGxlX2d1aWRlLm1k"
            ),  # example_guide.md
            "5455": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBleGFtcGxlX3BhY2thZ2UucHk="
            ),  # example_package.py
            "5657": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciB0ZXN0X2ZpbGUxLnB5"
            ),  # test_file1.py
            "5859": (
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciB0ZXN0X2ZpbGUyLmpz"
            ),  # test_file2.js
            "6061": (  # example_subpackage.py
                "dGhpcyBpcyB0aGUgZmlsZSBjb250ZW50IGZvciBleGFtcGxlX3N1YnBhY2thZ2UucHk="
            ),
        }

        if sha in mocked_blob_responses:
            return GitBlobResponseModel(
                sha=sha,
                url=f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}",
                content=mocked_blob_responses[sha],
                encoding="base64",
                size=8888,
                node_id="",
            )
        else:
            raise httpx.HTTPError(
                "404 Client Error: Not Found for url:"
                f" https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}"
            )

    github_client.get_blob = AsyncMock(side_effect=get_blob_side_effect)

    return github_client


def test_load_data_without_filters():
    branch_name = "test-branch-name"
    github_client = get_mocked_github_client()

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner="owner",
        repo="repo",
        verbose=True,
    )

    expected_docs = [
        Document(
            text="this is the file content for README.md",
            extra_info={
                "file_path": "README.md",
                "file_name": "README.md",
            },
        ),
        Document(
            text="this is the file content for LICENSE",
            extra_info={
                "file_path": "LICENSE",
                "file_name": "LICENSE",
            },
        ),
        Document(
            text="this is the file content for setup.py",
            extra_info={
                "file_path": "setup.py",
                "file_name": "setup.py",
            },
        ),
        Document(
            text="this is the file content for settings.json",
            extra_info={
                "file_path": ".vscode/settings.json",
                "file_name": "settings.json",
            },
        ),
        Document(
            text="this is the file content for index.rst",
            extra_info={
                "file_path": "docs/index.rst",
                "file_name": "index.rst",
            },
        ),
        Document(
            text="this is the file content for __init__.py",
            extra_info={
                "file_path": "src/__init__.py",
                "file_name": "__init__.py",
            },
        ),
        Document(
            text="this is the file content for lint.yml",
            extra_info={
                "file_path": ".github/workflows/lint.yml",
                "file_name": "lint.yml",
            },
        ),
        Document(
            text="this is the file content for build_package.yml",
            extra_info={
                "file_path": ".github/workflows/build_package.yml",
                "file_name": "build_package.yml",
            },
        ),
        Document(
            text="hello world",
            extra_info={
                "file_path": "docs/gallery/example_picture.png",
                "file_name": "example_picture.png",
            },
        ),
        Document(
            text="this is the file content for example_guide.md",
            extra_info={
                "file_path": "docs/guides/example_guide.md",
                "file_name": "example_guide.md",
            },
        ),
        Document(
            text="this is the file content for example_package.py",
            extra_info={
                "file_path": "src/package/example_package.py",
                "file_name": "example_package.py",
            },
        ),
        Document(
            text="this is the file content for test_file1.py",
            extra_info={
                "file_path": "src/tests/test_file1.py",
                "file_name": "test_file1.py",
            },
        ),
        Document(
            text="this is the file content for test_file2.js",
            extra_info={
                "file_path": "src/tests/test_file2.js",
                "file_name": "test_file2.js",
            },
        ),
        Document(
            text="this is the file content for example_subpackage.py",
            extra_info={
                "file_path": "src/package/subpackage/example_subpackage.py",
                "file_name": "example_subpackage.py",
            },
        ),
    ]

    docs = reader.load_data(branch=branch_name)

    assert len(docs) == len(expected_docs), (
        "There are 14 files in the test repo and 14 docs should be returned since no"
        " filters are applied."
    )

    print("Expected docs:")
    for doc in expected_docs:
        print(doc)

    print("Actual docs:")
    for doc in docs:
        print(doc)
    for expected, actual in zip(
        sorted(expected_docs, key=lambda x: x.extra_info["file_name"]),
        sorted(docs, key=lambda x: x.extra_info["file_name"]),
    ):
        assert expected.text == actual.text, (
            "The content of the expected doc and the actual doc should be the same"
            f"Expected: {expected.text}"
            f"Actual: {actual.text}"
        )
        assert expected.extra_info["file_path"] == actual.extra_info["file_path"]
        assert expected.extra_info["file_name"] == actual.extra_info["file_name"]


def test_load_data_with_filters1():
    branch_name = "test-branch-name"
    github_client = get_mocked_github_client()

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner="owner",
        repo="repo",
        verbose=True,
        filter_directories=(
            ["src/tests"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        filter_file_extensions=(
            [".py"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
    )

    expected_docs = [
        Document(
            text="this is the file content for test_file1.py",
            extra_info={
                "file_path": "src/tests/test_file1.py",
                "file_name": "test_file1.py",
            },
        ),
    ]

    docs = reader.load_data(branch=branch_name)

    assert len(docs) == len(
        expected_docs
    ), "Should have 1 docs since only .py files in src/tests are included"

    print("Expected docs:")
    for doc in expected_docs:
        print(doc)

    print("Actual docs:")
    for doc in docs:
        print(doc)

    for expected, actual in zip(
        sorted(expected_docs, key=lambda x: x.extra_info["file_name"]),
        sorted(docs, key=lambda x: x.extra_info["file_name"]),
    ):
        assert expected.text == actual.text, (
            "The content of the expected doc and the actual doc should be the same"
            f"Expected: {expected.text}"
            f"Actual: {actual.text}"
        )
        assert expected.extra_info["file_path"] == actual.extra_info["file_path"]
        assert expected.extra_info["file_name"] == actual.extra_info["file_name"]


def test_load_data_with_filters2():
    branch_name = "test-branch-name"
    github_client = get_mocked_github_client()

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner="owner",
        repo="repo",
        verbose=True,
        filter_directories=(
            ["src/package/subpackage", "docs/guides"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
        filter_file_extensions=(
            [".yml", ".png", ".js", ".md"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
    )

    expected_docs = [
        Document(
            text="this is the file content for lint.yml",
            extra_info={
                "file_path": ".github/workflows/lint.yml",
                "file_name": "lint.yml",
            },
        ),
        Document(
            text="this is the file content for build_package.yml",
            extra_info={
                "file_path": ".github/workflows/build_package.yml",
                "file_name": "build_package.yml",
            },
        ),
        Document(
            text="hello world",
            extra_info={
                "file_path": "docs/gallery/example_picture.png",
                "file_name": "example_picture.png",
            },
        ),
        Document(
            text="this is the file content for README.md",
            extra_info={
                "file_path": "README.md",
                "file_name": "README.md",
            },
        ),
        Document(
            text="this is the file content for test_file2.js",
            extra_info={
                "file_path": "src/tests/test_file2.js",
                "file_name": "test_file2.js",
            },
        ),
    ]

    docs = reader.load_data(branch=branch_name)

    assert len(docs) == len(expected_docs), (
        "Should have 5 docs since only .yml, .png, .js, .md files are included."
        " However, the docs/guides and src/package/subpackage directories are excluded."
    )

    print("Expected docs:")
    for doc in expected_docs:
        print(doc)

    print("Actual docs:")
    for doc in docs:
        print(doc)

    for expected, actual in zip(
        sorted(expected_docs, key=lambda x: x.extra_info["file_name"]),
        sorted(docs, key=lambda x: x.extra_info["file_name"]),
    ):
        assert expected.text == actual.text, (
            "The content of the expected doc and the actual doc should be the same"
            f"Expected: {expected.text}"
            f"Actual: {actual.text}"
        )
        assert expected.extra_info["file_path"] == actual.extra_info["file_path"]
        assert expected.extra_info["file_name"] == actual.extra_info["file_name"]


def test_load_data_with_filters3():
    branch_name = "test-branch-name"
    github_client = get_mocked_github_client()

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner="owner",
        repo="repo",
        verbose=True,
        filter_directories=(
            ["src/package/subpackage", "docs/guides", "src/tests"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        filter_file_extensions=(
            [".png", ".js", ".md"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
    )

    expected_docs = [
        Document(
            text="this is the file content for test_file1.py",
            extra_info={
                "file_path": "src/tests/test_file1.py",
                "file_name": "test_file1.py",
            },
        ),
        Document(
            text="this is the file content for example_subpackage.py",
            extra_info={
                "file_path": "src/package/subpackage/example_subpackage.py",
                "file_name": "example_subpackage.py",
            },
        ),
    ]

    docs = reader.load_data(branch=branch_name)

    assert len(docs) == len(expected_docs), (
        "There are 4 files in total. Only 2 files should pass the filters but"
        f" {len(docs)} files were returned."
    )

    print("Expected docs:")
    for doc in expected_docs:
        print(doc)

    print("Actual docs:")
    for doc in docs:
        print(doc)

    for expected, actual in zip(
        sorted(expected_docs, key=lambda x: x.extra_info["file_name"]),
        sorted(docs, key=lambda x: x.extra_info["file_name"]),
    ):
        assert expected.text == actual.text, (
            "The content of the expected doc and the actual doc should be the same"
            f"Expected: {expected.text}"
            f"Actual: {actual.text}"
        )
        assert expected.extra_info["file_path"] == actual.extra_info["file_path"]
        assert expected.extra_info["file_name"] == actual.extra_info["file_name"]


def test_load_data_with_filters4():
    branch_name = "test-branch-name"
    github_client = get_mocked_github_client()

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner="owner",
        repo="repo",
        verbose=True,
        filter_directories=(
            ["docs/gallery", "src/package/subpackage"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
        filter_file_extensions=(
            [".md", ".yml", ".js"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
    )

    expected_docs = [
        Document(
            text="this is the file content for settings.json",
            extra_info={
                "file_path": ".vscode/settings.json",
                "file_name": "settings.json",
            },
        ),
        Document(
            text="this is the file content for index.rst",
            extra_info={
                "file_path": "docs/index.rst",
                "file_name": "index.rst",
            },
        ),
        Document(
            text="this is the file content for test_file1.py",
            extra_info={
                "file_path": "src/tests/test_file1.py",
                "file_name": "test_file1.py",
            },
        ),
        Document(
            text="this is the file content for setup.py",
            extra_info={
                "file_path": "setup.py",
                "file_name": "setup.py",
            },
        ),
        Document(
            text="this is the file content for example_package.py",
            extra_info={
                "file_path": "src/package/example_package.py",
                "file_name": "example_package.py",
            },
        ),
        Document(
            text="this is the file content for __init__.py",
            extra_info={
                "file_path": "src/__init__.py",
                "file_name": "__init__.py",
            },
        ),
        Document(
            text="this is the file content for LICENSE",
            extra_info={
                "file_path": "LICENSE",
                "file_name": "LICENSE",
            },
        ),
    ]

    docs = reader.load_data(branch=branch_name)

    assert len(docs) == len(expected_docs), (
        "There are 7 files in total. Only 7 files should pass the filters but"
        f" {len(docs)} files were returned."
    )

    print("Expected docs:")
    for doc in expected_docs:
        print(doc)

    print("Actual docs:")
    for doc in docs:
        print(doc)

    for expected, actual in zip(
        sorted(expected_docs, key=lambda x: x.extra_info["file_name"]),
        sorted(docs, key=lambda x: x.extra_info["file_name"]),
    ):
        assert expected.text == actual.text, (
            "The content of the expected doc and the actual doc should be the same"
            f"Expected: {expected.text}"
            f"Actual: {actual.text}"
        )
        assert expected.extra_info["file_path"] == actual.extra_info["file_path"]
        assert expected.extra_info["file_name"] == actual.extra_info["file_name"]
