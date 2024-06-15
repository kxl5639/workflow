import tkinter as tk
from tkinter import ttk
from client.client_add.client_add_view import open_add_client_window #type:ignore 
from client.client_modify.client_modify_view import open_modify_client_window #type:ignore 
from client.client_delete.client_delete_controller import delete_selected_clients #type:ignore 
from client.client_model import Client, session # type: ignore
from client.client_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_client_window():
    client_window = tk.Toplevel()
    client_window.title("Design Engineers")
    client_window.grid_rowconfigure(0, weight=1)
    client_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(client_window,
                                                    columns_to_display,
                                                    session,
                                                    Client,
                                                    add_command=lambda: open_add_client_window(client_window),
                                                    modify_command=lambda: open_modify_client_window(client_window),
                                                    delete_command=lambda: delete_selected_clients(client_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(client_window)

    # Bring the window to the front and set focus
    client_window.focus_force()
    
    return client_window