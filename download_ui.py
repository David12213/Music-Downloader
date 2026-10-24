
import tkinter as tk
import yt_dlp
from tkinter import ttk, filedialog, messagebox
from pydub import AudioSegment


input_file=""

root = tk.Tk()
root.title("Music Downloader")
root.geometry("520x380")
root.resizable(False, False)

# Colors
BACKGROUND = "#202020"
PANEL = "#2B2B2B"
TEXT = "#FFFFFF"
ACCENT = "#E53935"

root.configure(bg=BACKGROUND)

# Widget styles
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Custom.TEntry",
    fieldbackground=PANEL,
    foreground=TEXT
)

style.configure(
    "Custom.TButton",
    background=PANEL,
    foreground=TEXT,
    padding=10,
    font=("Times New Roman", 12, "bold")
)

style.map(
    "Custom.TButton",
    background=[("active", "#3A3A3A")]
)

title = tk.Label(
    root,
    text="Music Downloader",
    font=("Times New Roman", 25, "bold"),
    bg=BACKGROUND,
    fg=TEXT
)
title.pack(pady=(24, 4))

subtitle = tk.Label(
    root,
    text="A Youtube video to mp3 downloader",
    font=("Times New Roman", 11),
    bg=BACKGROUND,
    fg="#BBBBBB"
)
subtitle.pack(pady=(0, 22))

url_label = tk.Label(
    root,
    text="Audio source URL",
    font=("Times New Roman", 11, "bold"),
    bg=BACKGROUND,
    fg=TEXT
)
url_label.pack(anchor="w", padx=35)

url_entry = ttk.Entry(
    root,
    width=55,
    style="Custom.TEntry"
)
url_entry.pack(padx=35, pady=(7, 15), ipady=7)

def convertto_mp3(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format ="mp3")


def start_download():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning(
            "Missing URL",
            "Please enter a URL first."
        )
        return

    output_folder = filedialog.askdirectory(
        title="Choose where to save your MP3"
    )

    if not output_folder:
        return

    status_label.config(
        text="Downloading audio...",
        fg="#FFD166"
    )
    root.update_idletasks()

    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download([url])

        status_label.config(
            text="Download complete!",
            fg="#7CFC98"
        )
        messagebox.showinfo(
            "Success",
            "Your MP3 has been saved!"
        )

    except Exception as error:
        status_label.config(
            text="Download failed.",
            fg="#E53935"
        )
        messagebox.showerror(
            "Download Error",
            str(error)
        )

download_button = ttk.Button(
    root,
    text="Download Audio",
    command=start_download,
    style="Custom.TButton",
    width=25
)
download_button.pack(pady=9)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Times New Roman", 10),
    bg=BACKGROUND,
    fg=TEXT
)
status_label.pack(pady=12)

root.mainloop()
