import tkinter as tk
from tkinter import ttk
from project_manager.project_manager_add.project_manager_add_controller import add_project_manager_wrapper #type:ignore
from project_manager.project_manager_model import field_metadata #type:ignore
from app import testing #type:ignore
from utils import create_add_or_modify_window #type:ignore

def open_add_project_manager_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Project Manager")

    prefilled_data = {}
    if testing:
        for field in field_metadata.keys():
            prefilled_data[field] = "TESTING"
    else:
        for field in field_metadata.keys():
            prefilled_data[field] = field_metadata[field]["default"]

    create_add_or_modify_window(
        add_window,
        field_metadata,
        window_title="Add Project Manager",
        prefilled_data=prefilled_data,
        button_text="Add Project Manager",
        submit_callback=lambda entries: add_project_manager_wrapper(entries, tree, add_window)
    )