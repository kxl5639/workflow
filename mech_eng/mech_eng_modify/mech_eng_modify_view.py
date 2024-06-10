# mech_eng_modify_view.py
import tkinter as tk
from tkinter import ttk
from mech_eng.mech_eng_model import field_metadata #type:ignore
from mech_eng.mech_eng_modify.mech_eng_modify_controller import modify_mech_eng_properly_selected, modify_mech_eng_wrapper #type:ignore
from utils import create_add_or_modify_window #type:ignore
from app import testing

def open_modify_mech_eng_window(tree):
    mech_eng = modify_mech_eng_properly_selected(tree)
    if mech_eng is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Mechanical Engineer")

    prefilled_data = {field: getattr(mech_eng, field) for field in mech_eng.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        window_title="Modify Mechanical Engineer",
        prefilled_data=prefilled_data,
        button_text="Update Mechanical Engineer",
        submit_callback=lambda entries: modify_mech_eng_wrapper(entries, mech_eng, modify_window, tree)
    )