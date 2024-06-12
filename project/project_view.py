import tkinter as tk
from tkinter import ttk
from project.project_add.project_add_view import open_add_project_window #type:ignore 
from project.project_modify.project_modify_view import open_modify_project_window #type:ignore 
from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
from project.project_model import Project, session # type: ignore
from project.project_controller import columns_to_display # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_project_window():

    project_window = tk.Toplevel()
    project_window.title("Projects")

    project_tree = create_tree_from_db_table(project_window,columns_to_display,session,Project)
    project_tree.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        project_window,
        add_command=lambda: open_add_project_window(project_tree),
        modify_command=lambda: open_modify_project_window(project_tree),
        delete_command=lambda: delete_selected_projects(project_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)

    project_window.grid_rowconfigure(1, weight=1)
    project_window.grid_columnconfigure(0, weight=1)

    # Center the window after adding widgets
    center_window(project_window)

    # Bring the window to the front and set focus
    project_window.focus_force()