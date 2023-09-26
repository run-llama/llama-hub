from unittest.mock import patch

import pytest

from llama_hub.youtube_transcript import YoutubeTranscriptReader, is_youtube_video

from importlib.util import find_spec


def test_is_youtube_video_helper() -> None:
    # youtube.com watch URLs
    assert is_youtube_video(
        "https://youtube.com/watch?v=Fy1xQSiLx8U/"
    ), "Expected youtube.com, no subdomain, with v query param to be valid"
    assert is_youtube_video(
        "https://www.youtube.com/watch?v=Fy1xQSiLx8U"
    ), "Expected youtube.com with subdomain and v query param to be valid"
    # youtube.com embed URLs
    assert is_youtube_video(
        "https://youtube.com/embed/Fy1xQSiLx8U"
    ), "Expected youtube.com /embed without subdomain to be valid"
    assert is_youtube_video(
        "https://www.youtube.com/embed/Fy1xQSiLx8U"
    ), "Expected youtube.com /embed with subdomain to be valid"

    # youtu.be URLs
    assert is_youtube_video(
        "https://youtu.be/Fy1xQSiLx8U"
    ), "Expected youtu.be without subdomain to be valid"
    assert not is_youtube_video(
        "https://www.youtu.be/Fy1xQSiLx8U"
    ), "Expected youtu.be with subdomain to be invalid"


transcription_api_available = find_spec("youtube_transcript_api") is not None


@pytest.mark.skipif(
    not transcription_api_available,
    reason="Skipping since youtube_transcript_api is not installed",
)
def test_loading_a_url_into_documents(monkeypatch) -> None:
    video_url = "https://www.youtube.com/watch?v=Fy1xQSiLx8U"
    fake_transcript = [
        {"text": "N'existe pas sans son contraire"},
        {"text": "qui lui semble facile à trouver"},
        {"text": "Le bonheur n'existe que pour plaire,"},
        {"text": "je le veux"},
    ]
    with patch(
        "youtube_transcript_api.YouTubeTranscriptApi.get_transcript",
        return_value=fake_transcript,
    ):
        documents = YoutubeTranscriptReader().load_data([video_url])
        assert (
            documents[0].text == "N'existe pas sans son contraire\n"
            "qui lui semble facile à trouver\n"
            "Le bonheur n'existe que pour plaire,\n"
            "je le veux"
        )
