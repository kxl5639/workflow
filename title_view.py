import tkinter as tk
from tkinter import ttk
from view import BaseWindow
from utils import center_window, create_button_frame
from configs import testing
from model import session, Project, DwgTitle


class TitleView:
    def __init__(self, title, parent, controller, project_number):
        self.title = title
        self.parent = parent
        self.controller = controller
        self.project_number = project_number
        self.title_column_break = 10
        self.active_entry_widget = None
        self.title_entry_widgets_list = []

        if __name__ == '__main__':
            self.root = BaseWindow(self.title, self.parent, is_root=isroot).root
        else:
            self.root = BaseWindow(self.title, self.parent).root

        self.root.resizable(width=True, height=True)

        # Create base frame where title entries and menu buttons will live
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.grid(row=0, column=0, sticky='nsew')
        self.base_frame.grid_columnconfigure(0, weight = 1)        

        # Create frame for Project Number
        self.project_frame = ttk.LabelFrame(self.base_frame, text='Project EM')        
        self.project_frame.grid(row=0, column=0, padx = (10,0), pady = (10,0), sticky='w')
        self.combo_project_number = tk.StringVar()
        self.project_combo = ttk.Combobox(self.project_frame,
                                          textvariable=self.combo_project_number, state='readonly')
        self.project_combo.bind('<<ComboboxSelected>>',
                                lambda _:self.controller.on_project_combobox_selected())
        self.project_combo.grid(row=0, column=0, padx = 5, pady = 5, sticky='nsew')
        
        # Load project numbers in combobox
        self.list_project_numbers = self._get_project_numbers_list()
        
        # Create frame for title entries
        self.titles_frame = ttk.LabelFrame(self.base_frame, text='Titles')        
        self.titles_frame.grid(row=1, column=0, padx = (10,0), pady = (0,10), sticky='new')        

        # Create frame for menu buttons
        self.menu_frame = ttk.LabelFrame(self.base_frame, text='Menu')
        self.menu_frame.grid(row=1, column=1, padx = 10, pady = (0,10), sticky='n')

        # Create button in menu frame
        self.add_button = create_button_frame(self.menu_frame,[('(+) Title',
                                                                lambda:self.controller.add_entry(self.titles_frame))])
        self.add_button.grid(row=0, column=0, padx=(10), pady = 10)
        self.moveup_button = create_button_frame(self.menu_frame,[('Move Up',
                                                                   lambda:self.controller.moveup_entry())])
        self.moveup_button.grid(row=1, column=0, padx=(10), pady = (0,10))
        self.movedown_button = create_button_frame(self.menu_frame,[('Move Down',
                                                                     lambda:self.controller.movedown_entry())])        
        self.movedown_button.grid(row=2, column=0, padx=(10), pady = (0,10))

        # Load the main contents of the titles_frame
        self._load_body(self.project_number)

        center_window(self.root)
        self.root.focus_force()                       

    def _load_body(self, project_number):
        '''Loads the title entries dependent on project selection'''       
        if project_number is None:
            # Prompt user to select a project number                            
            prompt_label = ttk.Label(self.titles_frame, text='Please select a project!')
            prompt_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        else:
            project_obj = self.controller.get_project_object(project_number)            
            self._remove_title_widgets()            
            # Get information of page numbers and titles from project object
            title_objs_list = self.controller.get_title_object(project_obj)
            if not title_objs_list: self._default_title_entries()
            else:
                for title_obj in title_objs_list:
                    entry_widget = self.create_entry_widget(self.titles_frame)
                    entry_widget.insert(0, title_obj.title)
            
    def _remove_title_widgets(self):
        '''Removes title widgets and resizes the window'''        
        self.root.withdraw()
        for widget in self.titles_frame.winfo_children():
            widget.destroy()
            self.title_entry_widgets_list = []
            self.titles_frame.update_idletasks() # Restores title frame back to proper size after removing widgets                
        self.root.geometry('')        
        self.root.deiconify()
        center_window(self.root)        

    def _default_title_entries(self):
        '''Creates title entries and default entries with GENERAL NOTES, COMM RISER, MASTER PANEL'''
        for _ in range(self.title_column_break): self.create_entry_widget(self.titles_frame)
        self.title_entry_widgets_list[0].insert(0, 'GENERAL NOTES')
        self.title_entry_widgets_list[1].insert(0, 'COMMUNICATION RISER')
        self.title_entry_widgets_list[2].insert(0, 'MASTER CONTROL PANEL')

    def _get_project_numbers_list(self):
        project_numbers_list = [project.project_number for project in session.query(Project).all()]        
        self.project_combo['values'] = project_numbers_list
        return project_numbers_list
        
    def on_project_selected(self):
        selected_project_number = self.combo_project_number.get()      
        ####### NEED TO CHECK IF VALUES CHANGED BEFORE SWITCHING TO NEW PROJECT INFOS    
        self._load_body(selected_project_number)        

    def create_entry_widget(self, parent):
        '''Creates entry widgets'''
        # Check how many existing entry widgets there are
        entry_count = len(self.title_entry_widgets_list)
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
        self.title_entry_widgets_list.append(entry) 
        self.titles_frame.grid_columnconfigure(in_column, weight = 1)
        if entry_count % self.title_column_break == 0 or entry_count == self.title_column_break-1:
            center_window(self.root)
        return entry

    def _get_active_entry_widget(self, entry):
        self.active_entry_widget = entry

    def _update_widget_data(self, entry_widget, data):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, data)

    def move_entry(self, direction):
        if self.active_entry_widget:
            if (direction == 'up' and self.active_entry_widget != self.title_entry_widgets_list[0]) or \
            (direction == 'down' and self.active_entry_widget != self.title_entry_widgets_list[-1]):                
                curr_idx = self.title_entry_widgets_list.index(self.active_entry_widget)
                new_idx = curr_idx - 1 if direction == 'up' else curr_idx + 1
                
                def _swap_widget_data(idx1, idx2):
                    data1 = self.title_entry_widgets_list[idx1].get()
                    data2 = self.title_entry_widgets_list[idx2].get()
                    self._update_widget_data(self.title_entry_widgets_list[idx1], data2)
                    self._update_widget_data(self.title_entry_widgets_list[idx2], data1)
                
                _swap_widget_data(curr_idx, new_idx)
                self.active_entry_widget = self.title_entry_widgets_list[new_idx]
                self.title_entry_widgets_list[new_idx].focus_set()
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