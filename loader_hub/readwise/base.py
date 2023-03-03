"""Simple Reader that loads text relevant to a certain search keyword from subreddits"""
from typing import List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

def _get_readwise_data(api_key, updated_after=None):
  """
  Uses Readwise's export API to export all highlights, optionally after a specified date.

  See https://readwise.io/api_deets for details.

  Args:
      updated_after (datetime.datetime): The datetime to load highlights after. Useful for updating indexes over time.
  """
  next_page = None
  while True:
    response = requests.get(
      url="https://readwise.io/api/v2/export/",
      params={"pageCursor": next_page, "updatedAfter": updated_after},
      headers={"Authorization": f"Token {api_key}"})
    yield from response.json()["results"]
    next_page = response.json().get("nextPageCursor")
    if not next_page: break

class ReadwiseReader(BaseReader):
    """
    Reader for Readwise highlights.
    """
    def __init__(self, api_key):
        self._api_key = api_key

    def load_data(
        self,
        updated_after = None,
    ) -> List[Document]:
        """
        Load your Readwise.io highlights.

        Args:
            updated_after (datetime.datetime): The datetime to load highlights after. Useful for updating indexes over time.
        """
        return [*_get_readwise_data(api_key=self._api_key, updated_after=updated_after)]
