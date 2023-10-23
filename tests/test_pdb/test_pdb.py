import pytest
from llama_hub.pdb.base import PdbAbstractReader
from llama_index.readers.schema.base import Document


@pytest.mark.parametrize("pdb_ids", [["1cbs", "125L"]])  # Example PDB ids to test
def test_load_data(pdb_ids):
    # Create an instance of the PdbAbstractReader class
    reader = PdbAbstractReader()

    # Call the load_data method with the test PDB ids
    documents = reader.load_data(pdb_ids)

    # Assert that the returned documents have the expected structure
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)
    assert all(doc.text is not None for doc in documents)
    assert all(isinstance(doc.extra_info, dict) for doc in documents)
    assert all("pdb_id" in doc.extra_info for doc in documents)
    assert all("primary_citation" in doc.extra_info for doc in documents)
