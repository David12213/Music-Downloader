import json
import queue
import threading
from pathlib import Path
from urllib.parse import urlparse
import tkinter as tk
import yt_dlp
import subprocess
from tkinter import ttk, filedialog, messagebox

HISTORY_FILE = Path(__file__).resolve().parent / "music_downloader_history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_history(history):
    try:
        temp_file = HISTORY_FILE.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)
        temp_file.replace(HISTORY_FILE)
    except OSError:
        messagebox.showerror("History Save Error", "Could not save download history.")

download_history = load_history()

def refresh_history():
    history_list.delete(0, tk.END)

    for index, song in enumerate(reversed(download_history), start=1):
        title = song.get("title") or song.get("url", "Unknown title")
        history_list.insert(tk.END, f"{index}. {title}")

def song_details(event=None):
    selection = history_list.curselection()

    if not selection:
        return

    index = len(download_history) - 1 - selection[0]
    song = download_history[index]
    url = song.get("url", "")
    title = song.get("title", "Unknown title")

    popup = tk.Toplevel(root)
    popup.title("Song Details")
    popup.geometry("600x200")
    popup.configure(bg=BACKGROUND)
    popup.resizable(False, False)

    tk.Label(
        popup,
        text=title,
        font=("Times New Roman", 16, "bold"),
        bg=BACKGROUND,
        fg=TEXT,
        wraplength=550
    ).pack(pady=(15, 10))

    url_entry = ttk.Entry(popup, width=75)
    url_entry.pack(padx=20, pady=5, fill="x")
    url_entry.insert(0, url)
    url_entry.config(state="readonly")

    def copy_url():
        popup.clipboard_clear()
        popup.clipboard_append(url)
        popup.update()
        messagebox.showinfo(
            "Copied",
            "URL copied to clipboard!",
            parent=popup
        )

    ttk.Button(
        popup,
        text="Copy URL",
        command=copy_url,
        style="Custom.TButton",
    ).pack(pady=10)

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("340x270")
    settings_window.configure(bg=BACKGROUND)
    settings_window.resizable(False, False)

    tk.Label(
        settings_window,
        text="SETTINGS",
        font=("Times New Roman", 18, "bold"),
        bg=BACKGROUND,
        fg=TEXT,
    ).pack(anchor="w", padx=24, pady=24)

    tk.Label(
        settings_window,
        text="Audio quality",
        font=("Times New Roman", 11, "bold"),
        bg=BACKGROUND,
        fg=TEXT,
    ).pack(anchor="w", padx=24, pady=(16))

    tk.Label(
        settings_window,
        text="Higher bitrates make larger files",
        font=("Times New Roman", 11),
        bg=BACKGROUND,
        fg="#929292",
    ).pack(anchor="w", padx=24, pady=12)

    for quality in ("128", "192", "320"):
        tk.Radiobutton(
            settings_window,
            text=f"{quality} kbps",
            variable=audio_quality,
            value=quality,
            bg=BACKGROUND,
            fg=TEXT,
            selectcolor="#292929",
            activebackground=BACKGROUND,
            activeforeground=TEXT,
            font=("Times New Roman", 11)
        ).pack(anchor="w", padx=30, pady=2)

    ttk.Button(
        settings_window,
        text="Done",
        command=settings_window.destroy,
        style="Custom.TButton",
    ).pack(fill="x", padx=24, pady=(16, 20))

root = tk.Tk()
audio_quality = tk.StringVar(master=root, value="192")
root.title("Music Downloader")
root.geometry("760x750")
root.resizable(False, False)

BACKGROUND = "#202020"
PANEL = "#2B2B2B"
TEXT = "#FFFFFF"

root.configure(bg=BACKGROUND)
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TEntry", fieldbackground=PANEL, foreground=TEXT)

style.configure(
    "Custom.TButton",
    background=PANEL,
    foreground=TEXT,
    padding=10,
    font=("Times New Roman", 12, "bold"),
)
style.map("Custom.TButton", background=[("active", "#3A3A3A")])

style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor="#2B2B2B",
    background="#FFFFFF",
    bordercolor="#2B2B2B",
    lightcolor="#FFFFFF",
    darkcolor="#FFFFFF",
)

header_frame = tk.Frame(root, bg=BACKGROUND)
header_frame.pack(fill="x", padx=35, pady=(24, 4))

