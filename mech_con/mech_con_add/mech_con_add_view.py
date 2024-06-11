import tkinter as tk
from tkinter import ttk
from mech_con.mech_con_add.mech_con_add_controller import add_mech_con_wrapper #type:ignore
from mech_con.mech_con_model import field_metadata, session #type:ignore
from app import testing #type:ignore
from utils import create_add_or_modify_window #type:ignore

def open_add_mech_con_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Mechanical Contractor")

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
        session,
        window_title="Add Mechanical Contractor",
        prefilled_data=prefilled_data,
        button_text="Add Mechanical Contractor",
        submit_callback=lambda entries: add_mech_con_wrapper(entries, tree, add_window)
    )