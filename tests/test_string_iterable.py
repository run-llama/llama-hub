"""Check that the string iterable loader is working as expected."""

from ..loader_hub.string_iterable import StringIterableReader


def test_string_iterable() -> None:
    """Check that StringIterableReader works correctly."""
    reader = StringIterableReader()
    documents = reader.load_data(texts=["I went to the store", "I bought an apple"])
    assert len(documents) == 2
