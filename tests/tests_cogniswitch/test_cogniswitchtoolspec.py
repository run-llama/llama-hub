import requests
from unittest.mock import Mock
from llama_hub.tools.cogniswitch import CogniswitchToolSpec

# Define some sample data for testing
sample_cs_token = "cs_token"
sample_oai_token = "oai_token"
sample_api_key = "api_key"
sample_url = "https://example.com"
sample_document_name = "Test Document"
sample_document_description = "Test Document Description"
sample_query = "Test Query"


# Create a mock response object for the requests.post method
class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


# Test the CogniswitchToolSpec class
def test_cogniswitch_tool_spec():
    # Initialize the CogniswitchToolSpec instance
    tool_spec = CogniswitchToolSpec(sample_cs_token, sample_oai_token, sample_api_key)

    # Mock the requests.post method
    requests.post = Mock()

    # Test store_data method when providing a URL
    requests.post.return_value = MockResponse(200, {"result": "Stored using URL"})
    result = tool_spec.store_data(
        url=sample_url,
        document_name=sample_document_name,
        document_description=sample_document_description,
    )
    assert result == {"result": "Stored using URL"}

    # Test query_knowledge method
    requests.post.return_value = MockResponse(200, {"response": "Query response"})
    result = tool_spec.query_knowledge(sample_query)
    assert result == {"response": "Query response"}

    # Test store_data and query_knowledge methods for error case (status_code != 200)
    requests.post.return_value = MockResponse(400, {"message": "Bad Request"})
    result = tool_spec.store_data(
        url=sample_url,
        document_name=sample_document_name,
        document_description=sample_document_description,
    )
    assert result == {"message": "Bad Request"}

    requests.post.return_value = MockResponse(400, {"message": "Bad Request"})
    result = tool_spec.query_knowledge(sample_query)
    assert result == {"message": "Bad Request"}

    # Clean up the mock
    requests.post = Mock()
