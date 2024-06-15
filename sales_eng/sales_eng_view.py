import tkinter as tk
from tkinter import ttk
from sales_eng.sales_eng_add.sales_eng_add_view import open_add_sales_eng_window #type:ignore 
from sales_eng.sales_eng_modify.sales_eng_modify_view import open_modify_sales_eng_window #type:ignore 
from sales_eng.sales_eng_delete.sales_eng_delete_controller import delete_selected_sales_engs #type:ignore 
from sales_eng.sales_eng_model import SalesEng, session # type: ignore
from sales_eng.sales_eng_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_sales_eng_window():
    sales_eng_window = tk.Toplevel()
    sales_eng_window.title("Sales Engineers")
    sales_eng_window.grid_rowconfigure(0, weight=1)
    sales_eng_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(sales_eng_window,
                                                    columns_to_display,
                                                    session,
                                                    SalesEng,
                                                    add_command=lambda: open_add_sales_eng_window(sales_eng_window),
                                                    modify_command=lambda: open_modify_sales_eng_window(sales_eng_window),
                                                    delete_command=lambda: delete_selected_sales_engs(sales_eng_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(sales_eng_window)

    # Bring the window to the front and set focus
    sales_eng_window.focus_force()
    
    return sales_eng_window