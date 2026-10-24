
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

def start_download():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning(
            "Missing URL",
        )
        return

    status_label.config(
        text="downloader not connected yet.",
        fg="#FFD166"
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
