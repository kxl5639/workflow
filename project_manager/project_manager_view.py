import tkinter as tk
from tkinter import ttk
from project_manager.project_manager_add.project_manager_add_view import open_add_project_manager_window   # type: ignore
from project_manager.project_manager_modify.project_manager_modify_view import open_modify_project_manager_window # type: ignore 
from project_manager.project_manager_delete.project_manager_delete_controller import delete_selected_project_managers # type: ignore
from project_manager.project_manager_model import ProjectManager, session # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_project_manager_window():    

    project_manager_window = tk.Toplevel()
    project_manager_window.title("Project Manager")

    tree_frame = ttk.Frame(project_manager_window)
    tree_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    columns = ['first_name', 'last_name']
    project_manager_tree = create_tree_from_db_table(project_manager_window,columns,session,ProjectManager)
    project_manager_tree.grid(row=0, column=0, pady=0, padx=0)

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        project_manager_window,
        add_command=lambda: open_add_project_manager_window(project_manager_tree),
        modify_command=lambda: open_modify_project_manager_window(project_manager_tree),
        delete_command=lambda: delete_selected_project_managers(project_manager_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)

    project_manager_window.grid_rowconfigure(1, weight=1)
    project_manager_window.grid_columnconfigure(0, weight=1)

    # Center the window after adding widgets
    center_window(project_manager_window)

    # Bring the window to the front and set focus
    project_manager_window.focus_force()