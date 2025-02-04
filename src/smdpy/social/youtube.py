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
    """

    def __init__(self, url: str):
        """
        Initialize with a YouTube video URL.
        """
        self.url = url
        self.info_cache: Dict[str, Any] = {}

    def _extract_info(self) -> Dict[str, Any]:
        """
        Use yt-dlp to extract metadata (no download).
        Caches the info so we only run extract once.
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
        Return a sorted list of resolution labels like ["360p", "720p60", "1080p60"].
        """
        info = self._extract_info()
        formats = info.get('formats', [])
        resolution_labels = set()

        for f in formats:
            if f.get('vcodec') != 'none':
                height = f.get('height')
                fps = f.get('fps')
                if height:
                    label = f"{height}p"
                    # If fps is > 30, append it e.g. "60"
                    if fps and fps > 30:
                        label += str(int(fps))
                    resolution_labels.add(label)

        # Sort by the height number (e.g. "1080" in "1080p60")
        def resolution_key(lbl: str) -> int:
            match_num = re.search(r'(\d+)p', lbl)
            return int(match_num.group(1)) if match_num else 0

        return sorted(resolution_labels, key=resolution_key)

    def download_video(self, path: str, name: str, resolution_label: str) -> Dict[str, Any]:
        """
        Download the video at the chosen resolution/fps label, e.g. "1080p60".
        """
        info = self._extract_info()
        all_formats = info.get('formats', [])

        # Parse the label "1080p60" => height=1080, fps=60
        match = re.match(r'(\d+)p(\d+)?', resolution_label)
        if not match:
            return {
                "success": False,
                "filepath": "",
                "message": f"Invalid resolution label '{resolution_label}'"
            }

        height_str, fps_str = match.groups()
        target_height = int(height_str)
        target_fps = int(fps_str) if fps_str else None

        # Collect all formats that match this height (and fps if specified)
        matching_formats = []
        for f in all_formats:
            if f.get('vcodec') == 'none':  # audio-only
                continue

            if f.get('height') == target_height:
                if target_fps:
                    # Allow small tolerance in case it's e.g. 59.94 vs 60
                    if f.get('fps') and abs(f['fps'] - target_fps) < 2:
                        matching_formats.append(f)
                else:
                    # No specific fps requirement
                    matching_formats.append(f)

        if not matching_formats:
            return {
                "success": False,
                "filepath": "",
                "message": (
                    f"No format found for '{resolution_label}'. Possibly the video "
                    f"doesn't have that exact resolution/fps."
                )
            }

        # Pick the best candidate by highest total bitrate (tbr)
        matching_formats.sort(key=lambda x: x.get('tbr') or 0, reverse=True)
        chosen_format_id = matching_formats[0]['format_id']

        # Build yt-dlp options
        outtmpl = os.path.join(path, f"{name}.%(ext)s")
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': f"{chosen_format_id}+bestaudio/best",
            'outtmpl': outtmpl,
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
        Download only the audio track as an MP3.
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
                "message": "Downloaded MP3 successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": "",
                "message": f"Download failed: {str(e)}"
            }