import tkinter as tk
from tkinter import ttk
from project.project_add.project_add_view import open_add_project_window
# from project.project_modify.project_modify_view import open_modify_project_window
# from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
from project.project_controller import column_map, table_data # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_project_window():
    project_window = tk.Toplevel()
    project_window.title("Projects")
    project_window.grid_rowconfigure(0, weight=1)
    project_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(project_window,
                                                    table_data,
                                                    column_map,                                                    
                                                    #add_command=None,
                                                    add_command=lambda: open_add_project_window(project_window),
                                                    modify_command=None,
                                                    delete_command=None)                                                    
                                                    # modify_command=lambda: open_modify_project_window(project_window),
                                                    # delete_command=lambda: delete_selected_projects(project_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(project_window)

    # Bring the window to the front and set focus
    project_window.focus_force()
    
    return project_window