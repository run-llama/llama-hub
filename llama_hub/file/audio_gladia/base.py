"""Audio Transcriber.

A transcriber for the audio of mp3, mp4 files using Gladia's OpenAI Whisper.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class GladiaAudioTranscriber(BaseReader):
    """Audio parser.

    Extract text from transcript of video/audio files using
    Gladia's OpenAI Whisper.

    """

    def __init__(
        self,
        *args: Any,
        diarization_max_speakers: Optional[str] = None,
        language: Optional[str] = None,
        language_behaviour: str = "automatic multiple languages",
        target_translation_language: str = "english",
        gladia_api_key: Optional[str] = None,
        transcription_hint: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

        self.parser_config = {}
        self.parser_config["gladia_api_key"] = gladia_api_key
        self.parser_config["diarization_max_speakers"] = diarization_max_speakers
        self.parser_config["language"] = language
        self.parser_config["language_behaviour"] = language_behaviour
        self.parser_config["target_translation_language"] = target_translation_language
        self.parser_config["transcription_hint"] = transcription_hint

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""

        if file.name.endswith("mp4"):
            from pydub import AudioSegment  # noqa: F401

            # open file
            video = AudioSegment.from_file(file, format="mp4")

            # Extract audio from video
            audio = video.split_to_mono()[0]

            file = str(file)[:-4] + ".mp3"
            # export file
            audio.export(file, format="mp3")

        import requests

        headers = {
            "accept": "application/json",
            "x-gladia-key": self.parser_config["gladia_api_key"],
        }

        files = {
            "audio": (str(file), open(str(file), "rb"), "audio/mpeg"),
            "output_format": (None, "txt"),
        }

        if self.parser_config["diarization_max_speakers"]:
            files["diarization_max_speakers"] = (
                None,
                self.parser_config["diarization_max_speakers"],
            )
        if self.parser_config["language"]:
            files["language"] = self.parser_config["language"]
        if self.parser_config["language_behaviour"]:
            files["language_behaviour"] = self.parser_config["language_behaviour"]
        if self.parser_config["target_translation_language"]:
            files["target_translation_language"] = self.parser_config[
                "target_translation_language"
            ]
        if self.parser_config["transcription_hint"]:
            files = self.parser_config["transcription_hint"]

        response = requests.post(
            "https://api.gladia.io/audio/text/audio-transcription/",
            headers=headers,
            files=files,
        )
        response_dict = response.json()
        transcript = response_dict["prediction"]

        return [Document(text=transcript, extra_info=extra_info or {})]
