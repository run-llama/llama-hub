import unittest
from importlib.util import find_spec
from unittest.mock import patch, call

import pytest
from llama_index.readers.schema.base import Document

from llama_hub.youtube_channel_transcript import YoutubeChannelTranscriptReader

dependencies_available = ((find_spec("googleapiclient") is not None) and
                          (find_spec("youtube_transcript_api") is not None))

CHANNELS_RESPONSE = {
    "items": [
        {
            "contentDetails": {
                "relatedPlaylists": {
                    "uploads": "test_playlist_id"
                }
            }
        }
    ]
}

PLAYLISTS_RESPONSE = {
    "items": [
        {
            "contentDetails": {
                "videoId": "test_video_id_1"
            }
        },
        {
            "contentDetails": {
                "videoId": "test_video_id_2"
            }
        }
    ]
}


def dummy_load_pages(ytlinks: list[str]):
    documents = []
    for ytlink in ytlinks:
        documents.append(Document(text=f"Transcript for {ytlink}"))
    return documents


def dummy_load_pages_with_exception(ytlinks: list[str]):
    documents = []
    for ytlink in ytlinks:
        if ytlink == "https://www.youtube.com/watch?v=test_video_id_2":
            documents.append(Document(text=f"Transcript for {ytlink}"))
        else:
            raise Exception("Failed to load transcript")
    return documents


class TestYoutubeChannelTranscriptReader(unittest.TestCase):

    @pytest.mark.skipif(
        not dependencies_available,
        reason="Skipping since google-api-python-client or youtube_transcript_api is not installed",
    )
    def test_yt_channel_transcript_reader_init(self):
        # test w/o args
        YoutubeChannelTranscriptReader()

    @pytest.mark.skipif(
        not dependencies_available,
        reason="Skipping since google-api-python-client or youtube_transcript_api is not installed",
    )
    def test_yt_channel_transcript_reader_load_data_invalid_args(self):
        youtube_channel_transcript_reader = YoutubeChannelTranscriptReader()

        with pytest.raises(
                TypeError,
                match="missing 2 required positional arguments: 'google_api_key' and 'yt_channel_id'",
        ):
            youtube_channel_transcript_reader.load_data()

    @pytest.mark.skipif(
        not dependencies_available,
        reason="Skipping since google-api-python-client or youtube_transcript_api is not installed",
    )
    @patch("llama_hub.youtube_transcript.base.YoutubeTranscriptReader.load_data")
    def test_yt_channel_transcript_reader_load_data(self, mock_load_data):
        with patch("googleapiclient.discovery") as mock_discovery:
            youtube_channel_transcript_reader = YoutubeChannelTranscriptReader()

            mock_build = mock_discovery.build.return_value
            mock_build.channels.return_value.list.return_value.execute.return_value = CHANNELS_RESPONSE
            mock_build.playlistItems.return_value.list.return_value.execute.return_value = PLAYLISTS_RESPONSE

            mock_load_data.side_effect = dummy_load_pages

            documents = youtube_channel_transcript_reader.load_data(google_api_key="test_key",
                                                                    yt_channel_id="test_channel_id")

            mock_discovery.build.assert_called_once_with('youtube', 'v3', developerKey='test_key')
            mock_discovery.build.return_value.channels.assert_called_once()
            mock_discovery.build.return_value.channels.return_value.list.assert_called_once_with(
                part='contentDetails', id='test_channel_id')
            mock_discovery.build.return_value.channels.return_value.list.return_value.execute.assert_called_once()
            mock_discovery.build.return_value.playlistItems.assert_called_once()
            mock_discovery.build.return_value.playlistItems.return_value.list.assert_called_once_with(
                part='contentDetails', playlistId='test_playlist_id', maxResults=50, pageToken=None)
            mock_discovery.build.return_value.playlistItems.return_value.list.return_value.execute.assert_called_once()

            assert mock_load_data.call_count == 2
            mock_load_data.assert_has_calls([
                call(ytlinks=['https://www.youtube.com/watch?v=test_video_id_1']),
                call(ytlinks=['https://www.youtube.com/watch?v=test_video_id_2'])])

            assert len(documents) == 2
            assert documents[0].text == "Transcript for https://www.youtube.com/watch?v=test_video_id_1"
            assert documents[1].text == "Transcript for https://www.youtube.com/watch?v=test_video_id_2"

    @pytest.mark.skipif(
        not dependencies_available,
        reason="Skipping since google-api-python-client or youtube_transcript_api is not installed",
    )
    @patch("llama_hub.youtube_transcript.base.YoutubeTranscriptReader.load_data")
    def test_yt_channel_transcript_reader_load_data_with_exceptions(self, mock_load_data):
        with patch("googleapiclient.discovery") as mock_discovery:
            youtube_channel_transcript_reader = YoutubeChannelTranscriptReader()

            mock_build = mock_discovery.build.return_value
            mock_build.channels.return_value.list.return_value.execute.return_value = CHANNELS_RESPONSE
            mock_build.playlistItems.return_value.list.return_value.execute.return_value = PLAYLISTS_RESPONSE

            mock_load_data.side_effect = dummy_load_pages_with_exception

            documents = youtube_channel_transcript_reader.load_data(google_api_key="test_key",
                                                                    yt_channel_id="test_channel_id")

            assert mock_load_data.call_count == 2
            mock_load_data.assert_has_calls([
                call(ytlinks=['https://www.youtube.com/watch?v=test_video_id_1']),
                call(ytlinks=['https://www.youtube.com/watch?v=test_video_id_2'])])

            assert len(documents) == 1
            assert documents[0].text == "Transcript for https://www.youtube.com/watch?v=test_video_id_2"
