import pytest
from pytest_mock import MockerFixture

from importlib.util import find_spec

from llama_hub.assemblyai.base import AssemblyAIAudioTranscriptReader
from llama_hub.assemblyai.base import TranscriptFormat


assemblyai_available = find_spec("assemblyai") is not None


@pytest.mark.skipif(
    not assemblyai_available,
    reason="Skipping test because assemblyai package is not available",
)
def test_initialization() -> None:
    reader = AssemblyAIAudioTranscriptReader(
        file_path="./testfile.mp3", api_key="api_key"
    )
    assert reader.file_path == "./testfile.mp3"
    assert reader.transcript_format == TranscriptFormat.TEXT


@pytest.mark.skipif(
    not assemblyai_available,
    reason="Skipping test because assemblyai package is not available",
)
def test_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "assemblyai.Transcriber.transcribe",
        return_value=mocker.MagicMock(
            text="Test transcription text", json_response={"id": "1"}, error=None
        ),
    )

    reader = AssemblyAIAudioTranscriptReader(
        file_path="./testfile.mp3", api_key="api_key"
    )
    docs = reader.load_data()
    assert len(docs) == 1
    assert docs[0].text == "Test transcription text"
    assert docs[0].metadata == {"id": "1"}


@pytest.mark.skipif(
    not assemblyai_available,
    reason="Skipping test because assemblyai package is not available",
)
def test_transcription_error(mocker: MockerFixture) -> None:
    mocker.patch(
        "assemblyai.Transcriber.transcribe",
        return_value=mocker.MagicMock(error="Test error"),
    )

    reader = AssemblyAIAudioTranscriptReader(
        file_path="./testfile.mp3", api_key="api_key"
    )

    expected_error = "Could not transcribe file: Test error"
    with pytest.raises(ValueError, match=expected_error):
        reader.load_data()
