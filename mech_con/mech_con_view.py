import tkinter as tk
from tkinter import ttk
from mech_con.mech_con_add.mech_con_add_view import open_add_mech_con_window   # type: ignore
from mech_con.mech_con_modify.mech_con_modify_view import open_modify_mech_con_window # type: ignore 
from mech_con.mech_con_delete.mech_con_delete_controller import delete_selected_mech_cons # type: ignore
from mech_con.mech_con_model import MechCon, session # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_mech_con_window():    

    mech_con_window = tk.Toplevel()
    mech_con_window.title("Mechanical Contractor")

    tree_frame = ttk.Frame(mech_con_window)
    tree_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    
    columns = ['mechanical_contractor', 'address','city','state','zip_code','phone_number']
    mech_con_tree = create_tree_from_db_table(tree_frame,columns,session,MechCon)
    mech_con_tree.grid(row=0, column=0, pady=0, padx=0)
    
    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        mech_con_window,
        add_command=lambda: open_add_mech_con_window(mech_con_tree),
        modify_command=lambda: open_modify_mech_con_window(mech_con_tree),
        delete_command=lambda: delete_selected_mech_cons(mech_con_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)
  
    mech_con_window.grid_rowconfigure(1, weight=1)
    mech_con_window.grid_columnconfigure(0, weight=1)

    # Center the window after adding widgets
    center_window(mech_con_window)

    # Bring the window to the front and set focus
    mech_con_window.focus_force()