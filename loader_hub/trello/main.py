"""Trello reader."""
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from trello import TrelloClient


class TrelloReader(BaseReader):
    """Trello reader. Reads data from Trello boards and cards.

    Args:
        api_key (str): Trello API key.
        api_token (str): Trello API token.
    """

    def __init__(self, api_key: str, api_token: str) -> None:
        """Initialize Trello reader."""
        self.api_key = api_key
        self.api_token = api_token
        self.client = TrelloClient(api_key=api_key, token=api_token)

    def load_data(self, board_id: str) -> List[Document]:
        """Load data from a Trello board.

        Args:
            board_id (str): Trello board ID.
        Returns:
            List[Document]: List of documents representing Trello cards.
        """
        board = self.client.get_board(board_id)
        cards = board.get_cards()

        documents = []
        for card in cards:
            document = Document(
                card.name,
                card.description,
                extra_info={
                    "id": card.id,
                    "url": card.url,
                    "due_date": card.due_date,
                    "labels": [label.name for label in card.labels],
                }
            )
            documents.append(document)

        return documents

