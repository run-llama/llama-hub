import pytest
import unittest
from unittest.mock import patch
from llama_hub.confluence.base import ConfluenceReader, Document


@pytest.fixture
def mock_confluence():
    with patch("atlassian.Confluence") as mock_confluence:
        yield mock_confluence


CONFLUENCE_BASE_URL = "https://example.atlassian.com/wiki"
MOCK_OAUTH = {
    "client_id": "your_client_id",
    "token": {
        "access_token": "your_access_token",
        "token_type": "Bearer",
    },
}


class TestConfluenceReader:
    def test_confluence_reader_initialization(self, mock_confluence):

        # Test with oauth2
        ConfluenceReader(base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH)
        mock_confluence.assert_called_once_with(
            url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH, cloud=True
        )

        # Test without oauth2
        with unittest.mock.patch.dict(
            "os.environ",
            {"CONFLUENCE_USERNAME": "user", "CONFLUENCE_API_TOKEN": "api_token"},
        ):
            ConfluenceReader(base_url=CONFLUENCE_BASE_URL)
            mock_confluence.assert_called_with(
                url=CONFLUENCE_BASE_URL,
                username="user",
                password="api_token",
                cloud=True,
            )

    def test_confluence_reader_load_data_invalid_args(self, mock_confluence):
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        with pytest.raises(
            ValueError,
            match="Must specify at least one among `space_key`, `page_ids`, `label`, `cql` parameters.",
        ):
            confluence_reader.load_data()

    def test_confluence_reader_load_data_by_page_ids(self, mock_confluence):
        mock_confluence.get_page_by_id.side_effect = [
            {
                "id": "123",
                "title": "Page 123",
                "body": {"storage": {"value": "<p>Content 123</p>"}},
            },
            {
                "id": "456",
                "title": "Page 456",
                "body": {"storage": {"value": "<p>Content 456</p>"}},
            },
        ]

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["123", "456"]
        documents = confluence_reader.load_data(page_ids=mock_page_ids)

        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].doc_id == "123"
        assert documents[0].extra_info == {"title": "Page 123"}
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {"title": "Page 456"}

        assert mock_confluence.get_page_by_id.call_count == 2

        assert mock_confluence.get_all_pages_from_space.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0

    def test_confluence_reader_load_data_by_space_id(self, mock_confluence):
        # one response with two pages
        mock_confluence.get_all_pages_from_space.return_value = [
            {
                "id": "123",
                "type": "page",
                "status": "current",
                "title": "Page 123",
                "body": {"storage": {"value": "<p>Content 123</p>"}},
            },
            {
                "id": "456",
                "type": "page",
                "status": "current",
                "title": "Page 456",
                "body": {"storage": {"value": "<p>Content 456</p>"}},
            },
        ]

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        documents = confluence_reader.load_data(space_key=mock_space_key)

        assert mock_confluence.get_all_pages_from_space.call_count == 1
        assert mock_confluence.get_all_pages_from_space.call_args[0][0] == "spaceId123"
        assert mock_confluence.get_all_pages_from_space.call_args[1]["start"] == 0
        assert mock_confluence.get_all_pages_from_space.call_args[1]["limit"] == 50

        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].doc_id == "123"
        assert documents[0].extra_info == {"title": "Page 123"}
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {"title": "Page 456"}

        assert mock_confluence.get_page_by_id.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0

    def test_confluence_reader_load_data_by_space_id_pagination(self, mock_confluence):
        # two api responses with one page each
        mock_confluence.get_all_pages_from_space.side_effect = [
            [
                {
                    "id": "123",
                    "type": "page",
                    "status": "current",
                    "title": "Page 123",
                    "body": {"storage": {"value": "<p>Content 123</p>"}},
                },
            ],
            [
                {
                    "id": "456",
                    "type": "page",
                    "status": "current",
                    "title": "Page 456",
                    "body": {"storage": {"value": "<p>Content 456</p>"}},
                }
            ],
            [],
        ]

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        mock_limit = 1  # fetch one page at a time
        documents = confluence_reader.load_data(
            space_key=mock_space_key, limit=mock_limit
        )

        assert mock_confluence.get_all_pages_from_space.call_count == 3

        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].doc_id == "123"
        assert documents[0].extra_info == {"title": "Page 123"}
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {"title": "Page 456"}

        assert mock_confluence.get_page_by_id.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0
