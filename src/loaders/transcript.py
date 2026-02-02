from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str) -> str:
    yt=YouTubeTranscriptApi()
    try:
        transcript = yt.fetch(video_id, languages=["en"])
        lang = "en"
    except Exception:
        transcript = yt.fetch(video_id, languages=["hi"])
        lang = "hi"

    text = " ".join([t.text for t in transcript])
    return text, lang