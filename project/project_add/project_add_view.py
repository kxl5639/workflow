import tkinter as tk
from tkinter import ttk
from utils import open_add_modify_window
from project.project_model import field_metadata, session, Project
from project.project_controller import columns_to_display

def open_add_project_window(project_window):    

    open_add_modify_window(project_window,Project,session,field_metadata,columns_to_display,'Add New Projects','Addio')
    # add_window = tk.Toplevel()
    # add_window.title('Add New Project')    
    # add_window.grid_rowconfigure(0, weight=1)
    # add_window.grid_columnconfigure(0, weight=1)
    # add_window.resizable(height=False,width=True)

    # #Tree created from the parent window, need it so that we can pass it to the buttons to refresh the tree when we add/modify data the table
    # project_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    

    # add_proj_frame, project_entries, dividing_frame, max_rows_in_dividing_frames = create_add_or_modify_frame(add_window,
    #                                                                                                             field_metadata,
    #                                                                                                             session,
    #                                                                                                             True)
    # add_proj_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    
    
    # # Adds an "Add Eng" button to the column of engineers
    # mech_eng_frame = dividing_frame[3] # [3] represents the column that the mechanical engineer info is in
    # butt_row = max_rows_in_dividing_frames[3]+1    
    # add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Engineer', None)])
    # add_mech_eng_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    # # Adds an "Add Eng" button to the column of engineers
    # mech_con_frame = dividing_frame[4]
    # butt_row = max_rows_in_dividing_frames[4]+1    
    # add_mech_con_but = create_dynamic_button_frame(mech_con_frame,[('Add Contractor', None)])
    # add_mech_con_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))
    
    # button_frame = create_dynamic_button_frame(add_window, [('Add', lambda:add_proj_button_cmd()),
    #                                                         ('Cancel', add_window.destroy)])
    # button_frame.grid(row=1,column=0,padx=10,pady=(0,10))
   
    # def add_proj_button_cmd():        
    #     formatted_entries, error_message=prep_data_entry(add_window,project_entries)
    #     if error_message:
    #         return
    #     update_table(Project,session,formatted_entries)
    #     refresh_table(project_window_tree, Project, session,columns_to_display)
    #     add_window.destroy()     


    # center_window(add_window) 
    # add_window.grab_set()     
    # add_window.focus_force()  
    # project_window.wait_window(add_window)
