
import pytest
from unittest.mock import patch, MagicMock
from llama_hub.youtube_transcript import YoutubeTranscriptReader, is_youtube_video

def test_is_youtube_video_helper() -> None:
    assert(
        is_youtube_video("https://youtube.com/watch?v=j83jrh2"),
        "Expected youtube.com, no subdomain, with v query param to be valid"
    )

    assert(
        is_youtube_video("https://www.youtube.com/watch?v=j83jrh2"),
        "Expected youtube.com with subdomain and v query param to be valid"
    )

    assert(
        is_youtube_video("https://youtube.com/embed?v=j83jrh2"),
        "Expected youtube.com without subdomain and with v query param to be valid"
    )

    assert(
        is_youtube_video("https://www.youtube.com/embed?v=j83jrh2"),
        "Expected youtube.com with subdomain and v query param to be valid"
    )
            
    assert(
        is_youtube_video("https://youtu.be/j83jrh2"),
        "Expected youtu.be without subdomain to be valid"
    )
   
    assert(
        is_youtube_video("https://www.youtu.be/j83jrh2"),
        "Expected youtu.be with subdomain to be invalid"
    )
try:
    import youtube_transcript_api
    transcription_api_available = True
except ImportError:
    transcription_api_available = False
@pytest.mark.skipif(not transcription_api_available,
               reason="Skipping since youtube_transcript_api is not installed")
def test_loading_a_url_into_documents(monkeypatch) -> None:
    video_url = "https://www.youtube.com/watch?v=Fy1xQSiLx8U"
    fake_transcript = [
        {"text": "N'existe pas sans son contraire"},
        {"text": "qui lui semble facile à trouver"},
        {"text": "Le bonheur n'existe que pour plaire,"},
        {"text": "je le veux"}
    ]
    with patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript", return_value=fake_transcript):
        documents = YoutubeTranscriptReader().load_data([video_url])
        assert documents[0].text == (
            "N'existe pas sans son contraire\n"
            "qui lui semble facile à trouver\n"
            "Le bonheur n'existe que pour plaire,\n"
            "je le veux"
        )