import tkinter as tk
from tkinter import ttk
from utils import create_add_modify_window
from sales_eng.sales_eng_model import field_metadata, session, SalesEng
from sales_eng.sales_eng_controller import columns_to_display

def open_add_sales_eng_window(sales_eng_window):    
    create_add_modify_window(sales_eng_window,SalesEng,session,field_metadata,columns_to_display,'Add New Sales Engineers','Add')
    