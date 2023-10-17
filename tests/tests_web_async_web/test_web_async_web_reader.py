import unittest

import pytest
from werkzeug.wrappers import Request, Response

from llama_hub.web.async_web.base import AsyncWebPageReader


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("localhost", 8888)


TEST_URL = "http://localhost:8888/primary.xml"
TEST_URL_OTHER = "http://localhost:8888/other.xml"
TEST_URL_ERROR = "http://localhost:8888/failme"


class TestAsyncWebPageReader(unittest.TestCase):
    def failme_handler(self, response: Request):
        return Response("Boo!", status=500)

    @pytest.fixture(autouse=True)
    def setup(self, httpserver):
        httpserver.expect_request("/other.xml", method="GET").respond_with_data(
            "Some big data chunk!"
        )
        httpserver.expect_request("/failme", method="GET").respond_with_handler(
            self.failme_handler
        )
        httpserver.expect_request("/primary.xml", method="GET").respond_with_data(
            "Some big data chunk!"
        )

    def test_async_web_reader_init(self):
        # test w/o args
        AsyncWebPageReader()

        # test w args
        AsyncWebPageReader(html_to_text=True, limit=50)

    def test_async_web_reader_load_data_invalid_args(self):
        reader = AsyncWebPageReader()

        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'urls'",
        ):
            reader.load_data()

    def test_async_web_reader_load_data(self):
        reader = AsyncWebPageReader()

        documents = reader.load_data(urls=[TEST_URL])

        assert len(documents) == 1
        assert documents[0].text == "Some big data chunk!"
        assert documents[0].extra_info["Source"] == "http://localhost:8888/primary.xml"

    def test_async_web_reader_load_data_consume_error(self):
        reader = AsyncWebPageReader()

        documents = reader.load_data(urls=[TEST_URL_ERROR])

        assert len(documents) == 0

    def test_async_web_reader_load_data_raise_error(self):
        reader = AsyncWebPageReader(fail_on_error=True)

        with pytest.raises(
            ValueError,
            match=(
                "error fetching page from http://localhost:8888/failme. server returned"
                " status: 500 and response Boo!"
            ),
        ):
            reader.load_data(urls=[TEST_URL_ERROR])

    def test_async_web_reader_load_data_dedupe(self):
        reader = AsyncWebPageReader(dedupe=True)

        documents = reader.load_data(urls=[TEST_URL, TEST_URL_OTHER, TEST_URL])

        assert len(documents) == 2
        assert documents[0].text == "Some big data chunk!"
        assert documents[0].extra_info["Source"] == "http://localhost:8888/primary.xml"
        assert documents[1].text == "Some big data chunk!"
        assert documents[1].extra_info["Source"] == "http://localhost:8888/other.xml"
