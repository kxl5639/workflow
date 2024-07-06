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

    def create_system_frame(self, row_idx, system_name, system_id):        
        system_frame = ttk.LabelFrame(self.system_base_frame, text=system_name)
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad)
        device_base_frame = self.create_device_base_frame(system_frame)
        self.iter_generate_device_frame(device_base_frame, system_id)

    def iter_generate_system_frame(self):        
        system_names, system_ids = self.controller.get_systems_names_ids_list()
        for idx, (system_name, system_id) in enumerate(zip(system_names, system_ids)):
            self.create_system_frame(idx,system_name, system_id)

    def create_device_base_frame(self, parent):
        device_base_frame = ttk.LabelFrame(parent, text='Devices')
        device_base_frame.grid(row=0,column=0,padx=10,pady=10)
        return device_base_frame

    def create_device_frame(self, parent, row_idx, device_name=None):
        device_frame = ttk.Frame(parent, relief='solid')
        ypad = 10 if row_idx == 0 else (0,10)
        device_frame.grid(row=row_idx,column=0,padx=10,pady=ypad)
        device_label = ttk.Label(device_frame, text=device_name)
        device_label.grid(row=0,column=0)

    # def iter_generate_device_frame(self, parent, system_id):
    #     devices_names, devices_ids = self.controller.get_devices_names_ids_list(system_id)
    #     for idx, (device_name, device_id) in enumerate(zip(devices_names, devices_ids)):
    #         self.create_device_frame(parent, idx, device_name, device_id)

    def iter_generate_device_frame(self, parent, system_id):
        devices_ids = self.controller.get_devices_ids_list(system_id)
        for idx, device_id in enumerate(devices_ids):
            self.create_device_frame(parent, idx, device_id)