"""Google Drive files reader."""

import logging
import os
import tempfile
from pathlib import Path
from typing import Any, List

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

# Scope for reading and downloading google drive files
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class GoogleDriveReader(BaseReader):
    """Google drive reader."""

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        pydrive_creds_path: str = "creds.txt",
    ) -> None:
        """Initialize with parameters."""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.pydrive_creds_path = pydrive_creds_path

        self._creds = None
        self._drive = None

        # Download Google Docs/Slides/Sheets as actual files
        # See https://developers.google.com/drive/v3/web/mime-types
        self._mimetypes = {
            "application/vnd.google-apps.document": {
                "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "extension": ".docx",
            },
            "application/vnd.google-apps.spreadsheet": {
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "extension": ".xlsx",
            },
            "application/vnd.google-apps.presentation": {
                "mimetype": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "extension": ".pptx",
            },
        }

    def _get_credentials(self) -> Any:
        """Authenticate with Google and save credentials.
        Download the credentials.json file with these instructions: https://developers.google.com/drive/api/v3/quickstart/python.
            Copy credentials.json file and rename it to client_secrets.json file which will be used by pydrive for downloading files.
            So, we need two files:
                1. credentials.json
                2. client_secrets.json
            Both 1, 2 are esentially same but needed with two different names according to google-api-python-client, google-auth-httplib2, google-auth-oauthlib and pydrive libraries.
        Returns:
            credentials, pydrive object
        """
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        # First, we need the Google API credentials for the app
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
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

        # Next, we need user authentication to download files (via pydrive)
        # Uses client_secrets.json file for authorization.
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(self.pydrive_creds_path)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file so user doesn't have to auth every time
        gauth.SaveCredentialsFile(self.pydrive_creds_path)

        drive = GoogleDrive(gauth)

        return creds, drive

    def _get_fileids_meta(
        self, folder_id: str = None, file_id: str = None
    ) -> List[str]:
        """Get file ids present in folder/ file id
        Args:
            folder_id: folder id of the folder in google drive.
            file_id: file id of the file in google drive
        Returns:
            metadata: List of metadata of filde ids.
        """
        from googleapiclient.discovery import build

        try:
            service = build("drive", "v3", credentials=self._creds)
            if folder_id:
                fileids_meta = []
                query = "'" + folder_id + "' in parents"
                results = service.files().list(q=query, fields="*").execute()
                items = results.get("files", [])
                for item in items:
                    if item["mimeType"] == "application/vnd.google-apps.folder":
                        fileids_meta.extend(
                            self._get_fileids_meta(folder_id=item["id"])
                        )
                    else:
                        fileids_meta.append(
                            (
                                item["id"],
                                item["owners"][0]["displayName"],
                                item["name"],
                                item["createdTime"],
                                item["modifiedTime"],
                            )
                        )
            else:
                # Get the file details
                file = service.files().get(fileId=file_id, fields="*").execute()

                # Get metadata of the file
                fileids_meta = (
                    file["id"],
                    file["owners"][0]["displayName"],
                    file["name"],
                    file["createdTime"],
                    file["modifiedTime"],
                )

            return fileids_meta

        except Exception as e:
            logger.error(
                "An error occurred while getting fileids metadata: {}".format(e)
            )

    def _download_file(self, fileid: str, filename: str) -> str:
        """Download the file with fileid and filename
        Args:
            fileid: file id of the file in google drive
            filename: filename with which it will be downloaded
        Returns:
            The downloaded filename, which which may have a new extension
        """
        try:
            file = self._drive.CreateFile({"id": fileid})
            if file["mimeType"] in self._mimetypes:
                download_mimetype = self._mimetypes[file["mimeType"]]["mimetype"]
                download_extension = self._mimetypes[file["mimeType"]]["extension"]
                new_filename = filename + download_extension
                # download file with filename and mimetype
                file.GetContentFile(new_filename, mimetype=download_mimetype)
                return new_filename
            else:
                # download file with filename
                file.GetContentFile(filename)
                return filename
        except Exception as e:
            logger.error("An error occurred while downloading file: {}".format(e))

    def _load_data_fileids_meta(self, fileids_meta: List[List[str]]) -> List[Document]:
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
                    filename = next(tempfile._get_candidate_names())
                    filepath = os.path.join(temp_dir, filename)
                    fileid = fileid_meta[0]
                    final_filepath = self._download_file(fileid, filepath)
                    metadata[final_filepath] = {
                        "file id": fileid_meta[0],
                        "author": fileid_meta[1],
                        "file name": fileid_meta[2],
                        "created at": fileid_meta[3],
                        "modified at": fileid_meta[4],
                    }
                SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
                loader = SimpleDirectoryReader(temp_dir, file_metadata=get_metadata)
                documents = loader.load_data()

            return documents
        except Exception as e:
            logger.error(
                "An error occurred while loading data from fileids meta: {}".format(e)
            )

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
            logger.error("An error occurred while loading with fileid: {}".format(e))

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
            logger.error("An error occurred while loading from folder: {}".format(e))

    def load_data(
        self, folder_id: str = None, file_ids: List[str] = None
    ) -> List[Document]:
        """Load data from the folder id and file ids.
        Args:
            folder_id: folder id of the folder in google drive.
            file_ids: file ids of the files in google drive.
        Returns:
            List[Document]: A list of documents.
        """
        self._creds, self._drive = self._get_credentials()

        if folder_id:
            return self._load_from_folder(folder_id)
        else:
            return self._load_from_file_ids(file_ids)
