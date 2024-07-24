import tkinter as tk
from tkinter import ttk
from class_collection import ButtonsFrame, BaseWindow, View
from tkinter import messagebox
from devicemanager import DeviceListBaseView
from project_detail.projectdetail_view import ProjectDetailWindow

class AddSystemWindow(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.model = self.controller.model
        self.systems_devices_data_dict, _, self.number_of_systems = self.controller.get_systems_devices_data()
        self.project_number = self.controller.project_number
        self.root.resizable(width=False, height=False)

        add_label = ttk.Label(self.root, text='Add System Name')
        add_label.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')

        add_entry_frame = ttk.Frame(self.root)
        add_entry_frame.grid(row=1,column=0,padx=10,pady=(0,10),sticky='nsew')

        self.add_entry = ttk.Entry(add_entry_frame, width=40)
        self.add_entry.grid(row=0,column=0, sticky='nsew')

        add_button_frame = ButtonsFrame(add_entry_frame,[('Add', lambda: self.add_button_cmd())])
        add_button_frame.button_frame.grid(row=0,column=1, padx=(10,0), sticky='nsew')
        
        BaseWindow.center_window(self.root)
        self.add_entry.focus_set()

    def add_button_cmd(self):
        error_msg = self.controller.add_new_system(self.add_entry)
        if not error_msg:
            self.controller.view.refresh_systems_data_view()
            self.root.destroy()
            BaseWindow.center_window(self.controller.view.root)
        else:
            messagebox.showerror('Error', error_msg, parent=self.root)

class AddDeviceWindow(DeviceListBaseView):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.root.resizable(width=False, height=False)
        self.create_exist_device_list()
        self.root.protocol("WM_DELETE_WINDOW", controller.on_close)
        self.center_window(self.root)

###################### Frame Structure ######################
#                                                           #
#  base_frame [ -> tree_frame                               #
#               -> device_list_frame [ -> system_name_frame #
#                                      -> devices_frame     #
#                                                           #
#############################################################

    def create_exist_device_list(self):
        def create_device_list_frame(parent):
            device_list_frame = View.create_frame(parent, 1, 0, 0, 0,
                                                  relief=None)
            return device_list_frame
        
        def create_system_name_frame(parent):
            
            system_name_frame = View.create_frame(parent, 0, 1, 0, 0,
                                                  relief=self.relief)
            return system_name_frame
            
        def create_system_name_label(parent):
            system_name_label = View.create_label(parent, 0, 0, 0, 0, relief=self.relief)
            system_name_label['text'] = f'SYSTEM: {self.controller.system_key[1]}'
            return system_name_label

        def create_devices_frame(parent):
            devices_frame = View.create_frame(parent, 1, 1, 0, 0,
                                                relief=self.relief)
            return devices_frame

        self.device_list_frame = create_device_list_frame(self.base_frame)
        self.system_name_frame = create_system_name_frame(self.device_list_frame)
        create_system_name_label(self.system_name_frame)
        self.devices_frame = create_devices_frame(self.device_list_frame)
        device_selection_frame, self.device_tag_entry_list = DeviceListBaseView.create_device_section(self.controller,
                                                                          self.devices_frame,
                                                                          self.controller.system_key,
                                                                          self.controller.systems_devices_data_dict,
                                                                          self.controller.max_device_data_char_dict)
        self.device_list_frame.update_idletasks()
        device_selection_frame.update_idletasks()
        device_list_frame_width = self.device_list_frame.winfo_width()
        device_selection_frame_width = device_selection_frame.winfo_width()

        spacer_width = (device_list_frame_width-device_selection_frame_width)/2
        View.create_frame(self.device_list_frame, 0, 0, 0, 0).configure(width=spacer_width)
        View.create_frame(self.device_list_frame , 0, 2, 0, 0).configure(width=spacer_width)
        View.create_frame(self.device_list_frame, 1, 0, 0, 0).configure(width=spacer_width)
        View.create_frame(self.device_list_frame, 1, 2, 0, 0).configure(width=spacer_width)

    
    def on_double_click(self):
        
        item_id = self.tree_frame.tree.selection()[0]
        item = self.tree_frame.tree.item(item_id)
        device_model = item['values'][3]

        spec_qty_window = BaseWindow('Specify Quantity', self, self.controller)   
        prompt_label = self.create_label(spec_qty_window.base_frame,
                                         f'Specify quantity of {device_model} to be added:',
                                         0, 0, (0,0), (0,0))
        qty_spinbox = ttk.Spinbox(spec_qty_window.base_frame, from_=0, to=9999, width=5)
        qty_spinbox.grid(row=1, column=0, pady=(10,0))

        add_button_frame = ButtonsFrame(spec_qty_window.base_frame,
                                        [('Add',
                                          lambda: self.controller.add_dev_btn_cmd(device_model,qty_spinbox.get()))])
        add_button_frame.button_frame.grid(row=2,column=0, pady=(10,0), sticky='ns')

        # Enter key invokes add button
        self.root.bind_all('<Return>', add_button_frame.button_list[0].invoke())
        # Make the window stay on top
        spec_qty_window.root.attributes('-topmost', True)
        # Disable interactions with the main window
        self.parent.root.attributes('-disabled', True)
        # Make other windows frozen
        spec_qty_window.root.grab_set()
        BaseWindow.center_window(spec_qty_window.root)
