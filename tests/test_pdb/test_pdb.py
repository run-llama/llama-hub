import unittest.mock
import pytest
from llama_hub.pdb.base import PdbAbstractReader
from llama_index.readers.schema.base import Document


@pytest.mark.parametrize("pdb_ids", [["1cbs"]])  # Example PDB ids to test
def test_load_data(pdb_ids):
    # Create an instance of the PdbAbstractReader class
    reader = PdbAbstractReader()

    # Mock the HTTP request
    with unittest.mock.patch("llama_hub.pdb.utils.requests.get") as mock_get:
        # Configure the mock response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "1cbs": [
                {
                    "title": "Example title",
                    "doi": "Example doi",
                    "abstract": {"example abstract section": "example text"},
                }
            ]
        }

        # Call the load_data method with the test PDB ids
        documents = reader.load_data(pdb_ids)

        # Assert that the returned documents have the expected structure
        assert isinstance(documents, list)
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(doc.text is not None for doc in documents)
        assert all(isinstance(doc.extra_info, dict) for doc in documents)
        assert all("pdb_id" in doc.extra_info for doc in documents)
        assert all("primary_citation" in doc.extra_info for doc in documents)
