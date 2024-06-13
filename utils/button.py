import tkinter as tk
from tkinter import ttk

def create_addmodifydelete_button_frame(master, add_command=None, modify_command=None, delete_command=None):
    button_frame = ttk.Frame(master)
    button_frame.grid_rowconfigure((0), weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    gen_pad = 10

    add_button = ttk.Button(button_frame, text="Add", command=add_command)
    add_button.grid(row=0, column=0, padx=(0,0), pady=0)
    #add_button.grid(row=0, column=0, padx=(0,0), pady=0, sticky="nsew")

    modify_button = ttk.Button(button_frame, text="Modify", command=modify_command)
    modify_button.grid(row=0, column=1, padx=(gen_pad,gen_pad), pady=0)
    #modify_button.grid(row=0, column=1, padx=(gen_pad,gen_pad), pady=0, sticky="nsew")

    delete_button = ttk.Button(button_frame, text="Delete", command=delete_command)
    delete_button.grid(row=0, column=2, padx=0, pady=0)
    #delete_button.grid(row=0, column=2, padx=0, pady=0,stick="nsew")
    
    return button_frame
