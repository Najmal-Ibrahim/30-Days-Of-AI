print("1. Importing library...")
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

print(f"2. Library Location: {youtube_transcript_api.__file__}")
# This tells us if it's loading from .venv (Good) or your Desktop (Bad)

print("3. Testing fetch...")
try:
    # Test video: "Google" (Short, has captions)
    # Video ID: K4TOrB7at0Y
    transcript = YouTubeTranscriptApi.get_transcript("K4TOrB7at0Y")
    print("\nSUCCESS! Found transcript:")
    print(transcript[0])
except Exception as e:
    print(f"\nFAILURE: {e}")
    print(f"Available attributes in library: {dir(YouTubeTranscriptApi)}")