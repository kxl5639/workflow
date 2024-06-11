# project_manager_modify_view.py
import tkinter as tk
from tkinter import ttk
from project_manager.project_manager_model import field_metadata, session #type:ignore
from project_manager.project_manager_modify.project_manager_modify_controller import modify_project_manager_properly_selected, modify_project_manager_wrapper #type:ignore
from utils import create_add_or_modify_window #type:ignore

def open_modify_project_manager_window(tree):
    project_manager = modify_project_manager_properly_selected(tree)
    if project_manager is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Project Manager Engineer")

    prefilled_data = {field: getattr(project_manager, field) for field in project_manager.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        session,
        window_title="Modify Project Manager Engineer",
        prefilled_data=prefilled_data,
        button_text="Update Project Manager",
        submit_callback=lambda entries: modify_project_manager_wrapper(entries, project_manager, modify_window, tree)
    )