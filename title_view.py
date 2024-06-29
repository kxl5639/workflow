import tkinter as tk
from tkinter import ttk
from view import BaseWindow
from utils import center_window, create_button_frame
from configs import testing

class TitleView:
    def __init__(self, title, parent) -> None:
        self.title = title
        self.parent = parent
        self.entry_widget_counter = 0

        if __name__ == '__main__':
            self.root = BaseWindow(self.title, self.parent, is_root=isroot).root
        else:
            self.root = BaseWindow(self.title, self.parent).root

        self.root.resizable(width=True, height=True)

        # Create frame where title entries and menu buttons will live
        base_frame = ttk.Frame(self.root)
        base_frame.grid(row=0, column=0, sticky='nsew')
        base_frame.grid_columnconfigure(0, weight = 1)
        base_frame.grid_rowconfigure(0, weight = 1)

        # Create frame for title entries
        entries_frame = ttk.LabelFrame(base_frame, text='Titles')        
        entries_frame.grid(row=0, column=0, padx = (10,0), pady = 10, sticky='new')
        entries_frame.grid_columnconfigure(0, weight = 1)

        # Create initial title entry object
        init_entry_frame = ttk.Frame(entries_frame)
        init_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        init_entry_frame.grid_columnconfigure(1, weight = 1)
        init_entry_label = ttk.Label(init_entry_frame, text=1)
        init_entry_label.grid(row=0, column=0, padx=(0,5))
        init_entry = ttk.Entry(init_entry_frame)
        init_entry.grid(row=0, column=1, sticky='nsew')        

        # Create frame for menu buttons
        menu_frame = ttk.LabelFrame(base_frame, text='Menu')
        menu_frame.grid(row=0, column=1, padx = 10, pady = 10, sticky='n')

        # Create button in menu frame
        add_button = create_button_frame(menu_frame,[('Add', None)])
        add_button.grid(row=0, column=0, padx=(10), pady = 10)

        moveup_button = create_button_frame(menu_frame,[('Move Up', None)])
        moveup_button.grid(row=1, column=0, padx=(10), pady = (0,10))

        center_window(self.root)
        self.root.focus_force()

    def create_entry_widget():
        '''Creates entry widgets'''
        pass


if __name__ == '__main__':
    if testing == 1:
        isroot = True
    else:
        isroot = False
    root = TitleView('Title Manager', None).root
    root.mainloop()