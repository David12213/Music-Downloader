# Youtube Downloader
YouTube audio downloader with a simple UI. Download only things with permission/legally.

<img width="730" height="691" alt="Screenshot 2026-10-25 at 7 13 31 PM" src="https://github.com/user-attachments/assets/7a585fda-68d0-4a71-9d8c-78e73219239b" />

## How to Run

1. Install [FFmpeg](https://ffmpeg.org/). FFmpeg is neccesary for the download feature (yt-dlp specifically) to work. It is NOT included in the app (I installed via Homebrew)
2. Go to release and download the zip of the app
3. run the app, paste your youtube url, and download away. All downloads are saved in a JSON file.

Alternatively, you could:
1. Clone/download this repository (Speicifcally music_downloader.py)
2. install python, [FFmpeg](https://ffmpeg.org/), and the yt-dlp library
3. run the code on your code editor.

## Requirements

- **Python:** Python 3.12 or up (I use 3.15, yt-dlp needs version 3.11 minimum)
- **Libraries:** `yt-dlp`
- **FFmpeg:** Required for MP3 conversion, downloaded separately (I downloaded via Homebrew on Mac)

## Sites to download from:
You can download from anything in these [sites](<https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)>). The sites you can download from are controlled by yt-dlp.

## Features:
- A download progress bar, showing how far a long a download is.
- A speed & time left bar, representing download speed and the time left until download is over.
- a settings menu to the change the bitrate at which something is downloaded. There are 3 settings for it.
- A history setting to show your past downloads. If ou double click on them, you will get the url. 
- The folder you choose to download to will automatically open up when download finishes to show you where audio file went.