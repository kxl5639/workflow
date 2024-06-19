import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy.orm import Session
from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
from utils import center_window
from project.project_utils import create_add_or_modify_frame
# Function to add project

def add_project():
  
    # project_number_entry = 
    # em_type_entry = 
    # job_phase_entry = 
    # submit_date_entry = 
    # projectmanager_entry = 
    # designengineer_entry = 
    # salesengineer_entry = 
    # client_entry = 
    # client_scope = 
    # client_address = 
    # client_city = 
    # client_state = 
    # client_zip_code = 
    # mecheng_name = 
    # mecheng_address = 
    # mecheng_city = 
    # mecheng_state = 
    # mecheng_zip_code = 
    # mechcon_name = 
    # mechcon_address = 
    # mechcon_city = 
    # mechcon_state = 
    # mechcon_zip_code = 
    # mechcon_phone = 



    pass

def extract_entry_widgets(parent, entry_widgets=None):
    if entry_widgets is None:
        entry_widgets = []
    
    for widget in parent.winfo_children():
        if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Entry):
            entry_widgets.append(widget)
        elif isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
            extract_entry_widgets(widget, entry_widgets)
    
    return entry_widgets



#region Create labels and entry boxes
# Create the main window
add_mod_window = tk.Tk()
add_mod_window.title("Add Project")
add_mod_window.grid_rowconfigure(0, weight=1)
add_mod_window.grid_columnconfigure(0, weight=1)
add_mod_window.resizable(height=False,width=True)

frame = create_add_or_modify_frame(add_mod_window)


# # Create submit button
# submit_button = tk.Button(add_mod_window, text="Add Project", command=add_project)
# submit_button.grid(row=10, columnspan=2)

center_window(add_mod_window)
# Start the main loop
add_mod_window.mainloop()






