from view import BaseWindow, ButtonsFrame
import tkinter as tk
from tkinter import ttk
from configs import testing

class ProjectAddModifyWindow(BaseWindow):
    def __init__(self, title, parent, controller, is_root=False, is_modify=False):
        super().__init__(title, parent.root, is_root)        
        self.title = title
        self.parent = parent
        self.controller = controller
        self.is_modify = is_modify
        self.tree = self.parent.tree_frame.tree
        self.root.resizable(width=False,height=False)
        
        self.data_frame = self.create_data_frame()
        self.create_project_section()
        self.load_combobox_options()
        self.create_client_section()
        self.create_me_section()    
        self.create_mc_section()
        self.load_data()
        self.create_buttons()        
                
        BaseWindow.center_window(self.root)
        self.project_number_entry.focus_set()

    def create_buttons(self):
        button_text = 'Modify' if self.is_modify else 'Add'
        self.buttons_frame = ButtonsFrame(self.base_frame,
                                          [(button_text, lambda: self.add_or_modify_commit()),
                                           ('Cancel', lambda: self.root.destroy())],)
        self.buttons_frame.button_frame.grid(row=1, column=0)

    def add_or_modify_commit(self):
        data = {'project':self.get_project_data(),
                'client':self.get_client_data(),
                'me':self.get_me_data(),
                'mc':self.get_mc_data()}        
        self.controller.add_or_mod_commit_button_command(self.is_modify, data, self.root)

    def load_data(self):
        if self.is_modify:                        
            self.load_tree_selection_data()
        else:
            self.load_default_data()        

    def load_tree_selection_data(self):
        self.selected_record_data = self.controller.fetch_record_data()
        self.load_selected_project_data(self.selected_record_data)
        self.load_selected_client_data(self.selected_record_data)
        self.load_selected_me_data(self.selected_record_data)
        self.load_selected_mc_data(self.selected_record_data)

    def load_selected_mc_data(self, data):
        mc_data = data['mc']        
        self.set_entry_text(self.mc_name, mc_data.name)
        self.set_entry_text(self.mc_address, mc_data.address)
        self.set_entry_text(self.mc_city, mc_data.city)
        self.set_entry_text(self.mc_state, mc_data.state)
        self.set_entry_text(self.mc_zip_code, str(mc_data.zip_code))
        self.set_entry_text(self.mc_telephone, mc_data.telephone)

    def load_selected_me_data(self, data):
        me_data = data['me']
        self.set_entry_text(self.me_name, me_data.name)
        self.set_entry_text(self.me_address, me_data.address)
        self.set_entry_text(self.me_city, me_data.city)
        self.set_entry_text(self.me_state, me_data.state)
        self.set_entry_text(self.me_zip_code, str(me_data.zip_code))

    def load_selected_client_data(self, data):
        client_data = data['client']
        self.set_entry_text(self.client_name, client_data.client_name)
        self.set_entry_text(self.client_scope, client_data.scope)
        self.set_entry_text(self.client_address, client_data.address)
        self.set_entry_text(self.client_city, client_data.city)
        self.set_entry_text(self.client_state, client_data.state)
        self.set_entry_text(self.client_zip_code, str(client_data.zip_code))

    def load_selected_project_data(self, data):
        project_data = data['project']
        pm_data = data['pm']
        de_data = data['de']
        se_data = data['se']
        self.set_entry_text(self.project_number_entry, project_data.project_number)
        self.project_number_entry.config(state='readonly')
        self.set_entry_text(self.em_type_entry, project_data.em_type)
        self.set_entry_text(self.job_phase_entry, project_data.job_phase)
        self.set_entry_text(self.submit_date_entry, project_data.submit_date)
        self.pm_name.set(f"{pm_data.first_name} {pm_data.last_name}")
        self.de_name.set(f"{de_data.first_name} {de_data.last_name}")
        self.se_name.set(f"{se_data.first_name} {se_data.last_name}")

    def load_default_data(self):
        if testing == 1:
            def find_entries(widget):
                if isinstance(widget, (tk.Entry, ttk.Entry)) and not isinstance(widget, ttk.Combobox):
                    self.set_entry_text(widget,"TEST")
                for child in widget.winfo_children():
                    find_entries(child)
            find_entries(self.root)            
            self.set_entry_text(self.submit_date_entry, "XX/XX/XX")
            self.pm_name.current(0)
            self.de_name.current(0)
            self.se_name.current(0)
        else:
            self.set_entry_text(self.em_type_entry, 'B')
            self.set_entry_text(self.job_phase_entry, 1)
            self.de_name.set(f'Kevin Lee')            

    def load_combobox_options(self):
        self.data = self.controller.get_combobox_options()        
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

    def create_data_frame(self):
        data_frame = ttk.Frame(self.base_frame)
        data_frame.grid(row=0, column=0, sticky='nsew')
        return data_frame
    
    def create_section_frame(self, text, row, column):
        frame = ttk.Labelframe(self.data_frame, text=text)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky='n')
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

    def get_project_data(self):
        pm_first_name, pm_last_name = '', ''
        de_first_name, de_last_name = '', ''
        se_first_name, se_last_name = '', ''
        # Check and split the project manager name
        pm_name = self.pm_name.get()
        if pm_name:
            pm_first_name, pm_last_name = pm_name.split(' ', 1)
        # Check and split the design engineer name
        de_name = self.de_name.get()
        if de_name:
            de_first_name, de_last_name = de_name.split(' ', 1)
        # Check and split the structural engineer name
        se_name = self.se_name.get()
        if se_name:
            se_first_name, se_last_name = se_name.split(' ', 1)
        return {
            'project_number': self.project_number_entry.get(),
            'em_type': self.em_type_entry.get(),
            'job_phase': self.job_phase_entry.get(),
            'submit_date': self.submit_date_entry.get(),
            'pm_first_name': pm_first_name,
            'pm_last_name' : pm_last_name,
            'de_first_name': de_first_name,
            'de_last_name' : de_last_name,
            'se_first_name': se_first_name,
            'se_last_name' : se_last_name            
        }

    def get_client_data(self):
        return {
            'client_name': self.client_name.get(),
            'scope': self.client_scope.get(),
            'address': self.client_address.get(),
            'city': self.client_city.get(),
            'state': self.client_state.get(),
            'zip_code': self.client_zip_code.get(),
        }

    def get_me_data(self):
        return {
            'name': self.me_name.get(),
            'address': self.me_address.get(),
            'city': self.me_city.get(),
            'state': self.me_state.get(),
            'zip_code': self.me_zip_code.get(),
        }

    def get_mc_data(self):
        return {
            'name': self.mc_name.get(),
            'address': self.mc_address.get(),
            'city': self.mc_city.get(),
            'state': self.mc_state.get(),
            'zip_code': self.mc_zip_code.get(),
            'telephone': self.mc_telephone.get(),
        }