import pytest

# Remove this to test changes to GithubRepositoryReader.
pytest.skip(
    "Skip by default due to dependence on network request and github api token.",
    allow_module_level=True,
)
