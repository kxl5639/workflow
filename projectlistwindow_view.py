from view import BaseWindow
import tkinter as tk
from tkinter import ttk

class ProjectAddModifyWindow(BaseWindow):
    def __init__(self, title, parent, controller, is_root=False, is_modify=False):
        super().__init__(title, parent.root, is_root)        
        self.title = title
        self.parent = parent
        self.controller = controller
        self.is_modify = is_modify
        self.tree = self.parent.tree_frame.tree

        self.create_project_section()        
        self.create_client_section()
        self.create_me_section()    
        self.create_mc_section()
        self.fill_combobox_options()

        BaseWindow.center_window(self.root)

    def fill_combobox_options(self):
        self.data = self.controller.fill_combobox_options()        
        self.pm_name['values'] = self.data['projectmanagers']
        self.de_name['values'] = self.data['designengineers']
        self.se_name['values'] = self.data['salesengineers']


    def create_mc_section(self):
        self.mc_frame = self.create_section_frame("Mechanical Contractor", 0, 3)
        self.mc_name = self.create_label_entry(self.mc_frame, "Name", 0, 0)
        self.mc_address = self.create_label_entry(self.mc_frame, "Address", 1, 0)
        self.mc_city = self.create_label_entry(self.mc_frame, "City", 2, 0)
        self.mc_state = self.create_label_entry(self.mc_frame, "State", 3, 0)
        self.mc_zip_code = self.create_label_entry(self.mc_frame, "Zip Code", 4, 0)
        self.mc_telephone = self.create_label_entry(self.mc_frame, "Telephone", 5, 0)
    
    def create_me_section(self):
        self.me_frame = self.create_section_frame('Mechanical Engineer', 0, 2)
        self.me_name = self.create_label_entry(self.me_frame, "Name", 0, 0)
        self.me_address = self.create_label_entry(self.me_frame, "Address", 1, 0)
        self.me_city = self.create_label_entry(self.me_frame, "City", 2, 0)
        self.me_state = self.create_label_entry(self.me_frame, "State", 3, 0)
        self.me_zip_code = self.create_label_entry(self.me_frame, "Zip Code", 4, 0)

    def create_client_section(self):
        self.client_frame = self.create_section_frame('Client', 0, 1)
        self.client_name = self.create_label_entry(self.client_frame, "Client", 0, 0)
        self.client_scope = self.create_label_entry(self.client_frame, "Scope", 1, 0)
        self.client_address = self.create_label_entry(self.client_frame, "Address", 2, 0)
        self.client_city = self.create_label_entry(self.client_frame, "City", 3, 0)
        self.client_state = self.create_label_entry(self.client_frame, "State", 4, 0)
        self.client_zip_code = self.create_label_entry(self.client_frame, "Zip Code", 5, 0)

    def create_project_section(self):
        self.project_frame = self.create_section_frame('Project Info', 0, 0)
        self.project_number_entry = self.create_label_entry(self.project_frame, 'Project Number', 0, 0)
        self.em_type_entry = self.create_label_entry(self.project_frame, 'EM Type', 1, 0)
        self.job_phase_entry = self.create_label_entry(self.project_frame, 'Job Phase', 2, 0)
        self.submit_date_entry = self.create_label_entry(self.project_frame, 'Submit Date', 3, 0)
        self.pm_name = self.create_combobox(self.project_frame, 'Project Manager', 4, 0)
        self.de_name = self.create_combobox(self.project_frame, 'Design Engineer', 5, 0)
        self.se_name = self.create_combobox(self.project_frame, 'Sales Engineer', 6, 0)

    def create_section_frame(self, text, row, column):
        frame = ttk.Labelframe(self.base_frame, text=text)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
        frame.grid_columnconfigure(1, weight=1)
        return frame
    
    def create_label_entry(self, parent, label_text, row, column):
        ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
        return entry
    
    def create_combobox(self, parent, label_text, row, column):
        ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
        combobox = ttk.Combobox(parent, state="readonly")
        combobox.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
        return combobox

    def set_entry_text(self, entry_widget, text):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)