import tkinter as tk
from tkinter import ttk
from utils import center_window, populate_treeview, columns_to_display  #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 
from project.project_add.project_add_view import open_add_project_window #type:ignore 
from project.project_modify.project_modify_view import open_modify_project_window #type:ignore 
from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
from project.project_model import Project, field_metadata, session # type: ignore

def create_project_window():
    window = tk.Toplevel()
    window.title("Projects")

    # Create the treeview
    columns = columns_to_display(field_metadata)
    tree = ttk.Treeview(window, columns=columns, show='headings')

    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    # Fetch the project data and insert it into the treeview
    populate_treeview(tree, Project, session, field_metadata)

    tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        window,
        add_command=lambda: open_add_project_window(tree),
        modify_command=lambda: open_modify_project_window(tree),
        delete_command=lambda: delete_selected_projects(tree)
    )
    button_frame.pack(pady=10)
  
    # Center the window after adding widgets
    center_window(window)

    # Bring the window to the front and set focus
    window.focus_force()

    window.mainloop()
