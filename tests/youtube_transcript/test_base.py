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
        "Expected youtu.be with subdomain to be invalud"
    )   