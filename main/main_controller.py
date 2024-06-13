import tkinter as tk
from tkinter import ttk

def create_main_button(master, button_text, button_command=None):
    button = ttk.Button(master, text=button_text, command=button_command)
    return button    
