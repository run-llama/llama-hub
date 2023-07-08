"""Google Keep reader."""

import os
from typing import Any, List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

SCOPES = ["https://www.googleapis.com/auth/keep.readonly"]


# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class GoogleKeepReader(BaseReader):
    """Google Keep reader.

    Reads notes from Google Keep

    """

    def load_data(self, note_ids: List[str]) -> List[Document]:
        """Load data from the note_ids.

        Args:
            note_ids (List[str]): a list of note ids.
        """
        if note_ids is None:
            raise ValueError('Must specify a "note_ids" in `load_kwargs`.')

        results = []
        for note_id in note_ids:
            note = self._load_note(note_ids)
            results.append(Document(text=note, extra_info={"note_id": note_id}))
        return results

    def _load_note(self, note_id: str) -> str:
        """Load a note from Google Keep.

        Args:
            note_id: the note id.

        Returns:
            The note text.
        """
        import googleapiclient.discovery as discovery

        credentials = self._get_credentials()
        notes_service = discovery.build("note", "v1", credentials=credentials)
        note = notes_service.notes().get(name="note").execute()
        note_content = note.get("body").get("text")
        # TODO: support list content.
        return note_content

    def _get_credentials(self) -> Any:
        """Get valid user credentials from storage.

        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        Returns:
            Credentials, the obtained credential.
        """
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2 import service_account

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        elif os.path.exists("service_account.json"):
            creds = service_account.Credentials.from_service_account_file(
                "service_account.json", scopes=SCOPES
            )
            return creds
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds


if __name__ == "__main__":
    reader = GoogleKeepReader()
    print(
        reader.load_data(note_id=["1eKU7kGn8eJCErZ52OC7vCzHDSQaspFYGHHCiTX_IvhFOc7ZQZVJhTIDFMdTJOPiejOk"])
    )
