import tkinter as tk
from tkinter import ttk
from class_collection import ButtonsFrame, BaseWindow, ListWindow
from tkinter import messagebox
from devicemanager import DeviceListBaseView

class AddSystemWindow(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.model = self.controller.model
        self.systems_devices_data_dict = self.controller.get_systems_devices_data()
        self.number_of_systems = len(self.systems_devices_data_dict)
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

class AddDeviceWinow(DeviceListBaseView):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)

        self.center_window(self.root)
    
    def on_double_click(self):
        pass
        