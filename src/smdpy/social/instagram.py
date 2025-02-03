import os
from typing import Dict, Any, Optional

import yt_dlp


class Instagram:
    """
    A simple wrapper around yt-dlp to download Instagram reels/videos in highest quality
    and optionally extract MP3 audio.

    Attributes
    ----------
    url : str
        The public Instagram post/Reel URL to download from.
    cookie_file_path : Optional[str]
        Path to a cookies.txt file for authentication, if required.

    Examples
    --------
    ig = Instagram("https://www.instagram.com/reel/xyz/", cookie_file_path="cookies.txt")
    result_vid = ig.download_video(path="downloads", name="insta_video")
    print(result_vid)
    {
        "success": True,
        "filepath": "downloads/insta_video.mp4",
        "message": "Downloaded video successfully"
    }
    result_mp3 = ig.download_audio_mp3(path="downloads", name="insta_audio")
    print(result_mp3)
    {
        "success": True,
        "filepath": "downloads/insta_audio.mp3",
        "message": "Downloaded MP3 successfully"
    }
    """

    def __init__(self, url: str, cookie_file_path: Optional[str] = None):
        """
        Initialize with a public Instagram Reel/Post URL.

        Parameters
        ----------
        url : str
            Public Instagram URL (e.g., https://www.instagram.com/reel/xxxxx/).
        cookie_file_path : str, optional
            Path to a cookies.txt file if authentication is required.
        """
        self.url = url
        self.cookie_file_path = cookie_file_path

    def download_video(self, path: str, name: str) -> Dict[str, Any]:
        """
        Download the Instagram reel/video in the highest available quality (merging audio).

        Parameters
        ----------
        path : str
            Directory to save the downloaded file.
        name : str
            Filename (without extension) for the saved video.

        Returns
        -------
        Dict[str, Any]
            {
                "success": bool,
                "filepath": str,
                "message": str
            }
        """
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(path, f"{name}.%(ext)s")
        }
        if self.cookie_file_path:
            ydl_opts["cookiefile"] = self.cookie_file_path
        os.makedirs(path, exist_ok=True)
        final_filepath = os.path.join(path, f"{name}.mp4")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return {
                "success": True,
                "filepath": final_filepath,
                "message": "Downloaded video successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": "",
                "message": f"Download failed: {str(e)}"
            }

    def download_audio_mp3(self, path: str, name: str, quality: str = "192") -> Dict[str, Any]:
        """
        Extract and download the audio track from the Instagram reel/video as MP3.

        Parameters
        ----------
        path : str
            Directory to save the MP3 file.
        name : str
            Filename (without extension) for the saved audio.
        quality : str, optional
            MP3 bitrate (e.g. "128", "192", "320"), default "192".

        Returns
        -------
        Dict[str, Any]
            {
                "success": bool,
                "filepath": str,
                "message": str
            }
        """
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(path, f"{name}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality
                }
            ]
        }
        if self.cookie_file_path:
            ydl_opts["cookiefile"] = self.cookie_file_path
        os.makedirs(path, exist_ok=True)
        final_filepath = os.path.join(path, f"{name}.mp3")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return {
                "success": True,
                "filepath": final_filepath,
                "message": "Downloaded MP3 successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": "",
                "message": f"Download failed: {str(e)}"
            }
