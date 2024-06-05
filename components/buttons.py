import tkinter as tk
from tkinter import ttk

def create_addmodifydelete_buttons(parent, add_command=None, modify_command=None, delete_command=None):
    button_frame = ttk.Frame(parent)
    
    add_button = ttk.Button(button_frame, text="Add", command=add_command)
    add_button.grid(row=0, column=0, padx=5)

    modify_button = ttk.Button(button_frame, text="Modify", command=modify_command)
    modify_button.grid(row=0, column=1, padx=5)

    delete_button = ttk.Button(button_frame, text="Delete", command=delete_command)
    delete_button.grid(row=0, column=2, padx=5)
    
    return button_frame
