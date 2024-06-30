import tkinter as tk
from tkinter import ttk
from view import BaseWindow
from utils import center_window, create_button_frame
from configs import testing


class TitleView:
    def __init__(self, title, parent, controller) -> None:
        self.title = title
        self.parent = parent
        self.controller = controller
        self.title_column_break = 10
        self.active_entry_widget = None

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

        # Create frame for title entries
        self.entries_frame = ttk.LabelFrame(self.base_frame, text='Titles')        
        self.entries_frame.grid(row=0, column=0, padx = (10,0), pady = 10, sticky='new')
        self.entries_frame.grid_columnconfigure(0, weight = 1)

        # Create initial title entry object
        for i in range(1,self.title_column_break+1):
            self.create_entry_widget(self.entries_frame)        

        # Create frame for menu buttons
        self.menu_frame = ttk.LabelFrame(self.base_frame, text='Menu')
        self.menu_frame.grid(row=0, column=1, padx = 10, pady = 10, sticky='n')

        # Create button in menu frame
        self.add_button = create_button_frame(self.menu_frame,[('Add', lambda:self.controller.add_entry(self.entries_frame))])
        self.add_button.grid(row=0, column=0, padx=(10), pady = 10)
        self.moveup_button = create_button_frame(self.menu_frame,[('Move Up', lambda:self.controller.moveup_entry())])
        self.moveup_button.grid(row=1, column=0, padx=(10), pady = (0,10))
        self.movedown_button = create_button_frame(self.menu_frame,[('Move Down', lambda:self.controller.movedown_entry)])
        self.movedown_button.grid(row=2, column=0, padx=(10), pady = (0,10))

        center_window(self.root)
        self.root.focus_force()
            
    def _count_entry_widgets(self):
        '''Counts the number of entry widgets in the entire window hierarchy'''
        def count_entries_recursive(widget):
            count = 0
            if isinstance(widget, ttk.Entry):
                count += 1
            for child in widget.winfo_children():
                count += count_entries_recursive(child)
            return count
        
        count = count_entries_recursive(self.root)
        return count

    def create_entry_widget(self, parent):
        '''Creates entry widgets'''
        # Check how many existing entry widgets there are
        entry_count = self._count_entry_widgets()
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
        if entry_count % self.title_column_break == 0 or entry_count == self.title_column_break-1:
            center_window(self.root)

    def _get_active_entry_widget(self, entry):
        self.active_entry_widget = entry

    def moveup_entry(self):
        # Get data from active entry widget
        try:
            curr_data = self.active_entry_widget.get()
        except AttributeError: print('Nothing Selected')
        else:
            print(curr_data)
        # Get data from entry widget above
        

    def movedown_entry(self):
        pass


if __name__ == '__main__':
    if testing == 1:
        isroot = True
    else:
        isroot = False
    from title_controller import TitleController
    controller = TitleController()
    root = TitleView('Title Manager', None, controller).root
    root.mainloop()