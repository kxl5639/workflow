import tkinter as tk
from tkinter import ttk
from utils.view import center_window, create_add_or_modify_frame
from utils.controller import generate_default_entry_data
from utils.button import create_dynamic_button_frame
from project.project_model import field_metadata, session



def open_add_project_window():
    add_window = tk.Toplevel()
    add_window.title('Add New Project')
    
    add_window.grid_rowconfigure(0, weight=1)
    add_window.grid_columnconfigure(0, weight=1)
    add_window.resizable(height=False,width=True)
    
    add_proj_frame, dividing_frame = create_add_or_modify_frame(add_window,field_metadata,generate_default_entry_data(field_metadata),session)
    add_proj_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    
    # Adds an "Add Eng" button to the column of engineers
    mech_eng_frame = dividing_frame[3]
    print(mech_eng_frame)
    add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Eng', None)])
    add_mech_eng_but.grid(row=7,column=0,columnspan = 2, pady=(10,0))

    button_frame = create_dynamic_button_frame(add_window, [('Add', None),('Cancel', add_window.destroy)])
    button_frame.grid(row=1,column=0,padx=10,pady=(0,10))

    center_window(add_window)    

