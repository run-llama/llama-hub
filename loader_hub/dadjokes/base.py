"""icanhazdadjoke based dad-joke generator."""

import requests
from typing import List

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document

class DadJokeReader(BaseReader):
    """Dad joke reader.

    Reads a random dad joke.

    """

    def _get_random_dad_joke(self):
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        if response.status_code == 200:
            json_data = response.json()
            return json_data["joke"]
        else:
            return "Sorry, I couldn't get a joke right now. Please try again later."


    def load_data(self) -> List[Document]:
        """Return a random dad joke.

        Args:
            None.

        """
        return [Document(self._get_random_dad_joke())]