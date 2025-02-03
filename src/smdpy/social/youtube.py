import os
import re
from typing import List, Dict, Any

import yt_dlp


class YouTube:
    """
    A simple wrapper around yt-dlp to:
      - get available video resolutions (as labels like '720p', '1080p60')
      - download video in chosen resolution
      - download audio as MP3

    Attributes
    ----------
    url : str
        The YouTube URL to download from.
    info_cache : dict
        Internal cache for metadata after extracting info with yt-dlp.

    Examples
    --------
    >>> yt = YouTube("https://youtu.be/dQw4w9WgXcQ")
    >>> print(yt.get_available_resolutions())
    ['144p', '240p', '360p', '720p']
    >>> yt.download_video(path="videos", name="my_video", resolution_label="720p")
    {'success': True, 'filepath': 'videos/my_video.mp4', 'message': 'Downloaded 720p successfully'}
    >>> yt.download_audio_mp3(path="audios", name="my_audio", quality="192")
    {'success': True, 'filepath': 'audios/my_audio.mp3', 'message': 'Downloaded MP3 successfully'}
    """

    def __init__(self, url: str):
        """
        Initialize the YouTube class with a given video URL.

        Parameters
        ----------
        url : str
            The full YouTube video URL (e.g., https://youtu.be/xxxx).
        """
        self.url = url
        self.info_cache: Dict[str, Any] = {}

    def _extract_info(self) -> Dict[str, Any]:
        """
        Use yt-dlp to extract metadata and format info for the video (no download).
        We store the result in `self.info_cache` so we don't re-extract multiple times.

        Returns
        -------
        Dict[str, Any]
            A dictionary of video metadata, including 'formats'.
        """
        if not self.info_cache:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.info_cache = ydl.extract_info(self.url, download=False)
        return self.info_cache

    def get_available_resolutions(self) -> List[str]:
        """
        Get a sorted list of all available video resolution labels (e.g. ['144p', '720p60']).

        Returns
        -------
        List[str]
            Sorted resolution labels like ['144p', '360p', '720p', '720p60', '1080p60'].
        """
        info = self._extract_info()
        formats = info.get('formats', [])
        resolution_labels = set()

        for f in formats:
            # Only consider entries that have video (vcodec != 'none')
            if f.get('vcodec') != 'none':
                height = f.get('height')
                fps = f.get('fps')
                if height:
                    label = f"{height}p"
                    # If fps is higher than ~30, append e.g. '60'
                    if fps and fps > 30:
                        label += str(int(fps))
                    resolution_labels.add(label)

        def resolution_key(lbl: str) -> int:
            # Extract the integer before 'p', e.g. "720p60" -> 720
            match_num = re.search(r'(\d+)p', lbl)
            return int(match_num.group(1)) if match_num else 0

        return sorted(list(resolution_labels), key=resolution_key)

    def download_video(self, path: str, name: str, resolution_label: str) -> Dict[str, Any]:
        """
        Download the YouTube video in a chosen resolution. If it's an adaptive format,
        yt-dlp merges the best audio track automatically into MP4.

        Parameters
        ----------
        path : str
            The directory to save the downloaded file.
        name : str
            Filename (without extension) for the saved video.
        resolution_label : str
            Desired resolution label, e.g. "360p", "720p", "720p60", "1080p60".

        Returns
        -------
        Dict[str, Any]
            {
                "success": bool,         # True if download succeeded, else False
                "filepath": str,         # Path to the downloaded .mp4 file
                "message": str           # Brief status message
            }

        Raises
        ------
        ValueError
            If the requested resolution isn't available.
        """
        info = self._extract_info()
        formats = info.get('formats', [])

        # Build a dict of label -> list of format_ids
        label_to_fids = {}
        for f in formats:
            if f.get('vcodec') != 'none':
                h = f.get('height')
                fps = f.get('fps', 30)
                if h:
                    lbl = f"{h}p"
                    if fps > 30:
                        lbl += str(int(fps))
                    label_to_fids.setdefault(lbl, []).append(f['format_id'])

        if resolution_label not in label_to_fids:
            available = list(label_to_fids.keys())
            raise ValueError(f"No format found for '{resolution_label}'. "
                             f"Available resolutions: {available}")

        # Pick the first format_id for that label
        chosen_format_id = label_to_fids[resolution_label][0]

        # Construct yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': f"{chosen_format_id}+bestaudio/best",
            'outtmpl': os.path.join(path, f"{name}.%(ext)s"),
            'merge_output_format': 'mp4',
        }

        os.makedirs(path, exist_ok=True)
        final_filepath = os.path.join(path, f"{name}.mp4")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return {
                "success": True,
                "filepath": final_filepath,
                "message": f"Downloaded {resolution_label} successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": "",
                "message": f"Download failed: {str(e)}"
            }

    def download_audio_mp3(self, path: str, name: str, quality: str = "192") -> Dict[str, Any]:
        """
        Download audio from the YouTube video as an MP3 file, using FFmpeg.

        Parameters
        ----------
        path : str
            The directory to save the MP3 file.
        name : str
            Filename (without extension) for the saved audio.
        quality : str, optional
            MP3 bitrate (e.g. "128", "192", "320"), default "192".

        Returns
        -------
        Dict[str, Any]
            {
                "success": bool,         # True if download succeeded, else False
                "filepath": str,         # Path to the downloaded .mp3 file
                "message": str           # Brief status message
            }
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(path, f"{name}.%(ext)s"),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }
            ],
        }
        os.makedirs(path, exist_ok=True)
        final_filepath = os.path.join(path, f"{name}.mp3")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return {
                "success": True,
                "filepath": final_filepath,
                "message": f"Downloaded MP3 successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": "",
                "message": f"Download failed: {str(e)}"
            }
