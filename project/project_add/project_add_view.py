import tkinter as tk
from tkinter import ttk
from utils import center_window, create_add_or_modify_frame, create_dynamic_button_frame
from project.project_model import field_metadata, session

def open_add_project_window(project_window):
    add_window = tk.Toplevel()
    add_window.title('Add New Project')    
    add_window.grid_rowconfigure(0, weight=1)
    add_window.grid_columnconfigure(0, weight=1)
    add_window.resizable(height=False,width=True)

    project_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    

    add_proj_frame, project_entries, dividing_frame, max_rows_in_dividing_frames = create_add_or_modify_frame(add_window,
                                                                                                              field_metadata,
                                                                                                              session,
                                                                                                              True)
    add_proj_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    


    
    # Adds an "Add Eng" button to the column of engineers
    mech_eng_frame = dividing_frame[3] # [3] represents the column that the mechanical engineer info is in
    butt_row = max_rows_in_dividing_frames[3]+1    
    add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Engineer', None)])
    add_mech_eng_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    # Adds an "Add Eng" button to the column of engineers
    mech_con_frame = dividing_frame[4]
    butt_row = max_rows_in_dividing_frames[4]+1    
    add_mech_con_but = create_dynamic_button_frame(mech_con_frame,[('Add Contractor', None)])
    add_mech_con_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    button_frame = create_dynamic_button_frame(add_window, [('Add', None),('Cancel', add_window.destroy)])
    button_frame.grid(row=1,column=0,padx=10,pady=(0,10))

    
    


    center_window(add_window)    

