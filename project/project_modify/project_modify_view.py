import tkinter as tk
from tkinter import ttk
from project.project_utils import create_add_modify_window

# def open_modify_project_window(project_window):    
#     from model import Project, session
#     table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    
#     selected_record = table_window_tree.selection()    
#     selected_record_id = selected_record[0] 
#     selected_record_info = session.query(Project).get(selected_record_id)
#     print(selected_record_info)
#     create_add_modify_window(project_window,'Modify Projects','Modify',selected_record=selected_record_info)

def open_modify_project_window(project_window):
    from model import Project, session
    table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree
    selected_record = table_window_tree.selection()
    if not selected_record:
        print("No record selected")
        return
    selected_record_id = selected_record[0]  # This should be the primary key (ID) of the selected record
    print(f"Selected Record ID: {selected_record_id}")  # Debug print
    selected_record_info = session.query(Project).get(int(selected_record_id))
    if selected_record_info:
        print(f"Selected Record Info: {selected_record_info}")  # Debug print
        create_add_modify_window(project_window, 'Modify Projects', 'Modify', selected_record=selected_record_info)
    else:
        print("Record not found")