"""Hubspot reader."""
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class HubspotReader(BaseReader):
    """Hubspot reader. Reads data from a Hubspot account.

    Args:
        access_token(str): Hubspot API key.
    """

    def __init__(self, access_token: str) -> None:
        """Initialize Hubspot reader."""

        self.access_token = access_token

    def load_data(self) -> List[Document]:
        """Load deals, contacts and companies data from Hubspot

        Returns:
            List[Document]: List of documents, where each document represensts a list of Hubspot objects
        """
        from hubspot import HubSpot

        api_client = HubSpot(access_token=self.access_token)
        all_deals = api_client.crm.deals.get_all()
        all_contacts = api_client.crm.contacts.get_all()
        all_companies = api_client.crm.companies.get_all()
        results = [
            Document(text=f"{all_deals}".replace("\n", ""), metadata={"type": "deals"}), 
            Document(text=f"{all_contacts}".replace("\n", ""), metadata={"type": "contacts"}),
            Document(text=f"{all_companies}".replace("\n", ""), metadata={"type": "companies"})
        ]
        return results
