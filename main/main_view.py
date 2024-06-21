import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window #type:ignore
from project.project_view import create_project_window

def create_main_button(master, button_text, button_command=None):
    button = ttk.Button(master, text=button_text, command=button_command)
    return button    

def create_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")  
    main_window.grid_rowconfigure((0), weight=1)
    main_window.grid_columnconfigure((0), weight=1)    
    main_window.resizable(width=False,height=False)
    
    button_frame=ttk.Frame(main_window)
    button_frame.grid(row=0, column=0, padx=10, pady=10)
    # button_frame.grid_rowconfigure((0,1,2), weight=1)
    # button_frame.grid_columnconfigure((0), weight=1)    

    projects_button = create_main_button(button_frame, "Projects", create_project_window)
    projects_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # design_engs_button = create_main_button(button_frame, "Design Engineers",create_design_eng_window)
    # design_engs_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # sales_engs_button = create_main_button(button_frame, "Sales Engineers",create_sales_eng_window)
    # sales_engs_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # proj_managers_button = create_main_button(button_frame, "Project Managers",create_proj_manager_window)
    # proj_managers_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    # client_button = create_main_button(button_frame, "Clients",create_client_window)
    # client_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # mech_cons_button = create_main_button(button_frame, "Mechanical Contractors",create_mech_con_window)
    # mech_cons_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # mech_engs_button = create_main_button(button_frame, "Mechanical Engineers",create_mech_eng_window)
    # mech_engs_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    

    # Center the window after adding widgets
    center_window(main_window)

    main_window.mainloop()
