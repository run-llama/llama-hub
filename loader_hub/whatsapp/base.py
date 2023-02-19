"""Whatsapp chat data loader"""

from pathlib import Path
from typing import List

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class WhatsappChatLoader(BaseReader):
    """
    Whatsapp chat data loader.

    Args:
        path (str): Path to Whatsapp chat file.
    """

    def __init__(self, path: str):
        """Initialize with path."""
        
        self.file_path = path

    def load_data(self, verbose=False) -> List[Document]:
        """
        Parse Whatsapp file into Documents

        Args:
            verbose (bool): Shows progress by printing "Added {count} of {total} messages".
        """

        import pandas as pd
        from chatminer.chatparsers import WhatsAppParser

        path = Path(self.file_path)

        parser = WhatsAppParser(path)
        parser.parse_file()
        df = parser.parsed_messages.get_df()

        print(f"Number of messages: {len(df)}.")

        docs = []
        n = 0
        for row in df.itertuples():
            extra_info = {
                "source": str(path).split("/")[-1].replace(".txt", ""), 
                "author": row.author, 
                "timestamp": str(row.timestamp)
            }
            
            docs.append(Document(str(row.timestamp) + " " + row.author + ":" + " " + row.message, extra_info=extra_info))

            if verbose:
                n += 1
                print(f"Added {n} of {len(df)} messages.")

        return docs