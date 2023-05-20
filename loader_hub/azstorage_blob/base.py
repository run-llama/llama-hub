"""Azure Storage Blob file and directory reader.

A loader that fetches a file or iterates through a directory from Azure Storage Blob.

"""
import logging
import tempfile
import time
import math
from pathlib import Path
from typing import Any, List, Optional, Union, Dict

from azure.core.credentials import AzureNamedKeyCredential, AzureSasCredential, TokenCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

class AzStorageBlobReader(BaseReader):
    """General reader for any Azure Storage Blob file or directory.

    Args:
        service_name
    
    """

    def __init__(
        self,
        *args: Any,
        container_name: str,
        blob: Optional[str] = None,
        name_starts_with: Union[str, None] = None,
        include: Union[str, List[str], None] = None, 
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        account_url: str,
        credential: Union[str, Dict[str, str], AzureNamedKeyCredential, AzureSasCredential, TokenCredential, None] = None,
        **kwargs: Any
    ) -> None:
        """Initializes Azure Storage Account
        """
        super().__init__(*args, **kwargs)

        self.container_name = container_name
        self.blob = blob
        self.name_starts_with = name_starts_with
        self.include = include

        self.file_extractor = file_extractor

        self.account_url = account_url
        self.credential = credential

    def load_data(self) -> List[Document]:
        """Load file(s) from Azure Storage Blob"""

        container_client = ContainerClient(self.account_url, self.container_name, credential=self.credential)
        total_download_start_time = time.time()

        with tempfile.TemporaryDirectory() as temp_dir:
            if self.blob:
                extension = Path(self.blob).suffix
                download_file_path = f"{temp_dir}/{next(tempfile._get_candidate_names())}{extension}"
                logger.info(f"Start download of {self.blob}")
                start_time = time.time()
                stream = container_client.download_blob(self.blob)
                with open(file=download_file_path, mode="wb") as download_file:
                    stream.readinto(download_file)
                end_time = time.time()
                logger.info(
                    f"{self.blob} downloaded in {end_time - start_time} seconds."
                )
            else:
                logger.info(f"Listing blobs")
                blobs_list = container_client.list_blobs(self.name_starts_with, self.include)
                for obj in blobs_list:
                    extension = Path(obj.name).suffix
                    download_file_path = f"{temp_dir}/{next(tempfile._get_candidate_names())}{extension}"
                    logger.info(f"Start download of {obj.name}")
                    start_time = time.time()
                    stream = container_client.download_blob(obj)
                    with open(file=download_file_path, mode="wb") as download_file:
                        stream.readinto(download_file)
                    end_time = time.time()
                    logger.info(
                        f"{obj.name} downloaded in {end_time - start_time} seconds."
                    )
            
            total_download_end_time = time.time()
            total_elapsed_time = math.ceil(total_download_end_time - total_download_start_time)
            logger.info(f"Downloading completed in approximately {total_elapsed_time // 60}min {total_elapsed_time % 60}s.")
            logger.info(f"Document creation starting")
            SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
            loader = SimpleDirectoryReader(temp_dir, file_extractor=self.file_extractor)

            return loader.load_data()         


