"""Google Mail reader."""
import email
from typing import Any, List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from pydantic import BaseModel
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailReader(BaseReader, BaseModel):
    """Gmail reader.

    Reads emails

    Args:
        query (str): Gmail query. Defaults to None.
        max_results (int): Max number of results. Defaults to 10.
    """
    query: str = None
    use_iterative_parser: bool = False
    max_results: int = 10
    service: Any

    def load_data(
        self
    ) -> List[Document]:
        """Load emails from the user's account
        """
        from googleapiclient.discovery import build

        credentials = self._get_credentials()
        if not self.service:
            self.service = build('gmail', 'v1', credentials=credentials)

        messsages = self.search_messages()

        results = []
        for message in messsages:
            text = message.pop('body')
            extra_info = message
            results.append(Document(text, extra_info=extra_info))

        return results

    def _get_credentials(self) -> Any:
        """Get valid user credentials from storage.

        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        Returns:
            Credentials, the obtained credential.
        """
        import os
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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

    def search_messages(self):
        query = self.query

        max_results = self.max_results

        messages = self.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=int(max_results)
        ).execute().get('messages', [])

        result = []
        try:
            for message in messages:
                message_data = self.get_message_data(message)
                if not message_data:
                    continue
                result.append(message_data)
        except Exception as e:
            raise Exception("Can't get message data" + str(e))

        return result

    def get_message_data(self, message):
        message_id = message['id']
        message_data = self.service.users().messages().get(
            format="raw",
            userId='me',
            id=message_id).execute()
        if self.use_iterative_parser:
            body = self.extract_message_body_iterative(message_data)
        else:
            body = self.extract_message_body(message_data)

        if not body:
            return None

        return {
            "id": message_data['id'],
            "threadId": message_data['threadId'],
            "snippet": message_data['snippet'],
            "body": body,
        }
    
    def extract_message_body_iterative(self, message:dict):
        if message['raw']:
            body = base64.urlsafe_b64decode(message['raw'].encode('utf8'))
            mime_msg = email.message_from_bytes(body)
        else:
            mime_msg = message
        
        body_text = ''
        if mime_msg.get_content_type() == 'text/plain':
            plain_text = mime_msg.get_payload(decode=True)
            charset = mime_msg.get_content_charset('utf-8')
            body_text = plain_text.decode(charset).encode('utf-8').decode('utf-8')
            
        elif mime_msg.get_content_maintype() == 'multipart':
            msg_parts = mime_msg.get_payload()
            for msg_part in msg_parts:
                body_text += self.extract_message_body_iterative(msg_part)
                
        return body_text

    def extract_message_body(self, message: dict):
        from bs4 import BeautifulSoup
        try:
            body = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(body)

            # If the message body contains HTML, parse it with BeautifulSoup
            if 'text/html' in mime_msg:
                soup = BeautifulSoup(body, 'html.parser')
                body = soup.get_text()
            return body.decode("ascii")
        except Exception as e:
            raise Exception("Can't parse message body" + str(e))


if __name__ == "__main__":
    reader = GmailReader(query="from:me after:2023-01-01")
    print(
        reader.load_data()
    )
