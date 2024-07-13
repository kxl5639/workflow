import tkinter as tk
from tkinter import ttk
from class_collection import BaseWindow, ButtonsFrame
from title.title_controller import TitleController
from project_list.projectlistwindow_controller import ProjectListWindowController
from configs import testing

class MainWindow(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)

        self.root.grid_rowconfigure((0), weight=1)
        self.root.grid_columnconfigure((0), weight=1)    
        self.root.resizable(width=False,height=False)
        self.root.bind("<Key>", lambda event: on_keypress(event, self.root))
        def on_keypress(event, window):
            if event.char == 'q':
                window.destroy()

        button_frame=ttk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=10)

        projects_button = ButtonsFrame(button_frame, [("Projects", lambda: ProjectListWindowController(self))])
        projects_button.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

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
        
        dwgtitles_button = ButtonsFrame(button_frame, [("Title Manager", lambda:TitleController(parent=self))])
        dwgtitles_button.button_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Center the window after adding widgets
        BaseWindow.center_window(self.root)

        if testing == 1:
            ProjectListWindowController(self)
    

        self.root.mainloop()