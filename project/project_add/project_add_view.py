import tkinter as tk
from tkinter import ttk
from utils import center_window
from project.project_add.project_add_controller import add_project_wrapper
from project.project_model import field_metadata
from app import testing
from project.project_utils import create_project_window





def open_add_project_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Project")

    prefilled_data = {}
    if testing:
        for field in field_metadata.keys():
            if field == "submittal_date":
                prefilled_data[field] = "XX/XX/XX"
            else:
                prefilled_data[field] = "TESTING"
    else:
        for field in field_metadata.keys():
            prefilled_data[field] = field_metadata[field]["default"]

    create_project_window(
        add_window,
        prefilled_data=prefilled_data,
        button_text="Add Project",
        submit_callback=lambda entries: add_project_wrapper(entries, tree, add_window)
    )