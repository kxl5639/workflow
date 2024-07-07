import tkinter as tk
from tkinter import ttk
from class_collection import ButtonsFrame

from class_collection import BaseWindow

class AddSystemWindow(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)

        self.root.resizable(width=False, height=False)
        self.base_frame.grid_columnconfigure(0, weight=1)

        add_label = ttk.Label(self.root, text='Add System Name')
        add_label.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')

        add_entry_frame = ttk.Frame(self.root)
        add_entry_frame.grid(row=1,column=0,padx=10,pady=(0,10),sticky='nsew')

        add_entry = ttk.Entry(add_entry_frame, width=40)
        add_entry.grid(row=0,column=0, sticky='nsew')

        add_button_frame = ButtonsFrame(add_entry_frame,[('Add', lambda: self.add_button_cmd())])
        add_button_frame.button_frame.grid(row=0,column=1, padx=(10,0), sticky='nsew')
    
        BaseWindow.center_window(self.root)

    def add_button_cmd(self):pass