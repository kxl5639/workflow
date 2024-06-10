import tkinter as tk
from tkinter import ttk
from components.buttons import create_addmodifydelete_buttons # type: ignore
from utils import create_table_window #type:ignore 
from sales_eng.sales_eng_add.sales_eng_add_view import open_add_sales_eng_window   # type: ignore
from sales_eng.sales_eng_modify.sales_eng_modify_view import open_modify_sales_eng_window # type: ignore 
from sales_eng.sales_eng_delete.sales_eng_delete_controller import delete_selected_sales_engs # type: ignore
from sales_eng.sales_eng_model import SalesEng, field_metadata, session # type: ignore

def create_sales_eng_window():    
    create_table_window(
        window_title="Sales Engineers",
        table=SalesEng,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_sales_eng_window,
        modify_command=open_modify_sales_eng_window,
        delete_command=delete_selected_sales_engs
    )
