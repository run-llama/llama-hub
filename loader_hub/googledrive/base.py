"""Google Drive files reader."""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
import os
import logging

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

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

DEFAULT_FILE_EXTRACTOR: Dict[str, str] = {
    ".pdf": "PDFReader",
    ".docx": "DocxReader",
    ".pptx": "PptxReader",
    ".jpg": "ImageReader",
    ".png": "ImageReader",
    ".jpeg": "ImageReader",
    ".mp3": "AudioTranscriber",
    ".mp4": "AudioTranscriber",
    ".csv": "PandasCSVReader",
    ".txt": "UnstructuredReader",
    ".html": "UnstructuredReader"
}


class GoogleDriveReader(BaseReader):
    """Google drive reader."""

    def __init__(self,
                 credentials_path: str = "credentials.json",
                 client_secrets_path: str = "client_secrets.json",
                 token_path: str = "token.json",
                 folder_id: Optional[str] = None,
                 file_ids: Optional[List[str]] = None,
                 file_extractor: Optional[Dict[str,
                                               Union[str, BaseReader]]] = None,
                 file_metadata: Optional[Callable[[str], Dict]] = None,) -> None:
        """Initialize with parameters."""
        self.credentials_path = credentials_path
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.folder_id = folder_id
        self.file_ids = file_ids
        self.file_extractor = file_extractor or DEFAULT_FILE_EXTRACTOR
        self.file_metadata = file_metadata

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

    def _load_from_file_id(self, file_id: str) -> Document:

        try:

            # Authenticate and build the Drive API client
            service = build('drive', 'v3', credentials=creds)

            # Get the file details
            file = service.files().get(fileId=file_id).execute()

            # Get file name that will be downloaded
            input_file = file['name']

            # Download the file locally
            file_obj = drive.CreateFile({'id': file_id})
            file_obj.GetContentFile(input_file)

            # Get suffix to read the content
            suffix = Path(input_file).suffix

            # Get metadata of the file
            metadata = None
            if self.file_metadata is not None:
                metadata = self.file_metadata(str(input_file))

            document = ""

            # If suffix in fileextractor, user reader
            if suffix in self.file_extractor:
                reader = self.file_extractor[suffix]
                reader = download_loader(reader)()
                document = reader.load_data(
                    file=input_file, extra_info=metadata)

            return document
        except Exception as e:
            logger.error('Failed with error: {}'.format(e))

    def _load_from_file_ids(self, file_ids: List[str]) -> List[Document]:

        try:
            documents = []
            for file_id in file_ids:
                documents.append(self._load_from_file_id(file_id))
            return documents
        except Exception as e:
            logger.error('Failed with error: {}'.format(e))

    def _load_from_folder(self, folder_id: str) -> List[Document]:

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)
            # Make a GET request to the files endpoint and filter results to only include files in the specified folder
            query = f"'{folder_id}' in parents"
            results = service.files().list(
                q=query, fields="nextPageToken, files(id)").execute()

            # Return the list of files
            files = results.get("files", [])

            fileids = [file['id'] for file in files]
            documents = self._load_from_file_ids(fileids)

            return documents
        except Exception as e:
            logger.error('An error occurred: {}'.format(e))

    def load_data(self) -> List[Document]:
        global creds, drive
        creds, drive = self._get_credentials()

        if self.folder_id:
            return self._load_from_folder(self.folder_id)
        else:
            return self._load_from_file_ids(self.file_ids)
