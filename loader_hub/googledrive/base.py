"""Google Drive files reader."""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
import os
import logging
import tempfile

from gpt_index import download_loader
from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# Scope for reading and downloading google drive files
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class GoogleDriveReader(BaseReader):
    """Google drive reader."""

    def __init__(self,
                 credentials_path: str = "credentials.json",
                 client_secrets_path: str = "client_secrets.json",
                 token_path: str = "token.json") -> None:
        """Initialize with parameters."""
        self.credentials_path = credentials_path
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path

    def _get_credentials(self) -> Any:
        """
        Reference: https://developers.google.com/drive/api/v3/quickstart/python

        Download the credentials.json file with above reference.
        Copy credentials.json file and rename it to client_secrets.json file which will be used by pydrive for downloading files.

        So, we need two files:
        1. credentials.json
        2. client_secrets.json

        Both 1, 2 are esentially same but needed with two different names according to google-api-python-client, google-auth-httplib2, google-auth-oauthlib and pydrive libraries.

        Returns:
            credentials, pydrive object
        """
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(
                self.token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        # Authorization for downloading files.
        # Uses client_secrets.json file for authorization.
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        return creds, drive

    def _get_fileids_meta(self, folder_id: str = None, file_id: str = None) -> List[str]:
        """Get file ids present in folder/ file id
        Args:
            folder_id: folder id of the folder in google drive.
            file_id: file id of the file in google drive
        Returns:
            metadata: List of metadata of filde ids.
        """
        try:

            service = build("drive", "v3", credentials=creds)
            if folder_id:
                fileids_meta = []
                query = "'" + folder_id + "' in parents"
                results = service.files().list(
                    q=query, fields="*").execute()
                items = results.get("files", [])
                for item in items:
                    if item["mimeType"] == 'application/vnd.google-apps.folder':
                        fileids_meta.extend(
                            self._get_fileids_meta(folder_id=item["id"]))
                    else:
                        fileids_meta.append(
                            (item["id"], item["owners"][0]['displayName'], item["name"], item["createdTime"], item["modifiedTime"]))
            else:
                # Get the file details
                file = service.files().get(fileId=file_id, fields="*").execute()

                # Get metadata of the file
                fileids_meta = (file["id"], file["owners"][0]['displayName'],
                                file["name"], file["createdTime"], file["modifiedTime"])

            return fileids_meta

        except Exception as e:
            logger.error(
                'An error occurred while getting fileids metadata: {}'.format(e))

    def _download_file(self, fileid: str, filename: str) -> None:
        """Download the file with fileid and filename
        Args:
            fileid: file id of the file in google drive
            filename: filename with which it will be downloaded
        Returns:
            None
        """
        try:
            file = drive.CreateFile({'id': fileid})
            # download file with filename
            file.GetContentFile(filename)
        except Exception as e:
            logger.error(
                'An error occurred while downloading file: {}'.format(e))

    def _load_data_fileids_meta(self, fileids_meta: str) -> List[Document]:
        """Load data from fileids metadata
        Args:
            fileids_meta: metadata of fileids in google drive.
        Returns:
            Lis[Document]: List of Document of data present in fileids
        """

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                def get_metadata(filename):
                    return metadata[filename]

                temp_dir = Path(temp_dir)
                metadata = {}

                for fileid_meta in fileids_meta:
                    filename = fileid_meta[2]
                    filepath = os.path.join(temp_dir, filename)
                    fileid = fileid_meta[0]
                    self._download_file(fileid, filepath)
                    metadata[filepath] = {
                        "author": fileid_meta[1],
                        "filename": filename,
                        "createdTime": fileid_meta[3],
                        "modifiedTime": fileid_meta[4]
                    }
                SimpleDirectoryReader = download_loader(
                    "SimpleDirectoryReader")
                loader = SimpleDirectoryReader(
                    temp_dir, file_metadata=get_metadata)
                documents = loader.load_data()

            return documents
        except Exception as e:
            logger.error(
                'An error occurred while loading data from fileids meta: {}'.format(e))

    def _load_from_file_ids(self, file_ids: List[str]) -> List[Document]:
        """Load data from file ids
        Args:
            file_ids: file ids of the files in google drive.
        Returns:
            Document: List of Documents of text.
        """

        try:
            fileids_meta = []
            for file_id in file_ids:
                fileids_meta.append(self._get_fileids_meta(file_id=file_id))
            documents = self._load_data_fileids_meta(fileids_meta)

            return documents
        except Exception as e:
            logger.error(
                'An error occurred while loading with fileid: {}'.format(e))

    def _load_from_folder(self, folder_id: str) -> List[Document]:
        """Load data from folder_id
        Args:
            folder_id: folder id of the folder in google drive.
        Returns:
            Document: List of Documents of text.
        """
        try:
            fileids_meta = self._get_fileids_meta(folder_id=folder_id)
            documents = self._load_data_fileids_meta(fileids_meta)
            return documents
        except Exception as e:
            logger.error(
                'An error occurred while loading from folder: {}'.format(e))

    def load_data(self, folder_id: str = None, file_ids: List[str] = None) -> List[Document]:
        """Load data from the folder id and file ids.
        Args:
            folder_id: folder id of the folder in google drive.
            file_ids: file ids of the files in google drive.
        Returns:
            List[Document]: A list of documents.
        """
        global creds, drive
        creds, drive = self._get_credentials()

        if folder_id:
            return self._load_from_folder(folder_id)
        else:
            return self._load_from_file_ids(file_ids)
