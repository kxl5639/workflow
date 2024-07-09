import tkinter as tk
from tkinter import ttk
from class_collection import BaseWindow, ButtonsFrame
from model import session, Project

class TitleView:
    def __init__(self, title, parent, controller, project_number):
        self.title = title
        self.parent = parent
        self.controller = controller
        self.project_number = project_number
        self.title_column_break = 15
        self.active_entry_widget = None  
        self.entry_frames_names = {} # Dictionary of names : entry frame widget. Used to destroy() blank entry frames
        self.root = BaseWindow(self.title, self.parent, controller=self.controller).root
        self.root.resizable(width=True, height=True)

        self._create_base_frame()
        self._create_project_number_frame()
        self._create_titles_frame()
        self._create_right_toolbar_frame()
        self._create_save_frame()
        self._create_menu_frame()
        self._create_autocad_src_frame()

        # Load the main contents of the titles_frame
        self._load_body(self.project_number)
        BaseWindow.center_window(self.root)
        self.root.focus_force()

#####################################################################################

    #region Creating widgets on screen
    def _create_base_frame(self):
        '''Create base frame where title entries and menu buttons will live'''
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.grid(row=0, column=0, sticky='nsew')
        self.base_frame.grid_columnconfigure(0, weight = 1)

    def _create_project_number_frame(self):
        '''Create frame for Project Number'''
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

    def _create_titles_frame(self):
        # Create frame for title entries
        self.titles_frame = ttk.LabelFrame(self.base_frame, text='Titles')
        self.titles_frame.grid(row=1, column=0, padx = (10,0), pady = (0,10), sticky='new')

    def _create_save_frame(self):
        # Create frame for save button
        self.save_frame = ttk.Frame(self.base_frame)
        self.save_frame.grid(row=0, column=1, padx = (10,10), pady = (10,0), sticky='nsew')
        self.save_frame.grid_rowconfigure(0, weight=1)
        self.save_frame.grid_columnconfigure(0, weight=1)
        self.save_button = ttk.Button(self.save_frame, text='Save Titles',
                                      command=lambda:self.controller.commit_titles(self.combo_project_number.get()))
        self.save_button.grid(row=0, column=0)

    def _create_right_toolbar_frame(self):
        # Create frame for title entries
        self.right_toolbar_frame = ttk.Frame(self.base_frame)
        self.right_toolbar_frame.grid(row=1, column=1, padx = (10,10), pady = (0,10), sticky='new')

    def _create_menu_frame(self):
        # Create frame for menu buttons
        self.menu_frame = ttk.LabelFrame(self.right_toolbar_frame, text='Menu')
        self.menu_frame.grid(row=1, column=1, padx = 10, pady = (0,10), sticky='n')
        # Create button in menu frame
        self.add_button = ButtonsFrame(self.menu_frame,[('(+) Title',
                                                                lambda:self.controller.add_entry(self.titles_frame))])
        self.add_button.button_frame.grid(row=0, column=0, padx=(10), pady = 10)
        self.moveup_button = ButtonsFrame(self.menu_frame,[('Move Up',
                                                                   lambda:self.controller.moveup_entry())])
        self.moveup_button.button_frame.grid(row=1, column=0, padx=(10), pady = (0,10))
        self.movedown_button = ButtonsFrame(self.menu_frame,[('Move Down',
                                                                     lambda:self.controller.movedown_entry())])
        self.movedown_button.button_frame.grid(row=2, column=0, padx=(10), pady = (0,10))

    def _create_autocad_src_frame(self):
        # Create frame for scr button
        self.scr_frame = ttk.LabelFrame(self.right_toolbar_frame, text='Generate SCR')
        self.scr_frame.grid(row=2, column=1, padx = 10, pady = (0,10), sticky='n')
        # Create button in scr frame
        self.add_button = ButtonsFrame(self.scr_frame,[('Write SCR',
                                                                lambda:self.controller.write_scr(self.project_number))])
        self.add_button.button_frame.grid(row=0, column=0, padx=(10), pady = 10)
        
    #endregion

    def _load_body(self, project_number):
        '''Loads the title entries dependent on project selection'''     
        def _prompt_select_project():
            """Prompt user to select a project."""
            prompt_label = ttk.Label(self.titles_frame, text='Please select a project!')
            prompt_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        def _load_project_titles(project_number):
            """Load the titles for the selected project."""
            project_obj = self.controller.get_project_object(project_number)
            self._remove_title_widgets()
            # Get information of page numbers and titles from project object
            title_objs_list = self.controller.get_title_object(project_obj)
            if not title_objs_list: self._default_title_entries()
            else:
                for title_obj in title_objs_list:
                    entry_widget = self.create_entry_widget(self.titles_frame)
                    entry_widget.insert(0, title_obj.title)

        if project_number is None: _prompt_select_project()
        else: _load_project_titles(project_number)
        BaseWindow.center_window(self.root)
            
    def _remove_title_widgets(self):
        '''Removes ALL title widgets and resizes the window'''
        self.root.withdraw()
        for widget in self.titles_frame.winfo_children():
            widget.destroy()
            self.title_entry_widgets_list = []
            self.titles_frame.update_idletasks() # Restores title frame back to proper size after removing widgets
        self.root.geometry('')
        self.root.deiconify()
        BaseWindow.center_window(self.root)

    def destroy_frames_if_labels_match(self, numbers):
        entry_frame_to_be_popped = []
        for item in numbers:
            for page_number, entry_frame in self.entry_frames_names.items():
                if page_number == item:
                    entry_frame_to_be_popped.append(page_number)
                    entry_frame.destroy()
        for item in entry_frame_to_be_popped:
            del self.entry_frames_names[item]
        self.get_all_entry_widgets(self.root)
        BaseWindow.center_window(self.root)

    def _default_title_entries(self):
        '''Creates title entries and default entries with GENERAL NOTES, COMM RISER, MASTER PANEL'''
        for _ in range(self.title_column_break):
            self.create_entry_widget(self.titles_frame)
        self.title_entry_widgets_list = self.get_all_entry_widgets(self.root)
        self.title_entry_widgets_list[0].insert(0, 'GENERAL NOTES')
        self.title_entry_widgets_list[1].insert(0, 'COMMUNICATION RISER')
        self.title_entry_widgets_list[2].insert(0, 'MASTER CONTROL PANEL')

    def _get_project_numbers_list(self):
        project_numbers_list = [project.project_number for project in session.query(Project).all()]
        self.project_combo['values'] = project_numbers_list
        return project_numbers_list
        
    def on_project_selected(self):        
        self.project_number = self.combo_project_number.get()
        ####### NEED TO CHECK IF VALUES CHANGED BEFORE SWITCHING TO NEW PROJECT INFOS
        self._load_body(self.project_number)        

    def create_entry_widget(self, parent):
        '''Creates entry widgets'''

        def _get_active_entry_widget(entry):
            self.active_entry_widget = entry
        
        def create_entry_frame(parent):
            entry_frame = ttk.Frame(parent)        
            ypad = 10 if entry_count % self.title_column_break == 0 else (0,10) 
            entry_frame.grid(row=in_row, column=in_column, padx=10, pady=ypad, sticky='nsew')
            entry_frame.grid_columnconfigure(1, weight = 1)
            return entry_frame

        # Count existing entries
        entry_count = len(self.get_all_entry_widgets(self.root))

        # Calculate column and rows indexes
        in_column = entry_count // self.title_column_break
        in_row = entry_count - (in_column*self.title_column_break)

        # Create entry frame
        entry_frame = create_entry_frame(parent)

        # Store entry frames
        self.entry_frames_names[entry_count+1] = entry_frame
        
        # Create number index label
        entry_label = ttk.Label(entry_frame, text=entry_count+1)
        entry_label.grid(row=0, column=0, padx=(0,5))

        # Create title entry widget
        entry = ttk.Entry(entry_frame, width=50)
        entry.grid(row=0, column=1, sticky='nsew')
        entry.bind("<FocusIn>", lambda event: _get_active_entry_widget(entry))
        self.titles_frame.grid_columnconfigure(in_column, weight = 1)
        if entry_count % self.title_column_break == 0 or entry_count == self.title_column_break-1:
            BaseWindow.center_window(self.root)
        return entry

    def get_all_entry_widgets(self, parent):
        entry_widgets = []
        
        def find_entries(widget):
            if isinstance(widget, (tk.Entry, ttk.Entry)) and not isinstance(widget, ttk.Combobox):
                entry_widgets.append(widget)
            for child in widget.winfo_children():
                find_entries(child)
        
        find_entries(parent)
        return entry_widgets

    def move_entry(self, direction):

        def _swap_widget_data(entry1, entry2):
            data1 = entry1.get()
            data2 = entry2.get()
            _update_widget_data(entry1, data2)
            _update_widget_data(entry2, data1)

        def _update_widget_data(entry_widget, data):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, data)

        # Gets list of all title entry widgets

        self.title_entry_widgets_list = self.get_all_entry_widgets(self.root)

        # Check if an entry widget is selected and move up/down if yes
        if self.active_entry_widget:
            if (direction == 'up' and self.active_entry_widget != self.title_entry_widgets_list[0]) or \
            (direction == 'down' and self.active_entry_widget != self.title_entry_widgets_list[-1]):
                curr_idx = self.title_entry_widgets_list.index(self.active_entry_widget)
                new_idx = curr_idx - 1 if direction == 'up' else curr_idx + 1
                curr_entry = self.title_entry_widgets_list[curr_idx]
                new_entry = self.title_entry_widgets_list[new_idx]
                _swap_widget_data(curr_entry, new_entry)
                self.active_entry_widget = self.title_entry_widgets_list[new_idx]
                self.active_entry_widget.focus_set()
            else:
                self.active_entry_widget.focus_set()