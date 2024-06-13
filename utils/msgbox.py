import tkinter as tk 
from tkinter import Toplevel, ttk
from utils.view import center_window

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

def show_custom_confirmation_message(parent_window, title, message):
    confirmation_window = Toplevel()
    confirmation_window.transient(parent_window)
    confirmation_window.title(title)
    confirmation_window.resizable(False, False)
    result = {'value': None}

    def on_yes():
        result['value'] = True
        confirmation_window.destroy()

    def on_no():
        result['value'] = False
        confirmation_window.destroy()

    ttk.Label(confirmation_window, text=message).pack(padx=10, pady=10)
    button_frame = ttk.Frame(confirmation_window)
    button_frame.pack(pady=5)
    ttk.Button(button_frame, text="Yes", command=on_yes).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="No", command=on_no).pack(side=tk.RIGHT, padx=5)

    center_window(confirmation_window)
    confirmation_window.grab_set()
    confirmation_window.focus_force()
    parent_window.wait_window(confirmation_window)

    return result['value']