# Youtube Downloader
YouTube audio downloader with a simple UI. Download only things with permission/legally. 

### Simply paste your url, choose the bitrate, and download the mp3 file to your computer!

<img width="730" height="691" alt="Screenshot 2026-10-25 at 7 13 31 PM" src="https://github.com/user-attachments/assets/7a585fda-68d0-4a71-9d8c-78e73219239b" />

## How to Run
> regardless of your method, FFmpeg is NEEDED for this to work!!! It converts the audio file to mp3.

1. Install [FFmpeg](https://ffmpeg.org/). FFmpeg is neccesary for the download feature (yt-dlp specifically) to work. It is NOT included in the .app (I installed via Homebrew)
2. Go to release and [downlaod the zip file](https://github.com/David12213/Music-Downloader/releases/tag/v1.0). The file is .app (I use Mac). If your on windows, look at alternative below.
3. run the app, paste your youtube url, and download away. All downloads are saved in a JSON file.

Alternatively, you could:
1. Clone/download this repository (Speicifcally [music_downloader.py](https://github.com/David12213/Music-Downloader/blob/419abaf6b0a7b443a96f6c107355946c5c2f2cc5/music_downloader.py))
2. install python, [FFmpeg](https://ffmpeg.org/), and the yt-dlp library.
3. run the [music_downloader.py file](https://github.com/David12213/Music-Downloader/blob/419abaf6b0a7b443a96f6c107355946c5c2f2cc5/music_downloader.py) on your code editor, paste your URL, and download away.
4. If you need to see your past downloads or lose the url, go to the history page, look for the song title, and double click to get the url for it. Your history is saved as a JSON file. 

## Requirements

- **Python:** Python 3.12 or up (I use 3.15, yt-dlp needs version 3.11 minimum)
- **Libraries:** `yt-dlp`; all other libraries included with Python. If you do not have Tktinter (normally comes with Python), download that as well.
- **FFmpeg:** Required for MP3 conversion, downloaded separately. (I downloaded via Homebrew on Mac)
- **Internet Connection** needed to download from online sites.

## Sites to download from:
You can download from anything in these [sites](<https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)>). The sites you can download from are controlled by yt-dlp.

## Features:
- A download progress bar, showing how far a long a download is.
- A speed & time left bar, representing download speed and the time left until download is over.
- a settings menu to the change the bitrate at which something is downloaded. There are 3 settings for it.
- A history setting to show your past downloads. If you double click on them, you will get the url. 
- The folder you choose to download to will automatically open up when download finishes to show you where audio file went.

## Notice/Why I made:
> This entire thing was built around my mac, I 90% sure it works on windows as well.
A lot of those "download youtube video" websites are super scummy and 50% of them turn out to be viruses. It's kinda hard to trust any of them. So, when I learned it's a program that you can download, I figured id build my own to get some music onto a ipod i found. Anyways, this project is my UI + the url downloader. As for now, the audio quality feels pretty solid and im satisfied. (Although I could be wrong). I easily uploaded the downloaded files to apple music to stream on the cloud, so it works great!



