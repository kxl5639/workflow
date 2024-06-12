import tkinter as tk
from tkinter import ttk
from mech_eng.mech_eng_add.mech_eng_add_view import open_add_mech_eng_window   # type: ignore
from mech_eng.mech_eng_modify.mech_eng_modify_view import open_modify_mech_eng_window # type: ignore 
from mech_eng.mech_eng_delete.mech_eng_delete_controller import delete_selected_mech_engs # type: ignore
from mech_eng.mech_eng_model import MechEng, session # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_mech_eng_window():    

    mech_eng_window = tk.Toplevel()
    mech_eng_window.title("Mechanical Engineer")

    columns = ['mechanical_engineer', 'address','city','state','zip_code']
    mech_eng_tree = create_tree_from_db_table(mech_eng_window,columns,session,MechEng)
    mech_eng_tree.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
    
    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        mech_eng_window,
        add_command=lambda: open_add_mech_eng_window(mech_eng_tree),
        modify_command=lambda: open_modify_mech_eng_window(mech_eng_tree),
        delete_command=lambda: delete_selected_mech_engs(mech_eng_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)

    mech_eng_window.grid_rowconfigure(1, weight=1)
    mech_eng_window.grid_columnconfigure(0, weight=1)

    # Center the window after adding widgets
    center_window(mech_eng_window)

    # Bring the window to the front and set focus
    mech_eng_window.focus_force()