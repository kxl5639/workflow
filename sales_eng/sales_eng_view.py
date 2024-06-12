import tkinter as tk
from tkinter import ttk
from sales_eng.sales_eng_add.sales_eng_add_view import open_add_sales_eng_window   # type: ignore
from sales_eng.sales_eng_modify.sales_eng_modify_view import open_modify_sales_eng_window # type: ignore 
from sales_eng.sales_eng_delete.sales_eng_delete_controller import delete_selected_sales_engs # type: ignore
from sales_eng.sales_eng_model import SalesEng, session # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_sales_eng_window():    

    sales_eng_window = tk.Toplevel()
    sales_eng_window.title("Sales Engineer")
 
    columns = ['first_name', 'last_name']
    sales_eng_tree = create_tree_from_db_table(sales_eng_window,columns,session,SalesEng)
    sales_eng_tree.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        sales_eng_window,
        add_command=lambda: open_add_sales_eng_window(sales_eng_tree),
        modify_command=lambda: open_modify_sales_eng_window(sales_eng_tree),
        delete_command=lambda: delete_selected_sales_engs(sales_eng_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)
  
    # Center the window after adding widgets
    center_window(sales_eng_window)

    # Bring the window to the front and set focus
    sales_eng_window.focus_force()