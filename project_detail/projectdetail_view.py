from class_collection import BaseWindow
import tkinter as tk
from tkinter import ttk

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, is_root)
        self.controller = controller
        self.project_number = project_number

        self.create_project_label()
        self.create_system_base_frame()        
        self.iter_generate_system_frame()

        BaseWindow.center_window(self.root)
    
    def create_project_label(self):
        self.project_label = ttk.Label(self.base_frame,
                                       text = f'EM Number: {self.project_number}')
        self.project_label.grid(row=0,column=0,padx=10,pady=(0,10),sticky='w')
        return self.project_label
    
    def create_system_base_frame(self):
        self.system_base_frame = ttk.Frame(self.base_frame, relief='solid')
        self.system_base_frame.grid(row=1, column=0,padx=10,pady=(0,10))
        return self.system_base_frame

    def create_system_frame(self, row_idx, system_name=None):
        system_frame = ttk.LabelFrame(self.system_base_frame, text=system_name)
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, padx=10, pady=ypad, column=0)
        device_entry = ttk.Entry(system_frame) ######### JUST A PLACE HOLDER
        device_entry.grid(row=0,column=0,padx=10,pady=10,sticky='w')

    def iter_generate_system_frame(self):        
        system_names = self.controller.get_systems_list()
        for idx, system in enumerate(system_names):
            self.create_system_frame(idx,system)
            