title = tk.Label(
    header_frame,
    text="Music Downloader",
    font=("Times New Roman", 25, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
)
title.place(relx=0.5, rely=0.5, anchor="center")

settings_button = ttk.Button(
    header_frame,
    text="Settings ⚙",
    command=open_settings,
    style="Custom.TButton",
)
settings_button.pack(side="right")

subtitle = tk.Label(
    root,
    text="A YouTube video to MP3 downloader",
    font=("Times New Roman", 11),
    bg=BACKGROUND,
    fg="#BBBBBB",
)
subtitle.pack(pady=(0, 22))

url_label = tk.Label(
    root,
    text="Audio source URL",
    font=("Times New Roman", 11, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
)
url_label.pack(anchor="center")

url_entry = ttk.Entry(root, width=55, style="Custom.TEntry")
url_entry.pack(padx=35, pady=(7, 15), ipady=7)

download_queue = queue.Queue()

def progress_hook(data):
    info = data.get("info_dict") or {}

    playlist_index = info.get("playlist_index") or 1
    playlist_count = info.get("playlist_count") or 1
    song_title = info.get("title") or "Current song"

    if data.get("status") == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        if total:
            song_percentage = min((downloaded / total) * 100, 100)
        else:
            song_percentage = None

        if song_percentage is not None:
            overall_percentage = (
                (playlist_index - 1 + song_percentage / 100)
                / playlist_count
            ) * 100
        else:
            overall_percentage = (
                (playlist_index - 1) / playlist_count
            ) * 100

        speed = data.get("speed")
        eta = data.get("eta")

        download_queue.put((
            "progress",
            song_percentage,
            overall_percentage,
            speed,
            eta,
            playlist_index,
            playlist_count,
            song_title,
        ))

    elif data.get("status") == "finished":
        download_queue.put((
            "status",
            f"Converting to MP3: {song_title}"
        ))

def process_download_queue():
    try:
        while True:
            item = download_queue.get_nowait()
            event = item[0]

            if event == "progress":
                (
                    _,
                    song_percentage,
                    overall_percentage,
                    speed,
                    eta,
                    playlist_index,
                    playlist_count,
                    song_title,
                ) = item

                #playlist progress
                overall_progress_bar["value"] = overall_percentage

                #song progress
                if song_percentage is not None:
                    song_progress_bar["value"] = song_percentage
                    song_progress_text = f"{song_percentage:.1f}%"
                else:
                    song_progress_text = "--"

                progress_label.config(
                    text=(
                        f"Playlist: {overall_percentage:.1f}%"
                        f"  |  Song {playlist_index}/{playlist_count}: "
                        f"{song_progress_text}"
                    ),
                    fg=TEXT,
                )

                current_song_label.config(
                    text=f"Current song: {song_title}"
                )

                if speed is not None and speed > 0:
                    if speed >= 1024 ** 2:
                        speed_text = f"{speed / (1024 ** 2):.2f} MB/s"
                    else:
                        speed_text = f"{speed / 1024:.1f} KB/s"

                    speed_label.config(text=f"Speed: {speed_text}")
                else:
                    speed_label.config(text="Speed: --")

                if eta is not None and eta > 0:
                    eta = int(eta)

                    if eta >= 60:
                        minutes, seconds = divmod(eta, 60)
                        time_label.config(
                            text=f"Time left: {minutes}m {seconds}s"
                        )
                    else:
                        time_label.config(
                            text=f"Time left: {eta}s"
                        )
                else:
                    time_label.config(text="Time left: --")

                status_label.config(text="Downloading audio...", fg="#FFD166")

            elif event == "status":
                status_label.config(text=item[1], fg="#FFD166")

            elif event == "success":
                url = item[1]
                title = item[2]
                subprocess.Popen(["open", last_download_folder])

                if not any(song.get("url") == url for song in download_history):
                    download_history.append({"url": url, "title": title})
                    save_history(download_history)

                refresh_history()

                overall_progress_bar["value"] = 100
                song_progress_bar["value"] = 100

                progress_label.config(
                    text="Playlist: 100%  |  Complete!",
                    fg="#7CFC98",
                )
                status_label.config(text="All downloads complete!", fg="#7CFC98")
                current_song_label.config(text="")
                speed_label.config(text="Speed: ")
                time_label.config(text="Time left: Complete")

                download_button.config(state="normal")

                messagebox.showinfo(
                    "Success",
                    "Your MP3 file(s) have been saved!"
                )

            elif event == "error":
                progress_label.config(text="Download failed.", fg="#E53935")
                status_label.config(text="Download failed.", fg="#E53935")

                speed_label.config(text="Speed: ")
                time_label.config(text="Time left: ")

                download_button.config(state="normal")
                messagebox.showerror("Download Error", item[1])

    except queue.Empty:
        pass
    except Exception as error:
        print(f"Progress display error: {error}")
    finally:
        root.after(100, process_download_queue)

def is_valid_url(value):
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)

last_download_folder = None
def start_download():
    global last_download_folder
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a URL first.")
        return

    if not is_valid_url(url):
        messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
        return

    output_folder = filedialog.askdirectory(
        title="Choose where to save your MP3"
    )
    if not output_folder:
        return

    last_download_folder = output_folder

    overall_progress_bar["value"] = 0
    song_progress_bar["value"] = 0

    progress_label.config(text="Preparing download...", fg="#FFD166")
    status_label.config(text="Starting download...", fg="#FFD166")
    current_song_label.config(text="")

    speed_label.config(text="Speed: --")
    time_label.config(text="Time left: --")

    download_button.config(state="disabled")

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(output_folder) / "%(title)s.%(ext)s"),
        "noplaylist": False,
        "restrictfilenames": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality.get(),
            }
        ],
    }

    def download_worker():
        try:
            with yt_dlp.YoutubeDL(options) as downloader:
                info = downloader.extract_info(url, download=False)
                title = info.get("title", "Unknown title")
                downloader.download([url])

            download_queue.put(("success", url, title))

        except Exception as error:
            message = str(error)
            if "ffmpeg" in message.lower():
                message = "FFmpeg is not installed or not available in PATH."
            download_queue.put(("error", message))

    threading.Thread(target=download_worker, daemon=True).start()

