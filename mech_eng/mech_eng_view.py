import tkinter as tk
from tkinter import ttk
from mech_eng.mech_eng_add.mech_eng_add_view import open_add_mech_eng_window #type:ignore 
from mech_eng.mech_eng_modify.mech_eng_modify_view import open_modify_mech_eng_window #type:ignore 
from mech_eng.mech_eng_delete.mech_eng_delete_controller import delete_selected_mech_engs #type:ignore 
from mech_eng.mech_eng_model import MechEng, session # type: ignore
from mech_eng.mech_eng_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_mech_eng_window():
    mech_eng_window = tk.Toplevel()
    mech_eng_window.title("Design Engineers")
    mech_eng_window.grid_rowconfigure(0, weight=1)
    mech_eng_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(mech_eng_window,
                                                    columns_to_display,
                                                    session,
                                                    MechEng,
                                                    add_command=lambda: open_add_mech_eng_window(mech_eng_window),
                                                    modify_command=lambda: open_modify_mech_eng_window(mech_eng_window),
                                                    delete_command=lambda: delete_selected_mech_engs(mech_eng_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(mech_eng_window)

    # Bring the window to the front and set focus
    mech_eng_window.focus_force()
    
    return mech_eng_window