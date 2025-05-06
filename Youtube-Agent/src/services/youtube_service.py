import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import logging

class YouTubeService:
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def get_transcript(video_id: str) -> Optional[str]:
        """Fetch English transcript for a YouTube video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=["en"]
            )
            return " ".join(chunk['text'] for chunk in transcript_list)
        except TranscriptsDisabled:
            logging.warning(f"Transcripts disabled for video {video_id}")
            return None
        except Exception as e:
            logging.error(f"Error fetching transcript: {str(e)}")
            raise