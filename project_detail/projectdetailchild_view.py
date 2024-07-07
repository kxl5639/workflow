import tkinter as tk
from tkinter import ttk
from class_collection import ButtonsFrame, BaseWindow
from model import System, Project

class AddSystemWindow(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.model = self.controller.model
        self.systems_devices_data_dict = self.controller.get_systems_devices_data()
        self.number_of_systems = len(self.systems_devices_data_dict)
        self.project_number = self.controller.project_number

        #region FOR TESTING ONLY ****** TO BE DELTED AFTER TESTING IS OVER
        # self.systems_devices_data_dict = {(1, 'AHU'):
        #                          {'devices_tags': {'data': ['SPT', 'CS'], 'max_char': 4},
        #                           'devices_qtys': {'data': [10, 5], 'max_char': 5},
        #                           'devices_descs': {'data': ['Static Pressure Transmitter', 'Current Switch'], 'max_char': 27},
        #                           'devices_manufs': {'data': ['Senva', 'Functional Devices'], 'max_char': 18},
        #                           'devices_models': {'data': ['P4-XXX','H-600'], 'max_char': 6}},
        #                           (2, 'VAV'):
        #                           {'devices_tags': {'data': ['8888'], 'max_char': 4},
        #                            'devices_qtys': {'data': [''], 'max_char': 5},
        #                            'devices_descs': {'data': ['Static Pressure Transmitter'], 'max_char': 27},
        #                            'devices_manufs': {'data': ['Senva'], 'max_char': 18},
        #                            'devices_models': {'data': ['P4-XXX'], 'max_char': 6}}}
        # self.number_of_systems = len(self.systems_devices_data_dict)
        # self.project_number = '2265B'
        #endregion

        self.root.resizable(width=False, height=False)
        self.base_frame.grid_columnconfigure(0, weight=1)

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
        self.new_system = self.add_entry.get()
        proj_id = self.model.get_id_from_model_column_data(Project,'project_number', self.project_number)
        # proj_id = 2
        new_system_record = System(name=self.new_system, project_id=proj_id)
        self.model.add_record(new_system_record)
        self.model.commit_changes()
        self.root.destroy()
        self.parent.destroy()
        self.controller.open_ProjectDetailWindow()
        

        # {(3, 'RTU'): {'devices_tags': {'data': [], 'max_char': 0}, 'devices_qtys': {'data': [], 'max_char': 0}, 'devices_descs': {'data': [], 'max_char': 0}, 'devices_manufs': {'data': [], 'max_char': 0}, 'devices_models': {'data': [], 'max_char': 6}}}
        


if __name__ == '__main__':
    root = tk.Tk()

    new_window = AddSystemWindow('title', root)

    BaseWindow.center_window(root)
    BaseWindow.center_window(new_window.root)
    root.mainloop()
