import unittest
from unittest.mock import patch, call
from typing import List

from llama_index.readers.schema.base import Document

from llama_hub.stripe_docs import StripeDocsReader

MOCK_URL = "https://stripe.com/sitemap/sitemap.xml"


def get_sitemap(file: str):
    f = open(file, "r")
    return f.read()


def dummy_load_pages(urls: List[str]):
    documents = []
    for u in urls:
        documents.append(Document(text="Bla", extra_info={"Source": u}))
    return documents


class TestSitemapReader(unittest.TestCase):
    def test_stripe_docs_reader_init(self):
        # works without args
        StripeDocsReader()

        # works with args
        StripeDocsReader(html_to_text=True, limit=50)

    @patch("llama_hub.web.async_web.base.AsyncWebPageReader.load_data")
    def test_stripe_docs_reader_load_data(self, mock_load_data):
        with patch("urllib.request.urlopen") as mock_urlopen:
            stripe_docs_reader = StripeDocsReader()

            # mock url calls
            mock_response = mock_urlopen.return_value
            mock_response.read.side_effect = [
                get_sitemap("tests/tests_stripe_docs/test_stripe_sitemap.xml"),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_0.xml"
                ),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_1.xml"
                ),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_2.xml"
                ),
            ]

            mock_load_data.side_effect = dummy_load_pages

            documents = stripe_docs_reader.load_data()

            mock_urlopen_calls = [
                call("https://stripe.com/sitemap/sitemap.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-0.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-1.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-2.xml"),
                call().read(),
            ]

            mock_urlopen.assert_has_calls(mock_urlopen_calls)

            assert mock_load_data.call_count == 1
            assert len(documents) == 1264

    @patch("llama_hub.web.async_web.base.AsyncWebPageReader.load_data")
    def test_sitemap_reader_load_data_with_filter(self, mock_load_data):
        with patch("urllib.request.urlopen") as mock_urlopen:
            stripe_docs_reader = StripeDocsReader()

            # mock url calls
            mock_response = mock_urlopen.return_value
            mock_response.read.side_effect = [
                get_sitemap("tests/tests_stripe_docs/test_stripe_sitemap.xml"),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_0.xml"
                ),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_1.xml"
                ),
                get_sitemap(
                    "tests/tests_stripe_docs/test_stripe_sitemap_partition_2.xml"
                ),
            ]

            mock_load_data.side_effect = dummy_load_pages

            documents = stripe_docs_reader.load_data(
                filters=["/docs/billing"],
            )

            mock_urlopen_calls = [
                call("https://stripe.com/sitemap/sitemap.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-0.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-1.xml"),
                call().read(),
                call("https://stripe.com/sitemap/partition-2.xml"),
                call().read(),
            ]

            mock_urlopen.assert_has_calls(mock_urlopen_calls)

            assert mock_load_data.call_count == 1

            assert len(documents) == 66
            assert (
                documents[0].extra_info["Source"]
                == "https://stripe.com/docs/billing/billing-apis"
            )
            assert (
                documents[1].extra_info["Source"]
                == "https://stripe.com/docs/billing/collection-method"
            )
