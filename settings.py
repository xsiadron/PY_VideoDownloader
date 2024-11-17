import tkinter as tk
from tkinter import ttk
from translations import translations

current_language = 'pl'
current_theme = 'azure-light'

def set_theme(root, theme):
    style = ttk.Style()
    root.tk.call("ttk::style", "theme", "use", theme)
    bg_color = "#2d2d2d" if theme == "azure-dark" else "#f0f0f0"
    fg_color = "#ffffff" if theme == "azure-dark" else "#000000"
    root.configure(bg=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TRadiobutton", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=bg_color, foreground=fg_color)
    style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
    style.configure("TCombobox", fieldbackground=bg_color, background=bg_color, foreground=fg_color)

def open_settings(root, apply_theme):
    window = tk.Toplevel(root)
    window.title(translations[current_language]['settings'])
    window.geometry("300x300")
    
    def update_theme():
        apply_theme(theme_var.get())

    def save_settings():
        global current_language, current_theme
        current_language = language_var.get()
        current_theme = theme_var.get()
        apply_theme(current_theme)
        window.destroy()

    bg_color = "#2d2d2d" if current_theme == "azure-dark" else "#f0f0f0"
    fg_color = "#ffffff" if current_theme == "azure-dark" else "#000000"
    window.configure(bg=bg_color)

    language_var = tk.StringVar(value=current_language)
    ttk.Label(window, text=translations[current_language]['language']).pack(pady=10)
    ttk.Radiobutton(window, text='Polski', variable=language_var, value='pl').pack(anchor='w', padx=20)
    ttk.Radiobutton(window, text='English', variable=language_var, value='en').pack(anchor='w', padx=20)

    theme_var = tk.StringVar(value=current_theme)
    ttk.Label(window, text="Motyw").pack(pady=20)
    ttk.Radiobutton(window, text='Jasny', variable=theme_var, value='azure-light', command=update_theme).pack(anchor='w', padx=20)
    ttk.Radiobutton(window, text='Ciemny', variable=theme_var, value='azure-dark', command=update_theme).pack(anchor='w', padx=20)

    ttk.Button(window, text="Zapisz", command=save_settings).pack(pady=20)
