# design_eng_modify_view.py
import tkinter as tk
from tkinter import ttk
from utils import center_window
from design_eng.design_eng_model import field_metadata
from design_eng.design_eng_modify.design_eng_modify_controller import modify_design_eng_properly_selected, modify_design_eng_wrapper
from design_eng.design_eng_utils import create_design_eng_window
from app import testing

def open_modify_design_eng_window(tree):
    design_eng = modify_design_eng_properly_selected(tree)
    if design_eng is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Design Engineer")

    prefilled_data = {field: getattr(design_eng, field) for field in design_eng.__table__.columns.keys()}

    create_design_eng_window(
        modify_window,
        prefilled_data=prefilled_data,
        button_text="Update Design Engineer",
        submit_callback=lambda entries: modify_design_eng_wrapper(entries, design_eng, modify_window, tree)
    )