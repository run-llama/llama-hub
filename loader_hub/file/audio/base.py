"""Audio Transcriber.

A transcriber for the audio of mp3, mp4 files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class AudioTranscriber(BaseReader):
    """Audio parser.

    Extract text from transcript of video/audio files using OpenAI Whisper.

    """

    def __init__(self, *args: Any, model_version: str = "base", 
                model_type: str = "openai_whisper", diarization_max_speakers: str = None,
                language: str = "English", language_behaviour: str = "automatic multiple languages",
                target_translation_language: str = 'english', gladia_api_key: str = None, 
                transcription_hint: str = None, **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

        self.parser_config = {}
        self.model_type = model_type

        if self.model_type == "openai_gladia_whsiper":
            self.parser_config['gladia_api_key'] = gladia_api_key
            self.parser_config['diarization_max_speakers'] = diarization_max_speakers
            self.parser_config['language'] = language
            self.parser_config['language_behaviour'] = language_behaviour
            self.parser_config['target_translation_language'] = target_translation_language
            self.parser_config['transcription_hint'] = transcription_hint
        else:
            self._model_version = model_version

            import whisper

            model = whisper.load_model(self._model_version)

            self.parser_config = {"model": model}

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file."""
        import whisper

        if file.name.endswith("mp4"):
            from pydub import AudioSegment  # noqa: F401

            # open file
            video = AudioSegment.from_file(file, format="mp4")

            # Extract audio from video
            audio = video.split_to_mono()[0]

            file = str(file)[:-4] + ".mp3"
            # export file
            audio.export(file, format="mp3")

        transcript = ""

        if self.model_type == "openai_whisper":
            model = cast(whisper.Whisper, self.parser_config["model"])
            result = model.transcribe(str(file))

            transcript = result["text"]
        else:
            import requests

            headers = {
                'accept': 'application/json',
                'x-gladia-key': self.parser_config['gladia_api_key'],
            }

            files = {'audio': (str(file), open(str(file), 'rb'), 'audio/mpeg'),
                     'output_format': (None, 'txt')}

            if self.parser_config['diarization_max_speakers']:
                files['diarization_max_speakers'] = (None, self.parser_config['diarization_max_speakers'])
            if self.parser_config['language']:
                files['language'] = self.parser_config['language']
            if self.parser_config['language_behaviour']:
                files['language_behaviour'] = self.parser_config['language_behaviour']
            if self.parser_config['target_translation_language']:
                files['target_translation_language'] = self.parser_config['target_translation_language']
            if self.parser_config['transcription_hint']:
                files = self.parser_config['transcription_hint']

            response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
            response_dict = response.json()
            transcript = response_dict['prediction']

        return [Document(transcript, extra_info=extra_info)]