import pytest
from unittest.mock import patch
from llama_hub.snowflake.base import SnowflakeReader
from llama_index.readers.schema.base import Document

# Test initialization with connection details
@patch("llama_hub.snowflake.base.create_engine")  # Patch the create_engine function
def test_init_with_connection_details(mock_create_engine):
    engine = "mock_engine"
    mock_create_engine.return_value = engine

    reader = SnowflakeReader(
        account="account",
        user="user",
        password="password",
        database="database",
        schema="schema",
        warehouse="warehouse",
    )

    mock_create_engine.assert_called_once()
    assert reader.engine == engine


# Test load_data method
@patch("llama_hub.snowflake.base.SnowflakeReader.execute_query")
def test_load_data(mock_execute_query):
    # Simulate query execution result
    mock_execute_query.return_value = [("row1",), ("row2",)]

    reader = SnowflakeReader()
    documents = reader.load_data("SELECT * FROM table")

    assert len(documents) == 2
    assert isinstance(documents[0], Document)
    assert documents[0].text == "row1"
    assert documents[1].text == "row2"


# Test load_data method with no query
def test_load_data_with_no_query():
    reader = SnowflakeReader()
    with pytest.raises(ValueError):
        reader.load_data(None)
