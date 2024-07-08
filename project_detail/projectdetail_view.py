from class_collection import BaseWindow, ButtonsFrame
from project_detail.projectdetailchild_view import AddSystemWindow
import tkinter as tk
from tkinter import ttk, messagebox

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.project_number = project_number
        self.system_frames_collec_dict = {}
        
        self.controller.get_systems_devices_data()
        self.base_frame.columnconfigure(0, weight=1)
        self.create_project_label()
        self.create_systems()
        self.create_add_system_button_frame()
        self.create_devices()
        
        BaseWindow.center_window(self.root)

#####################################################################################

    def create_project_label(self):
        self.project_label = ttk.Label(self.base_frame,
                                       text = f'EM Number: {self.project_number}')
        self.project_label.grid(row=0,column=0,padx=10,pady=(0,10),sticky='w')
        return self.project_label

    def refresh_systems_data_view(self):
        def destroy_frames():
            for system_frame in self.system_frames_collec_dict.values():
                system_frame[0].destroy()
            self.system_frames_collec_dict = {}
            
        self.systems_devices_data_dict, self.number_of_systems = self.controller.get_systems_devices_data()
        destroy_frames()
        self.iter_generate_system_frame()
        self.create_devices()
        BaseWindow.center_window(self.root)
    
    def create_add_system_button_frame(self):
        def add_system_button_cmd():
            self.add_system_window = AddSystemWindow('Add New System', self, controller=self.controller)
    
        system_add_button_frame = ButtonsFrame(self.system_base_frame, [('Add System', lambda: add_system_button_cmd())])
        system_add_button_frame.button_frame.grid(row=1,column=0,
                                                  padx=(10),pady=(0,10), sticky='e')

    def create_systems(self):
        #region Functions
        def create_system_base_frame():
            self.system_base_frame = ttk.Frame(self.base_frame, relief='solid')
            self.system_base_frame.grid(row=1, column=0,padx=10,pady=(0,10), sticky='nsew')
            self.system_base_frame.columnconfigure(0, weight=1)
            return self.system_base_frame
        
        def create_system_data_frame():
            self.system_data_frame = ttk.Frame(self.system_base_frame)
            self.system_data_frame.grid(row=0, column=0,padx=10,pady=10, sticky='nsew')
            self.system_data_frame.columnconfigure(0, weight=1)
            return self.system_data_frame
        #endregion

        create_system_base_frame()
        create_system_data_frame()
        self.iter_generate_system_frame()
        
    def iter_generate_system_frame(self):        

        def create_system_frame(row_idx, system_key):
            def pady_config(row_idx):
                if self.controller.number_of_systems == 0:
                    ypad = 0
                elif self.controller.number_of_systems == 1:
                    ypad = (10,0)
                elif row_idx == 0:
                    ypad = 10
                elif row_idx==self.controller.number_of_systems-1:
                    ypad = 0
                else: 
                    ypad = (0,10)
                return ypad
            
            def create_frame():
                system_frame = ttk.Frame(self.system_data_frame, relief= 'solid')
                ypad = pady_config(row_idx)
                system_frame.grid(row=row_idx, column=0, padx=10, pady=ypad, sticky='nsew')        
                system_frame.columnconfigure(0, weight=1)
                return system_frame
            
            def create_system_header_frame(parent):
                system_header_frame = ttk.Frame(parent)
                system_header_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky='nsew')
                system_header_frame.columnconfigure(0, weight=1)
                return system_header_frame

            def create_system_device_frame(parent):
                system_device_frame = ttk.Frame(parent)
                system_device_frame.grid(row=1, column=0, padx=10, pady=(0,10), sticky='nsew')        
                system_device_frame.columnconfigure(0, weight=1)
                return system_device_frame
            
            def create_system_name_label(parent, system_name):
                system_name_label = ttk.Label(parent, text=system_name.upper(),
                                                font=("Helvetica", 10, "bold"))
                system_name_label.grid(row=0,column=0,padx=10,pady=0,sticky='w')
                return system_name_label
            
            def delete_system_button_cmd(system_name):
                confirm = messagebox.askyesno('Confirm Delete',
                                             f'Are you sure you want to delete system {system_name} and all its associated drawings and devices?\n\nThis action cannot be undone.',
                                             parent=self.root)
                if confirm:
                    self.controller.delete_system(system_name)
                    self.refresh_systems_data_view()

            def create_system_delete_button(parent, system_name):
                system_delete_button = ButtonsFrame(parent, [('Delete System', lambda: delete_system_button_cmd(system_name))])
                system_delete_button.button_frame.grid(row=0,column=1,padx=10,pady=0,sticky='nse')

            system_name: str = system_key[1]
            system_frame = create_frame()
            system_header_frame = create_system_header_frame(system_frame)
            system_device_frame = create_system_device_frame(system_frame)
            create_system_name_label(system_header_frame, system_name)
            create_system_delete_button(system_header_frame, system_name)
            self.system_frames_collec_dict[system_key] = [system_frame, system_device_frame]

        if self.controller.systems_devices_data_dict:
            for idx, system_key in enumerate(self.controller.systems_devices_data_dict.keys()):
                create_system_frame(idx, system_key)

    def create_devices(self):
        #region Functions
        def create_device_base_frame(parent):
            device_base_frame = ttk.LabelFrame(parent, text='Devices')
            device_base_frame.grid(row=1,column=0,padx=10,pady=(0,10),sticky='nsew')
            device_base_frame.grid_columnconfigure(0, weight=1)
            return device_base_frame
        
        def create_add_device_button(parent):
                device_add_button_frame = ButtonsFrame(parent, [('Add Device', None)])
                device_add_button_frame.button_frame.grid(row=1, column=0,
                                                          padx=10, pady=(0,10), sticky='e')         

        def create_data_frame(parent):
            device_data_frame = ttk.Frame(parent)
            device_data_frame.grid(row=0,column=0,padx=10,pady=(0,10),sticky='nsew')
            return device_data_frame

        def iter_generate_device_frame(parent, system_key): # parent is device_data_frame
            #region Functions
            def create_device_frame(parent, row_idx, system_key):
                def create_device_tag_entry(parent, row_idx, system_key):
                    device_tag_data = self.controller.systems_devices_data_dict[system_key]['devices_tags']['data'][row_idx]
                    def validate_input_length(P):
                        if len(P) > 7:  # Limit to 10 characters
                            return False
                        return True
                    vcmd = (parent.register(validate_input_length), '%P')
                    device_tag_entry = ttk.Entry(parent,width=8, validate='key', validatecommand=vcmd)
                    device_tag_entry.grid(row=row_idx+1,column=0)
                    device_tag_entry.delete(0, tk.END)
                    device_tag_entry.insert(0, device_tag_data)

                def create_device_label(parent, row_idx, system_key, dev_prop_key, col):
                    device_data = self.controller.systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
                    label_width = self.controller.systems_devices_data_dict[system_key][dev_prop_key]['max_char'] + 2
                    device_label = ttk.Label(parent, text=f' {device_data}', relief='solid', width=label_width)
                    device_label.grid(row=row_idx+1,column=col, stick='nsew')
                
                def create_device_spinbox(parent, row_idx, system_key, dev_prop_key, col):
                    device_data = self.controller.systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
                    label_width = self.controller.systems_devices_data_dict[system_key][dev_prop_key]['max_char'] 
                    device_spinbox = ttk.Spinbox(parent, from_=0, to=9999, width=label_width)
                    device_spinbox.set(device_data)
                    device_spinbox.grid(row=row_idx+1,column=col, sticky='nsew')

                create_device_tag_entry(parent, row_idx, system_key)
                create_device_label(parent, row_idx, system_key, 'devices_descs', 1)
                create_device_label(parent, row_idx, system_key, 'devices_manufs', 2)
                create_device_label(parent, row_idx, system_key, 'devices_models', 3)
                create_device_spinbox(parent, row_idx, system_key, 'devices_qtys', 4)
                delete_device_button = ButtonsFrame(parent, [('Delete', None)])
                delete_device_button.button_frame.grid(row=row_idx+1, column=5, padx=(5,0))

            def create_device_header(parent):
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
                header_list = ['Tag', 'Description', 'Manufacturer', 'Model', 'Qty']
                width_dict = self.controller.max_device_data_char_dict
                width_list = []
                for header in header_list:
                    for idx, key in enumerate(width_dict.keys()):
                        clean_key = extract_model_from_string(key).lower()
                        if clean_key in header.lower():
                            width_list.append(width_dict[key])
                for idx, header in enumerate(header_list):
                    label_tag = ttk.Label(parent, text=header, width=width_list[idx]+2)
                    label_tag.grid(row=0,column=idx,sticky='nsew')

            #endregion

            manufs_list = self.controller.systems_devices_data_dict[system_key]['devices_manufs']['data']
            if manufs_list:
                num_devices = len(manufs_list)
                create_device_header(parent)
                for row_idx in range(num_devices):
                    create_device_frame(parent, row_idx, system_key)
        #endregion

        if self.controller.number_of_systems != 0:
            for system_key, system_frame in self.system_frames_collec_dict.items():
                device_base_frame = create_device_base_frame(system_frame[1])
                create_add_device_button(device_base_frame)
                device_data_frame = create_data_frame(device_base_frame)
                iter_generate_device_frame(device_data_frame, system_key)