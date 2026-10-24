
import tkinter as tk
import yt_dlp
import threading
import queue
from tkinter import ttk, filedialog, messagebox

root = tk.Tk()
root.title("Music Downloader")
root.geometry("520x430")
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

download_queue = queue.Queue()

def progress_hook(data):
    if data["status"] == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = (
            data.get("total_bytes")
            or data.get("total_bytes_estimate")
        )

        if total:
            percentage = downloaded / total * 100
        else:
            percentage = None

        speed = data.get("speed")
        eta = data.get("eta")

        download_queue.put(
            ("progress", percentage, speed, eta)
        )

    elif data["status"] == "finished":
        download_queue.put(
            ("status", "Converting audio to MP3...")
        )


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
                        details += f" | {speed / 1024**2:.2f} MB/s"

                    if eta is not None:
                        details += f" | ETA: {eta}s"

                    progress_label.config(text=details)

            elif event == "status":
                progress_label.config(
                    text=item[1],
                    fg="#FFD166"
                )

            elif event == "success":
                progress_bar["value"] = 100
                progress_label.config(
                    text="100% — Complete!",
                    fg="#7CFC98"
                )
                download_button.config(state="normal")

                messagebox.showinfo(
                    "Success",
                    "Your MP3 has been saved!"
                )

            elif event == "error":
                progress_label.config(
                    text="Download failed.",
                    fg="#E53935"
                )
                download_button.config(state="normal")

                messagebox.showerror(
                    "Download Error",
                    item[1]
                )

    except queue.Empty:
        pass

    root.after(100, process_download_queue)


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

    progress_bar["value"] = 0
    progress_label.config(
        text="Downloading audio...",
        fg="#FFD166"
    )
    download_button.config(state="disabled")

    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "noplaylist": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    def download_worker():
        try:
            with yt_dlp.YoutubeDL(options) as downloader:
                downloader.download([url])

            download_queue.put(("success",))

        except Exception as error:
            download_queue.put(("error", str(error)))

    threading.Thread(
        target=download_worker,
        daemon=True
    ).start()


download_button = ttk.Button(
    root,
    text="Download Audio",
    command=start_download,
    style="Custom.TButton",
    width=25
)
download_button.pack(pady=9)

progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=360,
    mode="determinate",
    maximum = 100
)
progress_bar.pack(pady=4)

progress_label=tk.Label(
    root,
    text="Ready to Download",
    font=("Times New Roman", 12),
    bg= BACKGROUND,
    fg=TEXT
)
progress_label.pack(pady=4)

root.after(100, process_download_queue)
root.mainloop()
