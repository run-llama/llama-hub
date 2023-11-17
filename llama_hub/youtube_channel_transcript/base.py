"""Simple Reader that reads transcripts of all YouTube videos for a YouTube channel."""
import logging
from importlib.util import find_spec
from typing import List

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class YoutubeChannelTranscriptReader(BaseReader):
    """YouTube channel reader. Reads transcripts for all videos from a YouTube channel.
    """
    def __init__(self) -> None:
        if find_spec("googleapiclient") is None:
            raise ImportError(
                "Missing package: googleapiclient.\n"
                "Please `pip install google-api-python-client` to use this Reader"
            )

        try:
            from llama_hub.utils import import_loader

            YoutubeTranscriptReader = import_loader("YoutubeTranscriptReader")
        except ImportError:
            YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")

        self._youtube_transcript_loader = YoutubeTranscriptReader()

    def load_data(self, google_api_key: str, yt_channel_id: str) -> List[Document]:
        """Load data for all videos in the YouTube channel.

        Args:
            google_api_key (str): Google API key.
            yt_channel_id (str): YouTube channel ID.

        """
        documents = []
        yt_links = self.get_channel_video_links(google_api_key=google_api_key, yt_channel_id=yt_channel_id)
        logging.info("Found %s YouTube videos from the channel", len(yt_links))

        # loading documents for one video at a time because it might fail for videos without transcripts
        for yt_link in yt_links:
            try:
                link_documents = self._youtube_transcript_loader.load_data(ytlinks=[yt_link])
                documents.extend(link_documents)
            except Exception:
                logging.warning("Failed to load data for video: %s", yt_link, exc_info=True)

        logging.info("Loaded %s documents from the channel", len(documents))
        return documents

    @staticmethod
    def get_channel_video_links(google_api_key: str, yt_channel_id: str) -> List[str]:
        import googleapiclient.discovery

        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=google_api_key)
        playlists_response = youtube.channels().list(part='contentDetails', id=yt_channel_id).execute()
        playlist_id = playlists_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        logging.info("Found playlist id: %s", playlist_id)

        next_page_token = None
        item_ids = []

        while True:
            items_response = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50,
                                                          pageToken=next_page_token).execute()
            items = items_response['items']
            video_ids = [item['contentDetails']['videoId'] for item in items]
            item_ids.extend(video_ids)
            next_page_token = items_response.get('nextPageToken')
            if not next_page_token:
                break

        return ['https://www.youtube.com/watch?v=' + item_id for item_id in item_ids]
