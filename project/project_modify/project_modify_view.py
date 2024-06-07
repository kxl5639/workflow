# project_modify_view.py
import tkinter as tk
from tkinter import ttk
from utils import center_window
from project.project_model import field_metadata
from project.project_modify.project_modify_controller import modify_project_properly_selected, modify_project_wrapper
from project.project_utils import create_project_window
from app import testing

def open_modify_project_window(tree):
    project = modify_project_properly_selected(tree)
    if project is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Project")

    prefilled_data = {field: getattr(project, field) for field in project.__table__.columns.keys()}

    create_project_window(
        modify_window,
        prefilled_data=prefilled_data,
        button_text="Update Project",
        submit_callback=lambda entries: modify_project_wrapper(entries, project, modify_window, tree)
    )