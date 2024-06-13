import tkinter as tk
from tkinter import ttk, messagebox
from utils.view import center_window #type:ignore
from main.main_controller import create_main_button
from project.project_view import create_project_window


def create_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")

    # Set up main window
    main_window.grid_rowconfigure((0,1,2), weight=1)
    main_window.grid_columnconfigure((0,1), weight=1)    
    
    projects_button = create_main_button(main_window, "Projects", create_project_window)
    projects_button.grid(row=0, column=0, padx=10, pady=(10,5), sticky="ew")

    design_engs_button = create_main_button(main_window, "Design Engineers")
    design_engs_button.grid(row=1, column=0, padx=10, pady=(5,10), sticky="ew")

    # Center the window after adding widgets
    center_window(main_window)

    main_window.mainloop()
