import tkinter as tk
from tkinter import ttk
from mech_con.mech_con_add.mech_con_add_view import open_add_mech_con_window #type:ignore 
from mech_con.mech_con_modify.mech_con_modify_view import open_modify_mech_con_window #type:ignore 
from mech_con.mech_con_delete.mech_con_delete_controller import delete_selected_mech_cons #type:ignore 
from mech_con.mech_con_model import MechCon, session # type: ignore
from mech_con.mech_con_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_mech_con_window():
    mech_con_window = tk.Toplevel()
    mech_con_window.title("Design Engineers")
    mech_con_window.grid_rowconfigure(0, weight=1)
    mech_con_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(mech_con_window,
                                                    columns_to_display,
                                                    session,
                                                    MechCon,
                                                    add_command=lambda: open_add_mech_con_window(mech_con_window),
                                                    modify_command=lambda: open_modify_mech_con_window(mech_con_window),
                                                    delete_command=lambda: delete_selected_mech_cons(mech_con_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(mech_con_window)

    # Bring the window to the front and set focus
    mech_con_window.focus_force()
    
    return mech_con_window