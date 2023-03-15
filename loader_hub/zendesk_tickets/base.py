"""Zendesk reader."""
import re
from zenpy import Zenpy
from bs4 import BeautifulSoup
import json
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class ZendeskTicketReader(BaseReader):
    """Zendesk reader. Reads data from a Zendesk Tickets.

    Args:
        zendesk_subdomain (str): Zendesk subdomain
    """

    def __init__(self, zendesk_subdomain: str, zendesk_oauth_token: str, zendesk_ticket_state: str) -> None:
        """Initialize Zendesk reader."""
        self.zendesk_subdomain = zendesk_subdomain
        self.zendesk_oauth_token = zendesk_oauth_token
        self.zendesk_ticket_state = zendesk_ticket_state
        
    def load_data(self) -> List[Document]:
        """Load data from the workspace.

        Args:
            workspace_id (str): Workspace ID.
        Returns:
            List[Document]: List of documents.
        """
        from bs4 import BeautifulSoup
        # Liste der bekannten Grußformeln
        greeting_regex = r"(Mit freundlichen Grüßen|Freundliche Grüße|Beste Grüße|Viele Grüße|Herzliche Grüße|Liebe Grüße|Alles Gute|Bis bald|Bis später|Bis zum nächsten Mal|Mit besten Grüßen|lg\n|Gruß|Grüße)"

        results = []
        creds = {
            "subdomain": self.zendesk_subdomain,
            "oauth_token": self.zendesk_oauth_token
        }
        zenpy_client = Zenpy(**creds)
        for ticket in zenpy_client.search_export(type='ticket', status=self.zendesk_ticket_state):
            description_text = BeautifulSoup(ticket.description, 'html.parser').get_text()
            m = re.search(greeting_regex, description_text, re.IGNORECASE)
            if m is not None:
                description_text = description_text[:m.start()].strip()
            body = description_text
            extra_info = {
                "id": ticket.id,
                "title": ticket.raw_subject,
                "created_at": ticket.created_at,
                "type": ticket.type,
                "priority": ticket.priority,
                "tags": ticket.tags,
                "satisfaction_rating": ticket.satisfaction_rating,
                "status": ticket.status
            }

            results.append(
                Document(
                    body,
                    extra_info=extra_info,
                )
            )

        return results

    def get_all_articles(self):
        articles = []
        next_page = None

        while True:
            response = self.get_articles_page(next_page)
            articles.extend(response["articles"])
            next_page = response["next_page"]

            if next_page is None:
                break

        return articles

    def get_articles_page(self, next_page: str = None):
        import requests

        if next_page is None:
            url = f"https://{self.zendesk_subdomain}.zendesk.com/api/v2/help_center/articles?per_page=100"
        else:
            url = next_page

        response = requests.get(url)

        response_json = json.loads(response.text)

        next_page = response_json.get("next_page", None)

        articles = response_json.get("articles", [])

        return {"articles": articles, "next_page": next_page}
