import tkinter as tk
from tkinter import ttk
from project.project_utils import create_add_modify_window

def open_add_project_window(project_window):   
    create_add_modify_window(project_window,'Add New Projects','Add',selected_record=None)