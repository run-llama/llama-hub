"""(Unofficial) Google Keep reader using gkeepapi."""

import os
import gkeepapi
import json
from typing import Any, List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class GoogleKeepReader(BaseReader):
    """Google Keep reader.

    Reads notes from Google Keep

    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a GoogleKeepReader.

        Args:
            **kwargs: keyword arguments.
        """
        super().__init__(**kwargs)
        self._keep = self._get_keep()

    def _get_keep(self) -> gkeepapi.Keep:
        """Get a Google Keep object with login."""
        # Read username and password from keep_credentials.json
        if os.path.exists("keep_credentials.json"):
            with open("keep_credentials.json", "r") as f:
                credentials = json.load(f)
        else:
            raise RuntimeError('Failed to load keep_credentials.json.')

        keep = gkeepapi.Keep()

        success = keep.login(credentials["username"], credentials["password"])
        if not success:
            raise RuntimeError('Failed to login to Google Keep.')

        return keep

    def load_data(self, note_ids: List[str]) -> List[Document]:
        """Load data from the note_ids.

        Args:
            note_ids (List[str]): a list of note ids.
        """
        if note_ids is None:
            raise ValueError('Must specify a "note_ids" in `load_kwargs`.')

        results = []
        for note_id in note_ids:
            note = self._keep.get(note_id)
            if note is None:
                raise ValueError(f'Note with id {note_id} not found.')
            text = f"Title: {note.title}\nContent: {note.text}"
            results.append(Document(text=text, extra_info={"note_id":
                                                           note_id}))
        return results

    def load_all_notes(self) -> List[Document]:
        """Load all notes from Google Keep."""
        notes = self._keep.all()
        results = []
        for note in notes:
            text = f"Title: {note.title}\nContent: {note.text}"
            results.append(Document(text=text, extra_info={"note_id":
                                                           note.id}))


if __name__ == "__main__":
    reader = GoogleKeepReader()
    print(
        reader.load_data(note_ids=[
            "1eKU7kGn8eJCErZ52OC7vCzHDSQaspFYGHHCiTX_IvhFOc7ZQZVJhTIDFMdTJOPiejOk"
        ]))
