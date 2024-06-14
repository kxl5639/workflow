import tkinter as tk
from tkinter import ttk

def create_two_button_frame(master,button_text):

    button_frame = ttk.Frame(master)
    button_frame.grid_rowconfigure((0), weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)   

    submit_button = ttk.Button(button_frame, text=button_text, command=lambda: submit_callback(entries))
    submit_button.grid(row=0, column=0, padx=(0,10), pady=0)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=master.destroy)
    cancel_button.grid(row=0, column=1, padx=0, pady=0)    

    return button_frame







def create_dynamic_button_frame(master, button_info):
    # """
    # Create a frame with dynamically generated buttons.

    # Parameters:
    # - master: The parent widget.
    # - button_info: A list of tuples, each containing the button label and command.
    #               Example: [("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)]
    # """
    button_frame = ttk.Frame(master)
    
    gen_pad = 5
    # Configure grid layout
    button_frame.grid_rowconfigure(0, weight=1)
    for i in range(len(button_info)):
        button_frame.grid_columnconfigure(i, weight=1)
    
    # Create buttons based on button_info
    for index, (label, command) in enumerate(button_info):
        button = ttk.Button(button_frame, text=label, command=command)
        button.grid(row=0, column=index, padx=(gen_pad if index != 0 else 0, gen_pad if index != len(button_info) - 1 else 0), pady=0, sticky="nsew")
    
    return button_frame