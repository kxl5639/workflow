# design_eng_modify_view.py
import tkinter as tk
from tkinter import ttk
from design_eng.design_eng_model import field_metadata, session #type:ignore
from design_eng.design_eng_modify.design_eng_modify_controller import modify_design_eng_properly_selected, modify_design_eng_wrapper #type:ignore
from utils import create_add_or_modify_window #type:ignore


def open_modify_design_eng_window(tree):
    design_eng = modify_design_eng_properly_selected(tree)
    if design_eng is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Design Engineer")

    prefilled_data = {field: getattr(design_eng, field) for field in design_eng.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        session,
        window_title="Modify Design Engineer",
        prefilled_data=prefilled_data,
        button_text="Update Design Engineer",
        submit_callback=lambda entries: modify_design_eng_wrapper(entries, design_eng, modify_window, tree)
    )