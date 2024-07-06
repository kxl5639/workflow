from class_collection import BaseWindow
import tkinter as tk
from tkinter import ttk, IntVar

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, is_root)
        self.controller = controller
        self.project_number = project_number

        self.base_frame.columnconfigure(0, weight=1)
        self.create_project_label()
        self.create_system_base_frame()
        self.systems_devices_data_dict = self.controller.get_systems_devices_data()
        self.iter_generate_system_frame()
        
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

    def iter_generate_system_frame(self):        
        if self.systems_devices_data_dict:
            for idx, system_key in enumerate(self.systems_devices_data_dict.keys()):
                self.create_system_frame(idx, system_key)
        else:
            self.create_add_system_frame(0)

    def create_system_frame(self, row_idx, system_key):
        system_name = system_key[1]
        system_frame = ttk.LabelFrame(self.system_base_frame, text=system_name,
                                      relief= 'solid')
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad, sticky='nsew')        
        system_frame.columnconfigure(0, weight=1)
        device_base_frame = self.create_device_base_frame(system_frame)
        self.iter_generate_device_frame(device_base_frame, system_key)

    def create_add_system_frame(self, row_idx):
        system_frame = ttk.LabelFrame(self.system_base_frame, text='Add System')
        ypad = 10 if row_idx == 0 else (0,10)
        system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad)
        system_add_label = ttk.Label(system_frame, text='Click here to add a new system.')      
        system_add_label.grid(row=0,column=0,padx=10,pady=10)

    def create_device_base_frame(self, parent):
        device_base_frame = ttk.LabelFrame(parent, text='Devices')
        device_base_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        device_base_frame.grid_columnconfigure(0, weight=1)
        return device_base_frame

    def create_add_device_frame(self, parent, row_idx):        
        ypad = 10 if row_idx == 0 else (0,10)
        device_add_label = ttk.Label(parent, text='Click here to add a new device.')      
        device_add_label.grid(row=0,column=0,padx=10,pady=ypad)

    def iter_generate_device_frame(self, parent, system_key):
        manufs_list = self.systems_devices_data_dict[system_key]['devices_manufs']['data']
        if manufs_list:
            num_devices = len(manufs_list)
            self.create_device_header(parent)
            for row_idx in range(num_devices):
                self.create_device_frame(parent, row_idx, system_key)
        else:            
            self.create_add_device_frame(parent, 0)

    def create_device_frame(self, parent, row_idx, system_key):
        # device_frame = ttk.Frame(parent, relief='solid')
        # ypad = 10 if row_idx == 0 else (0,10)
        # device_frame.grid(row=row_idx+1,column=0,padx=10,pady=ypad,sticky='nsew')
        # device_frame.grid_columnconfigure((1,2,3), weight=1)        
        self.create_device_tag_entry(parent, row_idx, system_key)
        self.create_device_label(parent, row_idx, system_key, 'devices_descs', 1)
        self.create_device_label(parent, row_idx, system_key, 'devices_manufs', 2)
        self.create_device_label(parent, row_idx, system_key, 'devices_models', 3)
        self.create_device_spinbox(parent, row_idx, system_key, 'devices_qtys', 4)

    def create_device_tag_entry(self, parent, row_idx, system_key):
        device_tag_data = self.systems_devices_data_dict[system_key]['devices_tags']['data'][row_idx]
        def validate_input_length(P):
            if len(P) > 7:  # Limit to 10 characters
                return False
            return True
        vcmd = (parent.register(validate_input_length), '%P')
        device_tag_entry = ttk.Entry(parent,width=8, validate='key', validatecommand=vcmd)
        device_tag_entry.grid(row=row_idx+1,column=0)
        device_tag_entry.delete(0, tk.END)
        device_tag_entry.insert(0, device_tag_data)

    def create_device_label(self, parent, row_idx, system_key, dev_prop_key, col):
        device_data = self.systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
        label_width = self.systems_devices_data_dict[system_key][dev_prop_key]['max_char'] + 2
        device_label = ttk.Label(parent, text=f' {device_data}', relief='solid', width=label_width)
        device_label.grid(row=row_idx+1,column=col, stick='nsew')
    
    def create_device_spinbox(self, parent, row_idx, system_key, dev_prop_key, col):
        device_data = self.systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
        label_width = self.systems_devices_data_dict[system_key][dev_prop_key]['max_char'] 
        device_spinbox = ttk.Spinbox(parent, from_=0, to=9999, width=label_width)
        device_spinbox.set(device_data)
        device_spinbox.grid(row=row_idx+1,column=col, sticky='nsew')
    
    def create_device_header(self, parent):
        def extract_model_from_string(input_string):
            # Split the input string by underscore
            parts = input_string.split('_')
            
            # Check if the split result has at least two parts
            if len(parts) >= 2:
                # Get the last part of the split result
                model = parts[-1]
                # Remove the last character if it is 's'
                if model.endswith('s'):
                    model = model[:-1]
                return model
        # device_header_frame = ttk.Frame(parent)
        # device_header_frame.grid(row=0,column=0)
        header_list = ['Tag', 'Description', 'Manufacturer', 'Model', 'Qty']
        width_dict = self.controller.max_device_data_char_dict
        print(f'\n{width_dict}')
        width_list = []
        for header in header_list:
            for idx, key in enumerate(width_dict.keys()):
                clean_key = extract_model_from_string(key).lower()
                if clean_key in header.lower():
                    print(f'{clean_key} is in {header.lower()}')
                    width_list.append(width_dict[key])
        print(width_list)
        for idx, header in enumerate(header_list):
            label_tag = ttk.Label(parent, text=header, width=width_list[idx]+2)
            label_tag.grid(row=0,column=idx,sticky='nsew')
        