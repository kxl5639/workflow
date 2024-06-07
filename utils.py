import tkinter as tk
from tkinter import Toplevel, ttk

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_custom_error_message(parent_window, title, message):
    error_message_window = Toplevel()
    error_message_window.transient(parent_window)
    error_message_window.title(title)
    error_message_window.resizable(False, False)  # Make the window non-resizable
    ttk.Label(error_message_window, text=message).pack(padx=10, pady=10)
    ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    center_window(error_message_window)

    error_message_window.grab_set()  # Make the window modal
    error_message_window.focus_force()  # Focus on the error message window
    parent_window.wait_window(error_message_window)  # Wait until the error message window is closed

def only_one_project_selected(tree):
    selected_items = tree.selection()    
    if len(selected_items) > 1:
        return False
    else:
        return True
