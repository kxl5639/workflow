import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from proj_manager.proj_manager_model import field_metadata, session, ProjManager
from proj_manager.proj_manager_controller import columns_to_display

def open_modify_proj_manager_window(proj_manager_window):    
    create_add_modify_window(proj_manager_window,ProjManager,session,field_metadata,columns_to_display,'Modify Project Manager','Modify')
    