import json
import queue
import threading
from pathlib import Path
from urllib.parse import urlparse

import tkinter as tk
import yt_dlp
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
    if "history_list" not in globals():
        return

    history_list.delete(0, tk.END)
    for song in download_history:
        title = song.get("title", "Unknown title")
        url = song.get("url", "")
        history_list.insert(tk.END, f"{title} — {url}")


root = tk.Tk()
root.title("Music Downloader")
root.geometry("760x600")
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

title = tk.Label(
    root,
    text="Music Downloader",
    font=("Times New Roman", 25, "bold"),
    bg=BACKGROUND,
    fg=TEXT,
)
title.pack(pady=(24, 4))

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
url_label.pack(anchor="w", padx=35)

url_entry = ttk.Entry(root, width=55, style="Custom.TEntry")
url_entry.pack(padx=35, pady=(7, 15), ipady=7)

download_queue = queue.Queue()


def progress_hook(data):
    if data.get("status") == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        if total:
            percentage = (downloaded / total) * 100
        else:
            percentage = None

        speed = data.get("speed")
        eta = data.get("eta")

        download_queue.put(("progress", percentage, speed, eta))

    elif data.get("status") == "finished":
        download_queue.put(("status", "Converting audio to MP3..."))


def process_download_queue():
    try:
        while True:
            item = download_queue.get_nowait()
            event = item[0]

            if event == "progress":
                _, percentage, speed, eta = item

                if percentage is not None:
                    progress_bar["value"] = percentage
                    details = f"{percentage:.1f}%"

                    if speed:
                        details += f" | {speed / (1024 ** 2):.2f} MB/s"

                    if eta is not None:
                        details += f" | ETA: {eta}s"

                    progress_label.config(text=details)

            elif event == "status":
                progress_label.config(text=item[1], fg="#FFD166")

            elif event == "success":
                url = item[1]
                title = item[2]

                if not any(song.get("url") == url for song in download_history):
                    download_history.append({"url": url, "title": title})
                    save_history(download_history)

                refresh_history()
                progress_bar["value"] = 100
                progress_label.config(text="100% — Complete!", fg="#7CFC98")
                download_button.config(state="normal")

                messagebox.showinfo("Success", "Your MP3 has been saved!")

            elif event == "error":
                progress_label.config(text="Download failed.", fg="#E53935")
                download_button.config(state="normal")
                messagebox.showerror("Download Error", item[1])

    except queue.Empty:
        pass

    root.after(100, process_download_queue)


def is_valid_url(value):
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def start_download():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a URL first.")
        return

    if not is_valid_url(url):
        messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
        return

    output_folder = filedialog.askdirectory(title="Choose where to save your MP3")
    if not output_folder:
        return

    progress_bar["value"] = 0
    progress_label.config(text="Downloading audio...", fg="#FFD166")
    download_button.config(state="disabled")

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(output_folder) / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
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

progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=360,
    mode="determinate",
    maximum=100,
)
progress_bar.pack(pady=4)

progress_label = tk.Label(
    root,
    text="Ready to Download",
    font=("Times New Roman", 12),
    bg=BACKGROUND,
    fg=TEXT,
)
progress_label.pack(pady=4)

history_label = tk.Label(
    root,
    text="Download History",
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

refresh_history()

root.after(100, process_download_queue)
root.mainloop()

