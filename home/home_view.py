import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window

def create_home_window(controller):
    window = tk.Tk()
    window.title("Home Window")

    # Create a frame to hold the buttons
    frame = ttk.Frame(window, padding="10 10 10 10")
    frame.grid(row=0, column=0, padx=10, pady=10)

    projects_button = ttk.Button(frame, text="Projects", command=controller['projects_button_clicked'])
    projects_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    design_engineers_button = ttk.Button(frame, text="Design Engineers", command=controller['design_engineers_button_clicked'])
    design_engineers_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    sales_engineers_button = ttk.Button(frame, text="Sales Engineers", command=controller['sales_engineers_button_clicked'])
    sales_engineers_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    project_managers_button = ttk.Button(frame, text="Project Managers", command=controller['project_managers_button_clicked'])
    project_managers_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    # Make the buttons expand to fill the available space
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    # Center the window after adding widgets
    center_window(window)

    window.mainloop()
