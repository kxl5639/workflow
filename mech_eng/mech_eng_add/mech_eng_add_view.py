import tkinter as tk
from tkinter import ttk
from mech_eng.mech_eng_add.mech_eng_add_controller import add_mech_eng_wrapper #type:ignore
from mech_eng.mech_eng_model import field_metadata #type:ignore
from app import testing #type:ignore
from utils import create_add_or_modify_window #type:ignore

def open_add_mech_eng_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Mechanical Engineer")

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
        window_title="Add Mechanical Engineer",
        prefilled_data=prefilled_data,
        button_text="Add Mechanical Engineer",
        submit_callback=lambda entries: add_mech_eng_wrapper(entries, tree, add_window)
    )