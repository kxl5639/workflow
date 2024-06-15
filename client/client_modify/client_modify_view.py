import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from client.client_model import field_metadata, session, Client
from client.client_controller import columns_to_display

def open_modify_client_window(client_window):    
    create_add_modify_window(client_window,Client,session,field_metadata,columns_to_display,'Modify Client','Modify')
    