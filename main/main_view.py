import tkinter as tk
from tkinter import ttk
# from utils import create_button_frame
# from project.project_view import create_project_window
from class_collection import BaseWindow, ButtonsFrame
from title.title_controller import TitleController
from project_list.projectlistwindow_controller import ProjectListWindowController


def create_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")  
    main_window.grid_rowconfigure((0), weight=1)
    main_window.grid_columnconfigure((0), weight=1)    
    main_window.resizable(width=False,height=False)
    
    button_frame=ttk.Frame(main_window)
    button_frame.grid(row=0, column=0, padx=10, pady=10)

    projects_button = ButtonsFrame(button_frame, [("Projects", lambda: ProjectListWindowController(main_window))])
    projects_button.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # def open_crud_window(table_name):
    #     '''Takes the table name arg to generate treeview'''
    #     CRUDWindow(main_window, table_name)

    design_engs_button = ButtonsFrame(button_frame, [("Design Engineers", lambda:None)])
    design_engs_button.button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    sales_engs_button = ButtonsFrame(button_frame, [("Sales Engineers", lambda:None)])
    sales_engs_button.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    proj_managers_button = ButtonsFrame(button_frame, [("Project Managers", lambda:None)])
    proj_managers_button.button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    client_button = ButtonsFrame(button_frame, [("Clients", lambda:None)])
    client_button.button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    mech_cons_button = ButtonsFrame(button_frame, [("Mechanical Contractors", lambda:None)])
    mech_cons_button.button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    mech_engs_button = ButtonsFrame(button_frame, [("Mechanical Engineers", lambda:None)])
    mech_engs_button.button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    dwgtitles_button = ButtonsFrame(button_frame, [("Title Manager", lambda:TitleController(parent=main_window))])
    dwgtitles_button.button_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    

    # Center the window after adding widgets
    BaseWindow.center_window(main_window)

    main_window.mainloop()
