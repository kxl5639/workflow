import tkinter as tk
from tkinter import ttk
from design_eng.design_eng_add.design_eng_add_view import open_add_design_eng_window   # type: ignore
from design_eng.design_eng_modify.design_eng_modify_view import open_modify_design_eng_window # type: ignore 
from design_eng.design_eng_delete.design_eng_delete_controller import delete_selected_design_engs # type: ignore
from design_eng.design_eng_model import DesignEng, session # type: ignore
from utils import create_tree_from_db_table, center_window #type:ignore 
from components.buttons import create_addmodifydelete_buttons #type:ignore 

def create_design_eng_window():    

    design_eng_window = tk.Toplevel()
    design_eng_window.title("Design Engineer")

    columns = ['first_name', 'last_name']
    design_eng_tree = create_tree_from_db_table(design_eng_window,columns,session,DesignEng)
    design_eng_tree.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        design_eng_window,
        add_command=lambda: open_add_design_eng_window(design_eng_tree),
        modify_command=lambda: open_modify_design_eng_window(design_eng_tree),
        delete_command=lambda: delete_selected_design_engs(design_eng_tree)
    )
    button_frame.grid(row=1, column=0, pady=10, padx=10)

    design_eng_window.grid_rowconfigure(1, weight=1)
    design_eng_window.grid_columnconfigure(0, weight=1)

    # Center the window after adding widgets
    center_window(design_eng_window)

    # Bring the window to the front and set focus
    design_eng_window.focus_force()