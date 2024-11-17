import tkinter as tk
from tkinter import ttk, messagebox
from downloader import download_content
from settings import open_settings, current_language, current_theme, set_theme
from translations import translations
import os

def apply_theme(theme):
    style = ttk.Style()
    root.tk.call("ttk::style", "theme", "use", theme)
    bg_color = "#2d2d2d" if theme == "azure-dark" else "#f0f0f0"
    fg_color = "#ffffff" if theme == "azure-dark" else "#000000"
    root.configure(bg=bg_color)
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=bg_color, foreground=fg_color)
    style.configure("TRadiobutton", background=bg_color, foreground=fg_color)
    style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
    style.configure("TCombobox", fieldbackground=bg_color, background=bg_color, foreground=fg_color)

root = tk.Tk()
root.title("Downloader")
root.geometry("600x400")
root.resizable(False, False)

root.tk.call('source', os.path.join('azure', 'dark.tcl'))
root.tk.call('source', os.path.join('azure', 'light.tcl'))

apply_theme(current_theme)

frame = ttk.Frame(root, padding=20, style="TFrame")
frame.grid(row=0, column=0, sticky="nsew")

ttk.Label(frame, text=translations[current_language]['select_platform'], style="TLabel").grid(row=0, column=0, sticky="w", pady=10)

platform_var = tk.StringVar()
platform_combobox = ttk.Combobox(frame, textvariable=platform_var, values=["YouTube", "TikTok", "Instagram"], state="readonly", style="TCombobox")
platform_combobox.grid(row=0, column=1, pady=10)

mode_var = tk.StringVar(value='profile')
ttk.Radiobutton(frame, text=translations[current_language]['download_profile'], variable=mode_var, value='profile', style="TRadiobutton").grid(row=1, column=0, sticky="w", pady=5)
ttk.Radiobutton(frame, text=translations[current_language]['download_link'], variable=mode_var, value='link', style="TRadiobutton").grid(row=1, column=1, sticky="w", pady=5)

ttk.Label(frame, text=translations[current_language]['enter_link'], style="TLabel").grid(row=2, column=0, sticky="w", pady=10)
link_entry = ttk.Entry(frame, width=50, style="TEntry")
link_entry.grid(row=2, column=1, pady=10)

ttk.Button(frame, text=translations[current_language]['settings'], command=lambda: open_settings(root, apply_theme), style="TButton").grid(row=3, columnspan=2, pady=20)

for child in frame.winfo_children():
    child.grid_configure(padx=10, pady=5)

root.mainloop()
