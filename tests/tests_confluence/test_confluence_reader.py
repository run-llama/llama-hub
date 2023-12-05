import unittest
from unittest.mock import patch

import pytest

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
    def setup_method(self):
        import sys

        sys.modules["atlassian"] = unittest.mock.MagicMock()

    def teardown_method(self):
        import sys

        del sys.modules["atlassian"]

    def test_confluence_reader_initialization(self, mock_confluence):
        # Test with oauth2
        ConfluenceReader(base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH)
        mock_confluence.assert_called_with(
            url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH, cloud=True
        )

        # Test with oauth2 and not cloud
        ConfluenceReader(base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH, cloud=False)
        mock_confluence.assert_called_with(
            url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH, cloud=False
        )

        # Test with api token
        with unittest.mock.patch.dict(
            "os.environ",
            {"CONFLUENCE_API_TOKEN": "api_token"},
        ):
            ConfluenceReader(base_url=CONFLUENCE_BASE_URL)
            mock_confluence.assert_called_with(
                url=CONFLUENCE_BASE_URL,
                token="api_token",
                cloud=True,
            )

        # Test with basic auth
        with unittest.mock.patch.dict(
            "os.environ",
            {"CONFLUENCE_USERNAME": "user", "CONFLUENCE_PASSWORD": "password"},
        ):
            ConfluenceReader(base_url=CONFLUENCE_BASE_URL)
            mock_confluence.assert_called_with(
                url=CONFLUENCE_BASE_URL,
                username="user",
                password="password",
                cloud=True,
            )

    def test_confluence_reader_load_data_invalid_args_no_method(self, mock_confluence):
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        with pytest.raises(
            ValueError,
            match=(
                "Must specify exactly one among `space_key`, `page_ids`, `label`, `cql`"
                " parameters."
            ),
        ):
            confluence_reader.load_data()

    def test_confluence_reader_load_data_invalid_args_multiple_methods(
        self, mock_confluence
    ):
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        with pytest.raises(
            ValueError,
            match=(
                "Must specify exactly one among `space_key`, `page_ids`, `label`, `cql`"
                " parameters."
            ),
        ):
            confluence_reader.load_data(space_key="123", page_ids=["123"])

    def test_confluence_reader_load_data_invalid_args_page_status_no_space_key(
        self, mock_confluence
    ):
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        with pytest.raises(
            ValueError,
            match="Must specify `space_key` when `page_status` is specified.",
        ):
            confluence_reader.load_data(page_status="current", page_ids=["123"])

    def test_confluence_reader_load_data_invalid_args_include_children_page_ids(
        self, mock_confluence
    ):
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        with pytest.raises(
            ValueError,
            match="Must specify `page_ids` when `include_children` is specified.",
        ):
            confluence_reader.load_data(space_key="123", include_children=True)

    def test_confluence_reader_load_data_by_page_ids(self, mock_confluence):
        mock_confluence.get_page_by_id.side_effect = [
            {
                "id": "123",
                "title": "Page 123",
                "body": {"storage": {"value": "<p>Content 123</p>"}},
                "status": "current",
                "_links": {"webui": "/spaces/123/pages/123/Page+123"},
            },
            {
                "id": "456",
                "title": "Page 456",
                "body": {"storage": {"value": "<p>Content 456</p>"}},
                "status": "current",
                "_links": {"webui": "/spaces/456/pages/456/Page+456"},
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
        assert documents[0].extra_info == {
            "title": "Page 123",
            "page_id": "123",
            "status": "current",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/123/pages/123/Page+123",
        }
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {
            "title": "Page 456",
            "page_id": "456",
            "status": "current",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/456/pages/456/Page+456",
        }

        assert mock_confluence.get_page_by_id.call_count == 2

        assert mock_confluence.get_all_pages_from_space.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0

    def test_confluence_reader_load_data_by_space_id(self, mock_confluence):
        # one response with two pages
        mock_confluence.get_all_pages_from_space.side_effect = [
            [
                {
                    "id": "123",
                    "type": "page",
                    "status": "current",
                    "title": "Page 123",
                    "body": {"storage": {"value": "<p>Content 123</p>"}},
                    "_links": {"webui": "/spaces/123/pages/123/Page+123"},
                },
                {
                    "id": "456",
                    "type": "page",
                    "status": "archived",
                    "title": "Page 456",
                    "body": {"storage": {"value": "<p>Content 456</p>"}},
                    "_links": {"webui": "/spaces/456/pages/456/Page+456"},
                },
            ],
            [],
        ]

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        documents = confluence_reader.load_data(
            space_key=mock_space_key, max_num_results=50
        )

        assert mock_confluence.get_all_pages_from_space.call_count == 2
        assert (
            mock_confluence.get_all_pages_from_space.call_args[1]["space"]
            == "spaceId123"
        )
        assert mock_confluence.get_all_pages_from_space.call_args[1]["start"] == 2
        assert mock_confluence.get_all_pages_from_space.call_args[1]["limit"] == 48
        assert mock_confluence.get_all_pages_from_space.call_args[1]["status"] is None
        assert (
            mock_confluence.get_all_pages_from_space.call_args[1]["expand"]
            == "body.storage.value"
        )

        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].doc_id == "123"
        assert documents[0].extra_info == {
            "title": "Page 123",
            "page_id": "123",
            "status": "current",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/123/pages/123/Page+123",
        }
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {
            "title": "Page 456",
            "page_id": "456",
            "status": "archived",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/456/pages/456/Page+456",
        }

        assert mock_confluence.get_page_by_id.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0

    def test_confluence_reader_load_data_by_space_id_pagination(self, mock_confluence):
        """Test pagination where there are more pages to retrieve than the server limit."""
        # two api responses with one page each, due to server limit of 1 page per response.
        # third call returns empty list.
        mock_confluence.get_all_pages_from_space.side_effect = [
            [
                {
                    "id": "123",
                    "type": "page",
                    "status": "current",
                    "title": "Page 123",
                    "body": {"storage": {"value": "<p>Content 123</p>"}},
                    "_links": {"webui": "/spaces/123/pages/123/Page+123"},
                },
            ],
            [
                {
                    "id": "456",
                    "type": "page",
                    "status": "current",
                    "title": "Page 456",
                    "body": {"storage": {"value": "<p>Content 456</p>"}},
                    "_links": {"webui": "/spaces/456/pages/456/Page+456"},
                }
            ],
            [],
        ]

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        mock_max_num_results = 3  # Asking for up to 3 pages. There are only two pages to retrieve though, and they'll come 1 at a time from Confluence.
        documents = confluence_reader.load_data(
            space_key=mock_space_key, max_num_results=mock_max_num_results
        )

        assert mock_confluence.get_all_pages_from_space.call_count == 3

        assert len(documents) == 2
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].doc_id == "123"
        assert documents[0].extra_info == {
            "title": "Page 123",
            "page_id": "123",
            "status": "current",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/123/pages/123/Page+123",
        }
        assert documents[1].doc_id == "456"
        assert documents[1].extra_info == {
            "title": "Page 456",
            "page_id": "456",
            "status": "current",
            "url": f"{CONFLUENCE_BASE_URL}/spaces/456/pages/456/Page+456",
        }

        assert mock_confluence.get_page_by_id.call_count == 0
        assert mock_confluence.get_all_pages_by_label.call_count == 0
        assert mock_confluence.cql.call_count == 0
        assert mock_confluence.get_page_child_by_type.call_count == 0

    def test_confluence_reader_load_data_max_10(self, mock_confluence):
        mock_confluence.get_all_pages_from_space.side_effect = (
            _mock_get_all_pages_from_space
        )

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        mock_max_num_results = 10  # Asking for up to 10 pages. There are only 8 pages to retrieve though, and they'll come 3 at a time from Confluence.
        documents = confluence_reader.load_data(
            space_key=mock_space_key, max_num_results=mock_max_num_results
        )

        # 4 calls are made, returning 3,3,2,0 results, respectively.
        assert mock_confluence.get_all_pages_from_space.call_count == 4
        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        # assert the ith document has id "i"
        assert all(documents[i].doc_id == str(i) for i in range(8))

    def test_confluence_reader_load_data_max_8(self, mock_confluence):
        mock_confluence.get_all_pages_from_space.side_effect = (
            _mock_get_all_pages_from_space
        )

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        mock_max_num_results = 5  # Asking for up to 5 pages. Since there are 8 pages in Confluence we will get 5 requested pages, at most 3 at a time.
        documents = confluence_reader.load_data(
            space_key=mock_space_key, max_num_results=mock_max_num_results
        )

        # 2 calls are made, returning 3,2 results, respectively.
        assert mock_confluence.get_all_pages_from_space.call_count == 2
        assert len(documents) == 5
        assert all(isinstance(doc, Document) for doc in documents)
        # assert the ith document has id "i"
        assert all(documents[i].doc_id == str(i) for i in range(5))

    def test_confluence_reader_load_data_max_5(self, mock_confluence):
        mock_confluence.get_all_pages_from_space.side_effect = (
            _mock_get_all_pages_from_space
        )

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        mock_max_num_results = 5  # Asking for up to 5 pages. Since there are 8 pages in Confluence we will get 5 requested pages, at most 3 at a time.
        documents = confluence_reader.load_data(
            space_key=mock_space_key, max_num_results=mock_max_num_results
        )

        # 2 calls are made, returning 3,2 results, respectively.
        assert mock_confluence.get_all_pages_from_space.call_count == 2
        assert len(documents) == 5
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(documents[i].doc_id == str(i) for i in range(5))

    def test_confluence_reader_load_data_max_none(self, mock_confluence):
        mock_confluence.get_all_pages_from_space.side_effect = (
            _mock_get_all_pages_from_space
        )

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_space_key = "spaceId123"
        # asking for all pages.  They will come at most 3 at a time from Confluence, and there are 8 pages in confluence.
        documents = confluence_reader.load_data(space_key=mock_space_key)

        # 4 calls are made, returning 3,3,2,0 results, respectively.
        assert mock_confluence.get_all_pages_from_space.call_count == 4
        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(documents[i].doc_id == str(i) for i in range(8))

    def test_confluence_reader_load_data_by_page_ids_max_10(self, mock_confluence):
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["0", "1", "2", "3", "4", "5", "6", "7"]
        mock_get_children = False
        mock_max_num_results = (
            10  # Asking for up to 10 pages, but only requesting 8 specific ones.
        )
        documents = confluence_reader.load_data(
            page_ids=mock_page_ids,
            include_children=mock_get_children,
            max_num_results=mock_max_num_results,
        )

        assert mock_confluence.get_page_by_id.call_count == 8
        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        assert [doc.doc_id for doc in documents] == mock_page_ids

    def test_confluence_reader_load_data_by_page_ids_max_5(self, mock_confluence):
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["0", "1", "2", "3", "4", "5", "6", "7"]
        mock_get_children = False
        mock_max_num_results = 5  # Asking for up to 5 pages
        documents = confluence_reader.load_data(
            page_ids=mock_page_ids,
            include_children=mock_get_children,
            max_num_results=mock_max_num_results,
        )

        assert mock_confluence.get_page_by_id.call_count == 5
        assert len(documents) == 5
        assert all(isinstance(doc, Document) for doc in documents)
        assert [doc.doc_id for doc in documents] == mock_page_ids[:5]

    def test_confluence_reader_load_data_by_page_ids_max_5_2(self, mock_confluence):
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["0", "1", "2", "3", "4", "5", "6", "7"]
        mock_get_children = False
        mock_max_num_results = None
        documents = confluence_reader.load_data(
            page_ids=mock_page_ids,
            include_children=mock_get_children,
            max_num_results=mock_max_num_results,
        )

        assert mock_confluence.get_page_by_id.call_count == 8
        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        assert [doc.doc_id for doc in documents] == mock_page_ids

    def test_confluence_reader_load_data_dfs(self, mock_confluence):
        mock_confluence.get_child_id_list.side_effect = _mock_get_child_id_list
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_id = "0"
        mock_get_children = True
        documents = confluence_reader.load_data(
            page_ids=[mock_page_id], include_children=mock_get_children
        )

        # {"0": ["1", "2", "3"], "1": ["4", "5"], "2": ["6"], "4": ["7"]}
        # 12 calls are made.  2 calls for each page that has children (0,1,2,4), 1 call for each page that does not have children (3,5,6,7).
        assert mock_confluence.get_child_id_list.call_count == 12
        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        # Check that it's actually DFS
        actual_doc_ids = [doc.doc_id for doc in documents]
        assert actual_doc_ids == ["0", "1", "4", "7", "5", "2", "6", "3"]

    def test_confluence_reader_load_data_dfs_repeated_pages(self, mock_confluence):
        mock_confluence.get_child_id_list.side_effect = _mock_get_child_id_list
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["0", "2"]
        mock_get_children = True
        documents = confluence_reader.load_data(
            page_ids=mock_page_ids, include_children=mock_get_children
        )

        # {"0": ["1", "2", "3"], "1": ["4", "5"], "2": ["6"], "4": ["7"]}
        # 12 calls are made for page_id "0".  2 calls for each page that has children (0,1,2,4), 1 call for each page that does not have children (3,5,6,7).
        # 3 calls are mode for page_id "2" (same logic as above)
        assert mock_confluence.get_child_id_list.call_count == 15
        # although there are only 8 documents on the server, we implicitly asked for some repeated documents, "2" and "6", so we should have 10 docs now.
        assert len(documents) == 10
        assert all(isinstance(doc, Document) for doc in documents)
        # Check that it's actually DFS
        actual_doc_ids = [doc.doc_id for doc in documents]
        assert actual_doc_ids == ["0", "1", "4", "7", "5", "2", "6", "3", "2", "6"]

    def test_confluence_reader_load_data_dfs_max_6(self, mock_confluence):
        mock_confluence.get_child_id_list.side_effect = _mock_get_child_id_list
        mock_confluence.get_page_by_id.side_effect = lambda page_id, expand: {
            "id": str(page_id),
            "type": "page",
            "status": "current",
            "title": f"Page {page_id}",
            "body": {"storage": {"value": f"<p>Content {page_id}</p>"}},
            "_links": {"webui": f"/spaces/{page_id}/pages/{page_id}/Page+{page_id}"},
        }

        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_page_ids = ["0", "2"]
        mock_get_children = True
        mock_max_num_results = 6
        documents = confluence_reader.load_data(
            page_ids=mock_page_ids,
            include_children=mock_get_children,
            max_num_results=mock_max_num_results,
        )

        # {"0": ["1", "2", "3"], "1": ["4", "5"], "2": ["6"], "4": ["7"]}
        # calls made to get_child_id_list for DFS on page_id "0":  0, 0, 1, 1, 4, 4, 7, 5.
        # That brings us to 6 ids, so we stop.  We didn't call for get_child_id_list for page_id "2".
        # Once page_id "0" is retrieved we have achieved the max number of documents, so we stop and do not call again for page_id "2"
        assert mock_confluence.get_child_id_list.call_count == 8
        # although there are only 8 documents on the server, we implicitly asked for some repeated documents, "2" and "6", so we should have 10 docs now.
        assert len(documents) == 6
        assert all(isinstance(doc, Document) for doc in documents)
        # Check that it's actually DFS
        actual_doc_ids = [doc.doc_id for doc in documents]
        assert actual_doc_ids == ["0", "1", "4", "7", "5", "2"]

    def test_confluence_reader_load_data_cql_paging_max_none(self, mock_confluence):
        mock_confluence.get.side_effect = [
            {
                "results": [
                    {
                        "id": "0",
                        "type": "page",
                        "title": "Page 0",
                        "body": {"storage": {"value": "<p>Content 0</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/0/pages/0/Page+0"},
                    },
                    {
                        "id": "1",
                        "type": "page",
                        "title": "Page 1",
                        "body": {"storage": {"value": "<p>Content 1</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/1/pages/1/Page+1"},
                    },
                    {
                        "id": "2",
                        "type": "page",
                        "title": "Page 2",
                        "body": {"storage": {"value": "<p>Content 2</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/2/pages/2/Page+2"},
                    },
                ],
                "_links": {
                    "next": "http://example.com/rest/api/content?cql=type%3Dpage&limit=3&start=3&cursor=RANDOMSTRING"
                },
            },
            {
                "results": [
                    {
                        "id": "3",
                        "type": "page",
                        "title": "Page 3",
                        "body": {"storage": {"value": "<p>Content 3</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/3/pages/3/Page+3"},
                    },
                    {
                        "id": "4",
                        "type": "page",
                        "title": "Page 4",
                        "body": {"storage": {"value": "<p>Content 4</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/4/pages/4/Page+4"},
                    },
                    {
                        "id": "5",
                        "type": "page",
                        "title": "Page 5",
                        "body": {"storage": {"value": "<p>Content 5</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/5/pages/5/Page+5"},
                    },
                ],
                "_links": {
                    "next": "http://example.com/rest/api/content?cql=type%3Dpage&limit=3&start=6&cursor=RANDOMSTRING"
                },
            },
            {
                "results": [
                    {
                        "id": "6",
                        "type": "page",
                        "title": "Page 6",
                        "body": {"storage": {"value": "<p>Content 6</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/6/pages/6/Page+6"},
                    },
                    {
                        "id": "7",
                        "type": "page",
                        "title": "Page 7",
                        "body": {"storage": {"value": "<p>Content 7</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/7/pages/7/Page+7"},
                    },
                ],
                "_links": {},
            },
        ]
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_cql = "type=page"
        documents = confluence_reader.load_data(cql=mock_cql)

        assert mock_confluence.get.call_count == 3

        assert len(documents) == 8
        assert all(isinstance(doc, Document) for doc in documents)
        assert [doc.doc_id for doc in documents] == [str(i) for i in range(8)]

    def test_confluence_reader_load_data_cql_paging_max_6(self, mock_confluence):
        mock_confluence.get.side_effect = [
            {
                "results": [
                    {
                        "id": "0",
                        "type": "page",
                        "title": "Page 0",
                        "body": {"storage": {"value": "<p>Content 0</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/0/pages/0/Page+0"},
                    },
                    {
                        "id": "1",
                        "type": "page",
                        "title": "Page 1",
                        "body": {"storage": {"value": "<p>Content 1</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/1/pages/1/Page+1"},
                    },
                    {
                        "id": "2",
                        "type": "page",
                        "title": "Page 2",
                        "body": {"storage": {"value": "<p>Content 2</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/2/pages/2/Page+2"},
                    },
                ],
                "_links": {
                    "next": "http://example.com/rest/api/content?cql=type%3Dpage&limit=3&start=3&cursor=RANDOMSTRING"
                },
            },
            {
                "results": [
                    {
                        "id": "3",
                        "type": "page",
                        "title": "Page 3",
                        "body": {"storage": {"value": "<p>Content 3</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/3/pages/3/Page+3"},
                    },
                    {
                        "id": "4",
                        "type": "page",
                        "title": "Page 4",
                        "body": {"storage": {"value": "<p>Content 4</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/4/pages/4/Page+4"},
                    },
                    {
                        "id": "5",
                        "type": "page",
                        "title": "Page 5",
                        "body": {"storage": {"value": "<p>Content 5</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/5/pages/5/Page+5"},
                    },
                ],
                "_links": {
                    "next": "http://example.com/rest/api/content?cql=type%3Dpage&limit=3&start=6&cursor=RANDOMSTRING"
                },
            },
            {
                "results": [
                    {
                        "id": "6",
                        "type": "page",
                        "title": "Page 6",
                        "body": {"storage": {"value": "<p>Content 6</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/6/pages/6/Page+6"},
                    },
                    {
                        "id": "7",
                        "type": "page",
                        "title": "Page 7",
                        "body": {"storage": {"value": "<p>Content 7</p>"}},
                        "status": "current",
                        "_links": {"webui": "/spaces/7/pages/7/Page+7"},
                    },
                ],
                "_links": {},
            },
        ]
        confluence_reader = ConfluenceReader(
            base_url=CONFLUENCE_BASE_URL, oauth2=MOCK_OAUTH
        )
        confluence_reader.confluence = mock_confluence

        mock_cql = "type=page"
        mock_max_num_results = 6
        documents = confluence_reader.load_data(
            cql=mock_cql, max_num_results=mock_max_num_results
        )

        assert mock_confluence.get.call_count == 2

        assert len(documents) == 6
        assert all(isinstance(doc, Document) for doc in documents)
        assert [doc.doc_id for doc in documents] == [str(i) for i in range(6)]


def _mock_get_all_pages_from_space(
    space,
    start=0,
    limit=3,
    status="current",
    expand="body.storage.value",
    content_type="page",
):
    """Mock the API results from a Confluence server that has 8 pages in a space, and a server limit of 3 results per call."""
    server_limit = 3
    num_pages_on_server = 8
    return [
        {
            "id": str(i),
            "type": "page",
            "status": "current",
            "title": f"Page {i}",
            "body": {"storage": {"value": f"<p>Content {i}</p>"}},
            "_links": {"webui": f"/spaces/{i}/pages/{i}/Page+{i}"},
        }
        for i in range(
            start,
            min(start + min(server_limit, limit or server_limit), num_pages_on_server),
        )
    ]


def _mock_get_child_id_list(
    page_id, type="page", start=0, limit=3, expand="body.storage.value"
):
    """Mock the API results from a Confluence server that has 3 child pages for each page."""
    server_limit = 3
    child_ids_by_page_id = {
        "0": ["1", "2", "3"],
        "1": ["4", "5"],
        "2": ["6"],
        "4": ["7"],
    }
    ret = child_ids_by_page_id.get(page_id, [])
    return ret[start : start + min(server_limit, limit or server_limit)]
