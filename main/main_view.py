import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window #type:ignore
from main.main_controller import create_main_button
from project.project_view import create_project_window
from design_eng.design_eng_view import create_design_eng_window


def create_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")  
    main_window.grid_rowconfigure((0), weight=1)
    main_window.grid_columnconfigure((0), weight=1)    
    main_window.resizable(width=False,height=False)
    
    button_frame=ttk.Frame(main_window)
    button_frame.grid(row=0,column=0,padx=20,pady=20,sticky='nsew')
    button_frame.grid_rowconfigure((0,1), weight=1)
    button_frame.grid_columnconfigure((0), weight=1)    

    projects_button = create_main_button(button_frame, "Projects", create_project_window)
    projects_button.grid(row=0, column=0, padx=0, pady=(0,20))

    design_engs_button = create_main_button(button_frame, "Design Engineers",create_design_eng_window)
    design_engs_button.grid(row=1, column=0, padx=0, pady=0)

    # Center the window after adding widgets
    center_window(main_window)

    main_window.mainloop()
