import tkinter as tk
from tkinter import ttk
from project.project_add.project_add_view import open_add_project_window #type:ignore 
from project.project_modify.project_modify_view import open_modify_project_window #type:ignore 
from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
from project.project_model import Project, session # type: ignore
from project.project_controller import columns_to_display # type: ignore
from utils.view import center_window, create_tree_and_addmoddel_buttons_frame #type:ignore 

def create_project_window():
    project_window = tk.Toplevel()
    project_window.title("Projects")
    project_window.grid_rowconfigure(0, weight=1)
    project_window.grid_columnconfigure(0, weight=1)

    # tree_frame = ttk.Frame(project_window)
    # tree_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    # tree_frame.grid_rowconfigure(0, weight=1)
    # tree_frame.grid_columnconfigure(0, weight=1)   
    
    tree_but_frame = create_tree_and_addmoddel_buttons_frame(project_window, columns_to_display, session, Project, add_command=None, modify_command=None, delete_command=None )
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")
    # tree_but_frame.grid_rowconfigure(0, weight=1)
    # tree_but_frame.grid_columnconfigure(0, weight=1)
    

    # Center the window after adding widgets
    center_window(project_window)

    # Bring the window to the front and set focus
    project_window.focus_force()