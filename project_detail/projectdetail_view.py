from class_collection import BaseWindow
import tkinter as tk
from tkinter import ttk

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, is_root)
        self.controller = controller
        self.project_number = project_number

        self.base_frame.columnconfigure(0, weight=1)
        self.create_project_label()
        self.create_system_base_frame()
        self.controller.get_systems_devices_data()
        # self.iter_generate_system_frame()
        

        BaseWindow.center_window(self.root)
    
    def create_project_label(self):
        self.project_label = ttk.Label(self.base_frame,
                                       text = f'EM Number: {self.project_number}')
        self.project_label.grid(row=0,column=0,padx=10,pady=(0,10),sticky='w')
        return self.project_label
    
    def create_system_base_frame(self):
        self.system_base_frame = ttk.Frame(self.base_frame, relief='solid')
        self.system_base_frame.grid(row=1, column=0,padx=10,pady=(0,10), sticky='nsew')
        self.system_base_frame.columnconfigure(0, weight=1)
        return self.system_base_frame

    def create_system_frame(self, row_idx, system_name, system_id=None):        
        system_frame = ttk.LabelFrame(self.system_base_frame, text=system_name)
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad, sticky='nsew')        
        system_frame.columnconfigure(0, weight=1)
        device_base_frame = self.create_device_base_frame(system_frame)
        self.iter_generate_device_frame(device_base_frame, system_id)

    def create_add_system_frame(self, row_idx):
        system_frame = ttk.LabelFrame(self.system_base_frame, text='Add System')
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad)
        system_add_label = ttk.Label(system_frame, text='Click here to add a new system.')      
        system_add_label.grid(row=0,column=0,padx=10,pady=10)

    def iter_generate_system_frame(self):        
        system_names, system_ids = self.controller.get_systems_names_ids_list()
        if system_names:
            for idx, (system_name, system_id) in enumerate(zip(system_names, system_ids)):
                self.create_system_frame(idx,system_name, system_id)
        else:
            self.create_add_system_frame(0)

    def create_device_base_frame(self, parent):
        device_base_frame = ttk.LabelFrame(parent, text='Devices')
        device_base_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        device_base_frame.grid_columnconfigure(0, weight=1)
        return device_base_frame

    def create_add_device_frame(self, parent, row_idx):        
        ypad = 10 if row_idx == 0 else (0,10)
        device_add_label = ttk.Label(parent, text='Click here to add a new device.')      
        device_add_label.grid(row=0,column=0,padx=10,pady=ypad)

    def iter_generate_device_frame(self, parent, system_id):        
        devices_data_dict = self.controller.get_system_devices_data(system_id)
        if devices_data_dict:
            num_devices = len(devices_data_dict[system_id]['devices_models']['data'])            
            for row_idx in range(num_devices):
                self.create_device_frame(parent, row_idx, system_id, devices_data_dict)
        else:
            self.create_add_device_frame(parent, 0)

    def create_device_frame(self, parent, row_idx, system_id, devices_data_dict):
        device_frame = ttk.Frame(parent, relief='solid')
        ypad = 10 if row_idx == 0 else (0,10)
        device_frame.grid(row=row_idx,column=0,padx=10,pady=ypad,sticky='nsew')
        device_frame.grid_columnconfigure((1,2,3), weight=1)
        tag_data = devices_data_dict[system_id]['devices_tags']['data'][row_idx]

        self.create_device_tag_entry(device_frame, tag_data)
        desc_data = devices_data_dict[system_id]['devices_descs']['data'][row_idx]
        self.create_device_label(device_frame, desc_data, 1)
        manf_data = devices_data_dict[system_id]['devices_manfs']['data'][row_idx]
        self.create_device_label(device_frame, manf_data, 2)
        model_data = devices_data_dict[system_id]['devices_models']['data'][row_idx]
        self.create_device_label(device_frame, model_data, 3)

    def create_device_tag_entry(self, parent, device_tag_data):
        def validate_input_length(P):
            if len(P) > 7:  # Limit to 10 characters
                return False
            return True
        vcmd = (parent.register(validate_input_length), '%P')
        device_tag_entry = ttk.Entry(parent,width=8, validate='key', validatecommand=vcmd)
        device_tag_entry.grid(row=0,column=0)
        device_tag_entry.delete(0, tk.END)
        device_tag_entry.insert(0, device_tag_data)

    def create_device_label(self, parent, device_data, col):
        device_desc_label = ttk.Label(parent, text=device_data, relief='solid')
        device_desc_label.grid(row=0,column=col, stick='nsew')