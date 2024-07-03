import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window, create_button_frame
from project.project_view import create_project_window
from view import CRUDWindow
from title_controller import TitleController

def create_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")  
    main_window.grid_rowconfigure((0), weight=1)
    main_window.grid_columnconfigure((0), weight=1)    
    main_window.resizable(width=False,height=False)
    from projectlistwindow_controller import ProjectListWindowController
    
    button_frame=ttk.Frame(main_window)
    button_frame.grid(row=0, column=0, padx=10, pady=10)
    # button_frame.grid_rowconfigure((0,1,2), weight=1)
    # button_frame.grid_columnconfigure((0), weight=1)    

    # projects_button = create_button_frame(button_frame, [("Projects", create_project_window)])
    projects_button = create_button_frame(button_frame, [("Projects", lambda: ProjectListWindowController(main_window))])
    projects_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def open_crud_window(table_name):
        '''Takes the table name arg to generate treeview'''
        CRUDWindow(main_window, table_name)
        
    design_engs_button = create_button_frame(button_frame, [("Design Engineers", lambda:open_crud_window('designengineers'))])
    design_engs_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    sales_engs_button = create_button_frame(button_frame, [("Sales Engineers", lambda:open_crud_window('salesengineers'))])
    sales_engs_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    proj_managers_button = create_button_frame(button_frame, [("Project Managers", lambda:open_crud_window('projectmanagers'))])
    proj_managers_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    client_button = create_button_frame(button_frame, [("Clients", lambda:open_crud_window('clients'))])
    client_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    mech_cons_button = create_button_frame(button_frame, [("Mechanical Contractors", lambda:open_crud_window('mechanicalcontractors'))])
    mech_cons_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    mech_engs_button = create_button_frame(button_frame, [("Mechanical Engineers", lambda:open_crud_window('mechanicalengineers'))])
    mech_engs_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    # dwgtitles_button = create_button_frame(button_frame, [("Title Manager", lambda:open_title_manager_window())])
    dwgtitles_button = create_button_frame(button_frame, [("Title Manager", lambda:TitleController(parent=main_window))])
    dwgtitles_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    

    # Center the window after adding widgets
    center_window(main_window)

    main_window.mainloop()
