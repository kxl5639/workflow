# sales_eng_modify_view.py
import tkinter as tk
from tkinter import ttk
from sales_eng.sales_eng_model import field_metadata, session #type:ignore
from sales_eng.sales_eng_modify.sales_eng_modify_controller import modify_sales_eng_properly_selected, modify_sales_eng_wrapper #type:ignore
from utils import create_add_or_modify_window #type:ignore

def open_modify_sales_eng_window(tree):
    sales_eng = modify_sales_eng_properly_selected(tree)
    if sales_eng is None:
        return

    modify_window = tk.Toplevel()
    modify_window.title("Modify Sales Engineer")

    prefilled_data = {field: getattr(sales_eng, field) for field in sales_eng.__table__.columns.keys()}

    create_add_or_modify_window(
        modify_window,
        field_metadata,
        session,
        window_title="Modify Sales Engineer",
        prefilled_data=prefilled_data,
        button_text="Update Sales Engineer",
        submit_callback=lambda entries: modify_sales_eng_wrapper(entries, sales_eng, modify_window, tree)
    )