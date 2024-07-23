import tkinter as tk
from tkinter import ttk, messagebox
from devicemanager import DeviceListBaseView
from class_collection import BaseWindow, ButtonsFrame

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.project_number = project_number
        self.system_frames_collec_dict = {}
        # Create a ttk Style object
        self.style = ttk.Style()
        # Configure a new style called "Custom.TFrame" with a desired background color
        self.style.configure('Custom.TFrame', background="#FFDDC1")
        self.base_frame.grid(row=0,column=1)
        
        self.systems_devices_data_dict, self.max_device_data_char_dict, _ = self.controller.get_systems_devices_data()
        self.base_frame.columnconfigure(1, weight=1)
        self.project_info_frame = self.create_project_info_frame(self.base_frame)
        self.project_label = self.create_project_label(self.project_info_frame)
        self.create_systems()
        self.create_add_system_button_frame()
        self.create_devices(self.systems_devices_data_dict, self.max_device_data_char_dict)
        self.left_menu_frame = self.create_left_menu_frame(self.root)
        self.create_title_manager_button(self.left_menu_frame)

        BaseWindow.center_window(self.root)

#####################################################################################

############################## System Frame Structure ###############################
#                                                                                   #
#                                                           -> system_header_frame  #
#  system_base_frame -> system_data_frame -> system_frame [                         #
#                                                           -> system_device_frame  #
#                                                                                   #
#####################################################################################

    def create_project_info_frame(self, parent):
        project_info_frame = ttk.Frame(parent, relief='solid')
        project_info_frame.grid(row=0, column=0, pady=(0,10), sticky='nsew')
        return project_info_frame

    def create_project_label(self, parent):
        project_label = ttk.Label(parent, text = f'EM Number: {self.project_number}')
        project_label.grid(row=0,column=0,padx=10,pady=10,sticky='w')
        return project_label

    def create_left_menu_frame(self, parent):
        left_menu_frame = ttk.Frame(parent, relief='solid')
        left_menu_frame.grid(row=0, column=0, padx=(10,0), pady=10, sticky='nsew')
        return left_menu_frame
    
    def create_title_manager_button(self, parent):
        title_manager_button = ButtonsFrame(parent, [('Title Manager',
                                                                    lambda: self.controller.open_title_manager())])
        title_manager_button.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

    def refresh_systems_data_view(self):
        def destroy_frames():
            for system_frame in self.system_frames_collec_dict.values():
                system_frame[0].destroy()
            self.system_frames_collec_dict = {}
            
        self.systems_devices_data_dict, _, self.number_of_systems = self.controller.get_systems_devices_data()
        destroy_frames()
        self.iter_generate_system_frame()
        self.create_devices(self.systems_devices_data_dict, self.max_device_data_char_dict)
        BaseWindow.center_window(self.root)

    def create_add_system_button_frame(self):
        def add_system_button_cmd():
            self.controller.system_add_btn_cmd()
    
        system_add_button_frame = ButtonsFrame(self.system_base_frame, [('Add System',
                                                                         lambda: add_system_button_cmd())])
        system_add_button_frame.button_frame.grid(row=1,column=0,
                                                  padx=(10,0),pady=(10,0), sticky='e')

    def create_systems(self):
        def create_system_base_frame():
            self.system_base_frame = ttk.Frame(self.base_frame)
            self.system_base_frame.grid(row=1, column=0,padx=0,pady=(0,0), sticky='nsew')
            self.system_base_frame.columnconfigure(0, weight=1)
            return self.system_base_frame
        
        def create_system_data_frame():
            self.system_data_frame = ttk.Frame(self.system_base_frame)
            self.system_data_frame.grid(row=0, column=0,padx=0,pady=(0), sticky='nsew')
            self.system_data_frame.columnconfigure(0, weight=1)
            return self.system_data_frame

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
                    ypad = (0,10)
                elif row_idx==self.controller.number_of_systems-1:
                    ypad = 0
                else: 
                    ypad = (0,10)
                return ypad
            
            def create_frame():
                system_frame = ttk.Frame(self.system_data_frame, relief= 'solid')
                ypad = pady_config(row_idx)
                system_frame.grid(row=row_idx, column=0, padx=0, pady=ypad, sticky='nsew')        
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
                system_name_label.grid(row=0,column=0,padx=(0,10),pady=0,sticky='w')
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
                system_delete_button.button_frame.grid(row=0,column=1,padx=(10,0),pady=0,sticky='nse')

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

    def create_devices(self, systems_devices_data_dict, max_device_data_char_dict):
                
        def create_add_device_button(parent, system_key):
                def add_device_button_cmd():
                    self.controller.add_new_device(system_key)
                device_add_button_frame = ButtonsFrame(parent, [('Add Device',
                                                                 lambda: add_device_button_cmd())])
                device_add_button_frame.button_frame.grid(row=1, column=0,
                                                          padx=10, pady=(0,10), sticky='e')  

        if self.controller.number_of_systems != 0:
            for system_key, system_frame in self.system_frames_collec_dict.items():
                device_base_frame = DeviceListBaseView.create_device_section(self.controller,
                                                                             system_frame[1],
                                                                             system_key,
                                                                             systems_devices_data_dict,
                                                                             max_device_data_char_dict)
                create_add_device_button(device_base_frame, system_key)