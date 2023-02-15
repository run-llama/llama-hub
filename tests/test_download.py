"""Check that downloading loaders from GPT Index is working as expected."""

from gpt_index import download_loader


def test_download_loader() -> None:
    """Check that gpt_index.download_loader works correctly."""

    StringIterableReader = download_loader("StringIterableReader")
    reader = StringIterableReader()
    documents = reader.load_data(texts=["I went to the store", "I bought an apple"])
    assert len(documents) == 2
