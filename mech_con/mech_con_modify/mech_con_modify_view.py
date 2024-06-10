# mech_con_modify_view.py
import tkinter as tk
from tkinter import ttk
from mech_con.mech_con_model import field_metadata #type:ignore
from mech_con.mech_con_modify.mech_con_modify_controller import modify_mech_con_properly_selected, modify_mech_con_wrapper #type:ignore
from utils import create_add_or_modify_window #type:ignore
from app import testing

def open_modify_mech_con_window(tree):
    mech_con = modify_mech_con_properly_selected(tree)
    if mech_con is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Mechanical Contractor")

    prefilled_data = {field: getattr(mech_con, field) for field in mech_con.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        window_title="Modify Mechanical Contractor",
        prefilled_data=prefilled_data,
        button_text="Update Mechanical Contractor",
        submit_callback=lambda entries: modify_mech_con_wrapper(entries, mech_con, modify_window, tree)
    )