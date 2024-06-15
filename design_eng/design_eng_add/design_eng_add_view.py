import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from design_eng.design_eng_model import field_metadata, session, DesignEng
from design_eng.design_eng_controller import columns_to_display

def open_add_design_eng_window(design_eng_window):    
    create_add_modify_window(design_eng_window,DesignEng,session,field_metadata,columns_to_display,'Add New Design Engineers','Add')
    