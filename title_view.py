import tkinter as tk
from tkinter import ttk
from view import BaseWindow
from utils import center_window, create_button_frame
from configs import testing


class TitleView:
    def __init__(self, title, parent, controller):
        self.title = title
        self.parent = parent
        self.controller = controller
        self.title_column_break = 10
        self.active_entry_widget = None
        self.title_entry_widgets = []

        if __name__ == '__main__':
            self.root = BaseWindow(self.title, self.parent, is_root=isroot).root
        else:
            self.root = BaseWindow(self.title, self.parent).root

        self.root.resizable(width=True, height=True)

        # Create base frame where title entries and menu buttons will live
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.grid(row=0, column=0, sticky='nsew')
        self.base_frame.grid_columnconfigure(0, weight = 1)
        self.base_frame.grid_rowconfigure(0, weight = 1)

        # Create frame for Project Number
        self.project_frame = ttk.LabelFrame(self.base_frame, text='Project EM')        
        self.project_frame.grid(row=0, column=0, padx = (10,0), pady = (10,0), sticky='w')
        self.project_entry = ttk.Entry(self.project_frame)
        self.project_entry.grid(row=0, column=0, padx = 5, pady = 5, sticky='nsew')
        
        # Create frame for title entries
        self.titles_frame = ttk.LabelFrame(self.base_frame, text='Titles')        
        self.titles_frame.grid(row=1, column=0, padx = (10,0), pady = (0,10), sticky='new')
        # self.titles_frame.grid_columnconfigure(0, weight = 1)

        # Create initial title entry object
        for i in range(1,self.title_column_break+1):
            self.create_entry_widget(self.titles_frame)        

        # Create frame for menu buttons
        self.menu_frame = ttk.LabelFrame(self.base_frame, text='Menu')
        self.menu_frame.grid(row=1, column=1, padx = 10, pady = (0,10), sticky='n')

        # Create button in menu frame
        self.add_button = create_button_frame(self.menu_frame,[('Add', lambda:self.controller.add_entry(self.titles_frame))])
        self.add_button.grid(row=0, column=0, padx=(10), pady = 10)
        self.moveup_button = create_button_frame(self.menu_frame,[('Move Up', lambda:self.controller.moveup_entry())])
        self.moveup_button.grid(row=1, column=0, padx=(10), pady = (0,10))
        self.movedown_button = create_button_frame(self.menu_frame,[('Move Down', lambda:self.controller.movedown_entry())])
        self.movedown_button.grid(row=2, column=0, padx=(10), pady = (0,10))

        center_window(self.root)
        self.root.focus_force()           

    def create_entry_widget(self, parent):
        '''Creates entry widgets'''
        # Check how many existing entry widgets there are
        entry_count = len(self.title_entry_widgets)
        in_column = entry_count // self.title_column_break
        in_row = entry_count - (in_column*self.title_column_break)
        entry_frame = ttk.Frame(parent)
        ypad = 10 if entry_count % self.title_column_break == 0 else (0,10) 
        entry_frame.grid(row=in_row, column=in_column, padx=10, pady=ypad, sticky='nsew')
        entry_frame.grid_columnconfigure(1, weight = 1)
        entry_label = ttk.Label(entry_frame, text=entry_count+1)
        entry_label.grid(row=0, column=0, padx=(0,5))
        entry = ttk.Entry(entry_frame)
        entry.grid(row=0, column=1, sticky='nsew')
        entry.bind("<FocusIn>", lambda event: self._get_active_entry_widget(entry))
        self.title_entry_widgets.append(entry) 
        self.titles_frame.grid_columnconfigure(in_column, weight = 1)
        if entry_count % self.title_column_break == 0 or entry_count == self.title_column_break-1:
            center_window(self.root)

    def _get_active_entry_widget(self, entry):
        self.active_entry_widget = entry

    def _update_widget_data(self, entry_widget, data):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, data)

    def move_entry(self, direction):
        if self.active_entry_widget:
            if (direction == 'up' and self.active_entry_widget != self.title_entry_widgets[0]) or \
            (direction == 'down' and self.active_entry_widget != self.title_entry_widgets[-1]):                
                curr_idx = self.title_entry_widgets.index(self.active_entry_widget)
                new_idx = curr_idx - 1 if direction == 'up' else curr_idx + 1
                
                def _swap_widget_data(idx1, idx2):
                    data1 = self.title_entry_widgets[idx1].get()
                    data2 = self.title_entry_widgets[idx2].get()
                    self._update_widget_data(self.title_entry_widgets[idx1], data2)
                    self._update_widget_data(self.title_entry_widgets[idx2], data1)
                
                _swap_widget_data(curr_idx, new_idx)
                self.active_entry_widget = self.title_entry_widgets[new_idx]
                self.title_entry_widgets[new_idx].focus_set()
            else:
                self.active_entry_widget.focus_set()

if __name__ == '__main__':
    if testing == 1:
        isroot = True
    else:
        isroot = False
    from title_controller import TitleController
    controller = TitleController()
    root = TitleView('Title Manager', None, controller).root
    root.mainloop()