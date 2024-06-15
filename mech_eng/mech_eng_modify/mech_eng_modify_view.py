import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from mech_eng.mech_eng_model import field_metadata, session, MechEng
from mech_eng.mech_eng_controller import columns_to_display

def open_modify_mech_eng_window(mech_eng_window):    
    create_add_modify_window(mech_eng_window,MechEng,session,field_metadata,columns_to_display,'Modify Mechanical Engineer','Modify')
    