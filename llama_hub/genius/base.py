"""Genius Reader."""
from typing import List, Optional
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import lyricsgenius

class GeniusReader(BaseReader):
    """GeniusReader for various operations with lyricsgenius."""

    def __init__(self, access_token: str):
        """Initialize the GeniusReader with an access token."""
        self.genius = lyricsgenius.Genius(access_token)

    def load_artist_songs(self, artist_name: str, max_songs: Optional[int] = None) -> List[Document]:
        """Load all or a specified number of songs by an artist."""
        artist = self.genius.search_artist(artist_name, max_songs=max_songs)
        return [Document(text=song.lyrics) for song in artist.songs] if artist else []

    def load_song_by_url_or_id(self, song_url: Optional[str] = None, song_id: Optional[int] = None) -> List[Document]:
        """Load song by URL or ID."""
        if song_url:
            song = self.genius.song(url=song_url)
        elif song_id:
            song = self.genius.song(song_id)
        else:
            return []

        return [Document(text=song.lyrics)] if song else []

    def load_songs_by_tag(self, tag: str, max_songs: Optional[int] = None) -> List[Document]:
        """Load songs by a specific tag (genre)."""
        # Implement functionality to fetch songs by tag using lyricsgenius

    def search_songs_by_lyrics(self, lyrics: str) -> List[Document]:
        """Search for songs by a snippet of lyrics."""
        songs = self.genius.search_songs(lyrics)
        return [Document(text=song.lyrics) for song in songs['hits']] if songs else []

    # Additional methods can be implemented for other features like:
    # - Least popular song of an artist
    # - Fetching YouTube URLs
    # - OAuth2 authentication (if required for specific endpoints)

if __name__ == "__main__":
    reader = GeniusReader("gUmUyikTQi7yoLuSdqHrsXCQYBH6XBd4PjlH1Uh9XGG9RWBJstuiZOxYYgXRwm7U")
    # Example usage
    print(reader.load_artist_songs("Chance the Rapper", max_songs=1))
