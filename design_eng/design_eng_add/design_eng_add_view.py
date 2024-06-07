import tkinter as tk
from tkinter import ttk
from utils import center_window
from design_eng.design_eng_add.design_eng_add_controller import add_design_eng_wrapper
from design_eng.design_eng_model import field_metadata
from app import testing
from design_eng.design_eng_utils import create_design_eng_window

def open_add_design_eng_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add design_eng")

    prefilled_data = {}
    if testing:
        for field in field_metadata.keys():
            prefilled_data[field] = "TESTING"
    else:
        for field in field_metadata.keys():
            prefilled_data[field] = field_metadata[field]["default"]

    create_design_eng_window(
        add_window,
        prefilled_data=prefilled_data,
        button_text="Add Design Engineer",
        submit_callback=lambda entries: add_design_eng_wrapper(entries, tree, add_window)
    )