import json
import pytest

from llama_hub.file.json import JSONReader

# Sample JSON data for testing
SAMPLE_JSON = {
    "name": "John Doe",
    "age": 30,
    "address": {"street": "123 Main St", "city": "Anytown", "state": "CA"},
}

SAMPLE_JSONL = [json.dumps(SAMPLE_JSON), json.dumps({"name": "Jane Doe", "age": 25})]


# Fixture to create a temporary JSON file
@pytest.fixture
def json_file(tmp_path):
    file = tmp_path / "test.json"
    with open(file, "w") as f:
        json.dump(SAMPLE_JSON, f)
    return file


# Fixture to create a temporary JSONL file
@pytest.fixture
def jsonl_file(tmp_path):
    file = tmp_path / "test.jsonl"
    with open(file, "w") as f:
        f.write("\n".join(SAMPLE_JSONL))
    return file


def test_json_reader_init():
    reader = JSONReader(levels_back=2)
    assert reader.levels_back == 2


def test_parse_jsonobj_to_document():
    reader = JSONReader()
    document = reader._parse_jsonobj_to_document(SAMPLE_JSON)
    assert "John Doe" in document.text
    assert "30" in document.text


def test_load_data_json(json_file):
    reader = JSONReader()
    documents = reader.load_data(json_file)
    assert len(documents) == 1
    assert "John Doe" in documents[0].text
    assert "123 Main St" in documents[0].text


def test_load_data_jsonl(jsonl_file):
    reader = JSONReader()
    documents = reader.load_data(jsonl_file, is_jsonl=True)
    assert len(documents) == 2
    assert "Jane Doe" in documents[1].text
    assert "25" in documents[1].text
