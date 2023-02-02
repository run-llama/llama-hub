from loader_hub.google_docs.base import GoogleDocsReader
from loader_hub.file.base import SimpleDirectoryReader
from loader_hub.web.simple_web.base import SimpleWebPageReader
from loader_hub.web.beautiful_soup_web.base import (
    BeautifulSoupWebReader,
)  # thejessezhang
from loader_hub.web.trafilatura_web.base import TrafilaturaWebReader

__all__ = [
    "GoogleDocsReader",
    "SimpleDirectoryReader",
    "SimpleWebPageReader",
    "BeautifulSoupWebReader",
    "TrafilaturaWebReader",
]
