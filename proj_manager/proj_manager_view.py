import tkinter as tk
from tkinter import ttk
from proj_manager.proj_manager_add.proj_manager_add_view import open_add_proj_manager_window #type:ignore 
from proj_manager.proj_manager_modify.proj_manager_modify_view import open_modify_proj_manager_window #type:ignore 
from proj_manager.proj_manager_delete.proj_manager_delete_controller import delete_selected_proj_managers #type:ignore 
from proj_manager.proj_manager_model import ProjManager, session # type: ignore
from proj_manager.proj_manager_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_proj_manager_window():
    proj_manager_window = tk.Toplevel()
    proj_manager_window.title("Design Engineers")
    proj_manager_window.grid_rowconfigure(0, weight=1)
    proj_manager_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(proj_manager_window,
                                                    columns_to_display,
                                                    session,
                                                    ProjManager,
                                                    add_command=lambda: open_add_proj_manager_window(proj_manager_window),
                                                    modify_command=lambda: open_modify_proj_manager_window(proj_manager_window),
                                                    delete_command=lambda: delete_selected_proj_managers(proj_manager_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(proj_manager_window)

    # Bring the window to the front and set focus
    proj_manager_window.focus_force()
    
    return proj_manager_window