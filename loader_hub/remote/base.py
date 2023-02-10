"""Remote file reader.

A loader that fetches an arbitrary remote page or file by URL and parses its contents.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from gpt_index import download_loader
from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class RemoteReader(BaseReader):
    """General reader for any remote page or file."""

    def __init__(
        self,
        *args: Any,
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

        self.file_extractor = file_extractor

    def load_data(self, url: str) -> List[Document]:
        """Parse whatever is at the URL."""
        import tempfile
        from urllib.parse import urlparse
        from urllib.request import urlopen

        extra_info = {"Source": url}

        result = urlopen(url)
        url_type = result.info().get_content_type()
        documents = []
        if url_type == "text/html" or url_type == "text/plain":
            text = "\n\n".join([str(el.decode("utf-8-sig")) for el in result])
            documents = [Document(text, extra_info=extra_info)]
        else:
            suffix = Path(urlparse(url).path).suffix
            with tempfile.TemporaryDirectory() as temp_dir:
                filepath = f"{temp_dir}/temp{suffix}"
                with open(filepath, "wb") as output:
                    output.write(result.read())

                SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
                loader = SimpleDirectoryReader(
                    temp_dir,
                    file_metadata=(lambda _: extra_info),
                    file_extractor=self.file_extractor,
                )
                documents = loader.load_data()
        return documents
