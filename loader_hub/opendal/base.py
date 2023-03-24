"""Opendal file and directory reader.

A loader that fetches a file or iterates through a directory on AWS S3 or other compatible service.

"""
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import asyncio

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import opendal

class OpendalReader(BaseReader):
    """General reader for any opendal operator."""

    def __init__(
        self,
        *args: Any,
        scheme: str,
        path: Optional[str] = None,
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize opendal operator, along with credentials if needed.


        Args:
        scheme (str): the scheme of the service
        path (Optional[str]): the path of the data. If none is provided,
            this loader will iterate through the entire bucket. If path is endswith `/`, this loader will iterate through the entire dir. Otherwise, this loeader will load the file.
        file_extractor (Optional[Dict[str, BaseParser]]): A mapping of file
            extension to a BaseParser class that specifies how to convert that file
            to text. See `SimpleDirectoryReader` for more details.
        """
        super().__init__(*args, **kwargs)

        self.path = path
        self.file_extractor = file_extractor

        self.op = opendal.AsyncOperator(scheme, **kwargs)

    def load_data(self) -> List[Document]:
        """Load file(s) from OpenDAL."""

        with tempfile.TemporaryDirectory() as temp_dir:
            if not self.path.endswith("/"):
                asyncio.run(download_file_from_opendal(self.op, temp_dir, self.path))
            else:
                for obj in self.op.scan(self.path):
                    asyncio.run(download_file_from_opendal(self.op, temp_dir, obj.path))

            SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
            loader = SimpleDirectoryReader(temp_dir, file_extractor=self.file_extractor)

            return loader.load_data()


async def download_file_from_opendal(
    op: opendal.AsyncOperator, temp_dir: str, path: str
) -> str:
    """Download file from OpenDAL."""

    suffix = Path(path).suffix
    filepath = f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"

    with op.open_reader(path) as r:
        with open(filepath, "wb") as w:
            w.write(await r.read())

    return filepath
