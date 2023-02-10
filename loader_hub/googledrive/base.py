"""Google Drive files reader."""

import os
from typing import Any, List, Optional
import logging

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class GoogleDriveReader(BaseReader):
    """Google drive reader."""

    def __init__(self,
                 credentials_path: str = "credentials.json",
                 token_path: str = "token.json",
                 folder_id: Optional[str] = None,
                 file_ids: Optional[List[str]] = None) -> None:
        """Initialize with parameters."""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.folder_id = folder_id
        self.file_ids = file_ids


def _get_credentials(self) -> Any:
    """
    Reference: https://developers.google.com/drive/api/v3/quickstart/python

    Returns:
        credentials
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

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

    return creds

def _load_from_file_id(self, id: str) -> Document:
    """Load from file id."""
    import io
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaIoBaseDownload

    creds = self._get_credentials()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        request = service.files().get_media(fileId=id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        text = file.getvalue().decode("utf-8")

        return Document(text)
    except HttpError as error:
        logger.error('An error occurred: {}'.format(error))

def _load_from_file_ids(self) -> List[Document]:
    '''Load from multiple file ids'''
    documents = []
    for id in self.file_ids:
        documents.append(self._load_from_file_id(id))
    return documents
    
def _load_files_from_folder(self) -> List[Document]:
    """Load files from a folder."""
    from googleapiclient.discovery import build

    creds = self._get_credentials()
    service = build("drive", "v3", credentials=creds)

    results = (
        service.files()
        .list(
            q=f"'{self.folder_id}' in parents",
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType)",
        )
        .execute()
    )
    items = results.get("files", [])

    documents = []
    for item in items:
        if item["mimeType"] == "text/plain":
            documents.append(self._load_from_file_id(item["id"]))
    return documents


def load_data(self) -> List[Document]:
    """Load files using file id or from folder."""
    if self.folder_id:
        return self._load_files_from_folder()
    else:
        return self._load_from_file_ids()