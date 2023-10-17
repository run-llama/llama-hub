import asyncio
from typing import List, Tuple

import pytest

from llama_hub.github_repo.github_client import GitTreeResponseModel
from llama_hub.github_repo.utils import (
    BufferedAsyncIterator,
    BufferedGitBlobDataIterator,
)

# Remove this to test changes to GithubRepositoryReader.
# pytest.skip(
#     "Skip by default due to dependence on network request and github api token.",
#     allow_module_level=True,
# )


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
