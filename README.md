# SMDP - Social Media Downloader (PyPI Package)

**SMDP** is a Python package that allows you to download videos from **YouTube** and **Instagram** effortlessly. With
SMDP, you can fetch videos in various resolutions (e.g., 360p, 720p, 1080p) from YouTube and download Instagram videos
with ease. It's perfect for developers who want to integrate social media downloading capabilities into their
applications.

---

## Features ✨

- **YouTube Video Downloader**:
    - Fetch videos in multiple resolutions (360p, 480p, 720p, 1080p, etc.).
    - Extract video details like title, description, and thumbnail.
- **Instagram Video Downloader**:
    - Download videos from posts, reels, and IGTV.
    - Simple and straightforward API.
- **Lightweight and Easy to Use**:
    - Designed for developers with a clean and intuitive API.
- **No Dependencies**:
    - Built with pure Python; no external tools like FFmpeg required.

---

## Installation 📦

Install SMDP directly from PyPI using pip:

```bash
pip install smdp
```

# Usage 🚀

# 1. Download YouTube Videos

```python
from smdpy.youtube import YouTube
```

## 1.1. Initialize the YouTube downloader with the video URL

```python
yt = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

## 1.2. Get available video formats

```python
formats = yt.get_formats()
for fmt in formats:
    print(f"Resolution: {fmt['resolution']}, Format: {fmt['mime_type']}, URL: {fmt['url']}")
```

## 1.3. Download a specific format (e.g., 720p) and save it as 'video.mp4'

```python
yt.download(format="720p", output_path="video.mp4")
```

# 2. Download Instagram Videos

```python
from smdpy.instagram import Instagram
```

## 2.1. Initialize the Instagram downloader with the post URL

```python
ig = Instagram("https://www.instagram.com/p/example_post_id/")
```

## 2.2. Get the direct video URL

```python
video_url = ig.get_video_url()
print(f"Video URL: {video_url}")
```

## 2.3. Download the video and save it as 'instagram_video.mp4'

```python
ig.download(output_path="instagram_video.mp4")
```

## API Reference 📚

### `smdpy.youtube.YouTube`

**Constructor:**

- `YouTube(video_url: str)`: Initializes the YouTube downloader.

**Methods:**

- `get_formats() -> List[Dict[str, str]]`: Returns a list of available video formats with details (resolution, MIME
  type, download URL).
- `download(format: str, output_path: str)`: Downloads the video in the specified format (e.g., "720p") and saves it to
  `output_path`.

### `smdpy.instagram.Instagram`

**Constructor:**

- `Instagram(post_url: str)`: Initializes the Instagram downloader.

**Methods:**

- `get_video_url() -> str`: Returns the direct download URL of the video.
- `download(output_path: str)`: Downloads the video and saves it to `output_path`.

## Example Use Cases 🌟

- **Download YouTube Videos in Bulk**:
  Fetch multiple videos in different resolutions and save them locally.

- **Integrate Instagram Downloads into Your App**:
  Allow users to download Instagram videos directly from your platform.

- **Build a Video Archiver**:
  Automate the process of downloading and archiving videos from social media.

## Contributing 🤝

We welcome contributions! To improve SMDP, you can:

- Report bugs or suggest features by opening an issue.
- Submit pull requests with your enhancements.

## License 📜

SMDP is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support ☕

If you find SMDP useful, please consider supporting the project by:

- Starring the [repository](https://github.com/Shaxzodbek16/smdpy). on GitHub.
- Sharing it with your friends and colleagues.
- [Buy me a coffee](https://www.buymeacoffee.com/Shaxzodbek16).
- [Sponsoring the developer on GitHub](https://github.com/sponsors/Shaxzodbek16).

## Disclaimer ⚠️

SMDP is intended for personal use only. Please respect the copyright and terms of service of the platforms you download
from. The developers are not responsible for any misuse of this tool.

### Enjoy using SMDP to download your favorite social media videos! 🎉