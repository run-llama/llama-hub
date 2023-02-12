from loader_hub.github_repo.base import GithubRepositoryReader
from loader_hub.github_repo.github_client import GithubClient

import pytest


def test_github_reader():
    """Test the Github reader."""

    github_client = GithubClient(verbose=True)
    

    loader = GithubRepositoryReader(
        github_client=github_client,
        owner="jerryjliu",
        repo="gpt_index",
        use_parser=False,
        verbose=True,
        filter_directories=(
            ["docs"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        filter_file_extensions=(
            [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", "json", ".ipynb"],
            GithubRepositoryReader.FilterType.EXCLUDE,
        ),
    )

    docs = loader.load_data(branch="main")
    for doc in docs:
        fp: str = doc.extra_info["file_path"]
        assert fp.startswith("docs"), f"File path {fp} does not start with docs"
        assert (
            not fp.endswith(".png")
            and not fp.endswith(".jpg")
            and not fp.endswith(".jpeg")
            and not fp.endswith(".gif")
            and not fp.endswith(".svg")
            and not fp.endswith(".ico")
            and not fp.endswith("json")
            and not fp.endswith(".ipynb")
        ), f"File path {fp} ends with an excluded extension"

        print(doc.extra_info)
