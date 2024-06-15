import tkinter as tk
from tkinter import ttk
from design_eng.design_eng_add.design_eng_add_view import open_add_design_eng_window #type:ignore 
from design_eng.design_eng_modify.design_eng_modify_view import open_modify_design_eng_window #type:ignore 
from design_eng.design_eng_delete.design_eng_delete_controller import delete_selected_design_engs #type:ignore 
from design_eng.design_eng_model import DesignEng, session # type: ignore
from design_eng.design_eng_controller import columns_to_display # type: ignore
from utils import center_window, create_standard_tree_but_frame #type:ignore 

def create_design_eng_window():
    design_eng_window = tk.Toplevel()
    design_eng_window.title("Design Engineers")
    design_eng_window.grid_rowconfigure(0, weight=1)
    design_eng_window.grid_columnconfigure(0, weight=1)
   
    tree_but_frame = create_standard_tree_but_frame(design_eng_window,
                                                    columns_to_display,
                                                    session,
                                                    DesignEng,
                                                    add_command=lambda: open_add_design_eng_window(design_eng_window),
                                                    modify_command=lambda: open_modify_design_eng_window(design_eng_window),
                                                    delete_command=lambda: delete_selected_design_engs(design_eng_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    center_window(design_eng_window)

    # Bring the window to the front and set focus
    design_eng_window.focus_force()
    
    return design_eng_window