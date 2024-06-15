import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from mech_con.mech_con_model import field_metadata, session, MechCon
from mech_con.mech_con_controller import columns_to_display

def open_add_mech_con_window(mech_con_window):    
    create_add_modify_window(mech_con_window,MechCon,session,field_metadata,columns_to_display,'Add New Mechanical Contractor','Add')
    