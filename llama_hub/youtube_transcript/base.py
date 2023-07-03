"""Simple Reader that reads transcript of youtube video."""
import re
from typing import Any, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class YoutubeTranscriptReader(BaseReader):
    """Youtube Transcript reader."""

    @staticmethod
    def _extract_video_id(yt_link) -> Optional[str]:
        # regular expressions to match the different syntax of YouTube links
        patterns = [
            r"^https?://(?:www\.)?youtube\.com/watch\?v=([\w-]+)",
            r"^https?://(?:www\.)?youtube\.com/embed/([\w-]+)",
            r"^https?://youtu\.be/([\w-]+)",
        ]  # youtu.be does not use www

        for pattern in patterns:
            match = re.search(pattern, yt_link)
            if match:
                return match.group(1)

        # return None if no match is found
        return None

    def load_data(
        self,
        ytlinks: List[str],
        languages: Optional[List[str]] = ["en"],
        **load_kwargs: Any
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            pages (List[str]): List of youtube links \
                for which transcripts are to be read.

        """
        from youtube_transcript_api import YouTubeTranscriptApi

        results = []
        for link in ytlinks:
            video_id = self._extract_video_id(link)
            srt = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript = ""
            for chunk in srt:
                transcript = transcript + chunk["text"] + "\n"
            results.append(Document(text=transcript, extra_info={"video_id": video_id}))
        return results
