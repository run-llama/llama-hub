import os
from contextlib import contextmanager
from pathlib import Path
from urllib.request import Request, urlopen

import pytest

from importlib.util import find_spec

from llama_hub.file.audio.base import AudioTranscriber

REMOTE_AUDIO_SAMPLE_URL = (
    "https://audio-samples.github.io/samples/mp3/"
    "blizzard_tts_unbiased/sample-5/real.mp3"
)

LOCAL_TEST_FILE_PATH = "tests/tmp/llama-hub-audio-sample-test-temp.mp3"

whisper_available = find_spec("whisper") is not None


@pytest.mark.skipif(
    not whisper_available, reason="Skipping test because whisper is not available"
)
def test_transcribing_a_remote_mp3() -> None:
    if os.path.exists(LOCAL_TEST_FILE_PATH):
        documents = AudioTranscriber().load_data(file=Path(LOCAL_TEST_FILE_PATH))
    else:
        with load_remote_audio_sample() as filename:
            documents = AudioTranscriber().load_data(file=Path(filename))

    # It technically gets the transcription incorrect, at least with
    # the base model. The final word is 'moor', not 'more'. (This
    # sample is from 'The Secret Garden'.) So skipping that word
    # in the assertion and matching on an easier fragment.
    assert "they are exactly the color of the sky" in documents[0].text


@contextmanager
def load_remote_audio_sample():
    req = Request(REMOTE_AUDIO_SAMPLE_URL, headers={"User-Agent": "Magic Browser"})
    remote_audio_sample = urlopen(req)
    filepath = "tests/tmp/llama-hub-audio-sample-test-temp.mp3"
    with open(filepath, "wb") as output:
        output.write(remote_audio_sample.read())
        yield filepath