download_button = ttk.Button(
    root,
    text="Download Audio",
    command=start_download,
    style="Custom.TButton",
    width=25,
)
download_button.pack(pady=9)

#playlist progress bar
tk.Label(
    root,
    text="Overall playlist progress",
    font=("Times New Roman", 10, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
).pack(pady=(3, 0))

overall_progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=360,
    mode="determinate",
    maximum=100,
    style="Custom.Horizontal.TProgressbar",
)
overall_progress_bar.pack(pady=4)

#current song progress
tk.Label(
    root,
    text="Current song progress",
    font=("Times New Roman", 10, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
).pack(pady=(5, 0))

song_progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=360,
    mode="determinate",
    maximum=100,
    style="Custom.Horizontal.TProgressbar",
)
song_progress_bar.pack(pady=4)

progress_details_frame = tk.Frame(root, bg=BACKGROUND)
progress_details_frame.pack(fill="x", padx=35, pady=(6, 2))

speed_label = tk.Label(
    progress_details_frame,
    text="Speed: --",
    font=("Times New Roman", 10, "bold"),
    bg=BACKGROUND,
    fg="#BBBBBB",
)
speed_label.pack(side="left")

time_label = tk.Label(
    progress_details_frame,
    text="Time left: --",
    font=("Times New Roman", 10, "bold"),
    bg=BACKGROUND,
    fg="#BBBBBB",
)
time_label.pack(side="right")

progress_label = tk.Label(
    root,
    text="Ready to Download",
    font=("Times New Roman", 12),
    bg=BACKGROUND,
    fg=TEXT,
)
progress_label.pack(pady=4)

current_song_label = tk.Label(
    root,
    text="",
    font=("Times New Roman", 10),
    bg=BACKGROUND,
    fg="#BBBBBB",
    wraplength=680,
)
current_song_label.pack(pady=2)

status_label = tk.Label(
    root,
    text="",
    font=("Times New Roman", 11),
    bg=BACKGROUND,
    fg="#FFD166",
)
status_label.pack(pady=2)

history_label = tk.Label(
    root,
    text="Download History (Double Click for URL)",
    font=("Times New Roman", 12, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
)
history_label.pack(pady=(12, 4))

history_list = tk.Listbox(
    root,
    width=60,
    height=5,
    bg=PANEL,
    fg=TEXT,
    selectbackground="#555555",
    font=("Times New Roman", 10),
)
history_list.pack(padx=35, pady=4)
history_list.bind("<Double-Button-1>", song_details)

refresh_history()
root.after(100, process_download_queue)
root.mainloop()