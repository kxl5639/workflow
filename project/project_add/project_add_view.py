import tkinter as tk
from tkinter import ttk
from utils.view import center_window, create_add_or_modify_frame
from project.project_add.project_add_controller import default_entry_data
from project.project_model import field_metadata, session



def open_add_project_window():
    add_window = tk.Toplevel()
    add_window.title('Add New Project')
    
    add_window.grid_rowconfigure(0, weight=1)
    add_window.grid_columnconfigure(0, weight=1)
    add_window.resizable(height=False,width=True)
    
    add_proj_frame = create_add_or_modify_frame(add_window,field_metadata,default_entry_data(),session)
    add_proj_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    

    center_window(add_window)    

