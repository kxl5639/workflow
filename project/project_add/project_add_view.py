import tkinter as tk
from tkinter import ttk
from project.project_add.project_add_controller import add_project_wrapper #type:ignore
from project.project_model import field_metadata #type:ignore
from configs import testing #type:ignore
from utils import create_add_or_modify_window #type:ignore
#from design_eng.design_eng_model import session, DesignEng # type: ignore

def open_add_project_window(tree):
    add_window = tk.Toplevel()    

    prefilled_data = {}
    if testing:
        for field in field_metadata.keys():
            if field == "submittal_date":
                prefilled_data[field] = "XX/XX/XX"
            elif field == "design_engineer":
                prefilled_data[field] = "Kevin Lee"
            else:
                prefilled_data[field] = "TESTING"
    else:
        for field in field_metadata.keys():
            prefilled_data[field] = field_metadata[field]["default"]

    create_add_or_modify_window(
        add_window,        
        field_metadata,
        window_title="Add Project",
        prefilled_data=prefilled_data,
        button_text="Add Project",
        submit_callback=lambda entries: add_project_wrapper(entries, tree, add_window)        
    )