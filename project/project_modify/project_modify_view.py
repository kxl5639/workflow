# project_modify_view.py
import tkinter as tk
from tkinter import ttk
from project.project_model import field_metadata, session #type:ignore
from project.project_modify.project_modify_controller import modify_project_properly_selected, modify_project_wrapper # type: ignore
from utils.view import create_add_or_modify_window # type: ignore

def open_modify_project_window(tree):
    project = modify_project_properly_selected(tree)
    if project is None:
        return

    modify_window = tk.Toplevel()    

    prefilled_data = {field: getattr(project, field) for field in project.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        session,
        window_title="Modify Project",
        prefilled_data=prefilled_data,
        button_text="Update Project",
        submit_callback=lambda entries: modify_project_wrapper(entries, project, modify_window, tree)        
    )