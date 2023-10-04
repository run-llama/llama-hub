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

    def __init__(self, *args: Any, model_version: str = "base", **kwargs: Any) -> None:
        """Init params."""
        try:
            import whisper
        except ImportError:
            raise ImportError(
                "Missing required package: whisper\n"
                "Please `pip install whisper` to use AudioTranscriber"
            )

        super().__init__(*args, **kwargs)
        self._model_version = model_version

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

            file_str = str(file)[:-4] + ".mp3"
            # export file
            audio.export(file_str, format="mp3")

        model = cast(whisper.Whisper, self.parser_config["model"])
        result = model.transcribe(str(file))

        transcript = result["text"]

        return [Document(text=transcript, extra_info=extra_info or {})]
