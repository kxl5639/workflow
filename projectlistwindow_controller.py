from projectlistwindow_model import ProjectListWindowModel
from projectlistwindow_view import ProjectAddModifyWindow
from model import session, ProjectManager, DesignEngineer, SalesEngineer, Client, MechanicalContractor, MechanicalEngineer, Project
from view import ListWindow
from tkinter import messagebox

class ProjectListWindowController:
    def __init__(self, parent=None) -> None:
        self.parent = parent        
        self.model = ProjectListWindowModel()
        self.column_map = self.model.colump_map
        self.table_data = self.model.table_data
        self.button_info = [("Add", lambda: self.add_button_command()),
                    ("Modify", lambda: self.modify_button_command()),
                    ("Delete", None)]             
        self.view = ListWindow(title = 'Projects List', parent=self.parent, controller=self)        

    def add_or_mod_commit_button_command(self, is_modify, data, parent):        
        if not self.check_for_blanks(data, parent):
            return False
        
        self.project_data = data['project']        
        self.client_data = data['client']
        self.me_data = data['me']
        self.mc_data = data['mc']
        data= None

        if is_modify:
            tree_selection = self.view.tree_frame.tree.selection()        
            selected_record_iid = tree_selection[0] # The item identifier (iid) is the project ID        
            self.update_existing_record_obj()
            self.model.commit_changes()
            parent.destroy()
            self.view.refresh_tree()
            self.view.tree_frame.tree.selection_set(selected_record_iid)
            self.view.tree_frame.tree.focus(selected_record_iid)
            self.view.tree_frame.tree.see(selected_record_iid) 
            # existing_page_titleobj_dict[new_page_number].title = new_title_name                
        else:
            if self.check_project_unique(parent):                    
                self.commit_add()
                parent.destroy()
                self.view.refresh_tree()    
    
    def update_existing_record_obj(self):
        print('about to modify')
        proj_data_dict = self.project_data
        pm_first_name = proj_data_dict['pm_first_name']
        pm_last_name = proj_data_dict['pm_last_name']
        se_first_name = proj_data_dict['se_first_name']
        se_last_name = proj_data_dict['se_last_name']
        de_first_name = proj_data_dict['de_first_name']
        de_last_name = proj_data_dict['de_last_name']
        # Gets id so that we can compare it to the record object dict
        projectmanager_id = session.query(ProjectManager).filter_by(first_name=pm_first_name,last_name=pm_last_name).first().id
        designengineer_id = session.query(DesignEngineer).filter_by(first_name=de_first_name,last_name=de_last_name).first().id
        salesengineer_id = session.query(SalesEngineer).filter_by(first_name=se_first_name,last_name=se_last_name).first().id
        client_id = session.query(Client).filter_by(client_name=self.client_data['client_name']).first().id
        mechanicalengineer_id = session.query(MechanicalEngineer).filter_by(name=self.me_data['name']).first().id
        mechanicalcontractor_id = session.query(MechanicalContractor).filter_by(name=self.mc_data['name']).first().id
        # Deletes keys that doesn't match with record object dict
        del proj_data_dict['pm_first_name']
        del proj_data_dict['pm_last_name']
        del proj_data_dict['se_first_name']
        del proj_data_dict['se_last_name']
        del proj_data_dict['de_first_name']
        del proj_data_dict['de_last_name']
        # Insert keys with the values as ids so that we can compare it with the record obj dict
        proj_data_dict['client_id'] = client_id
        proj_data_dict['mechanicalengineer_id'] = mechanicalengineer_id
        proj_data_dict['mechanicalcontractor_id'] = mechanicalcontractor_id
        proj_data_dict['projectmanager_id'] = projectmanager_id
        proj_data_dict['designengineer_id'] = designengineer_id
        proj_data_dict['salesengineer_id'] = salesengineer_id
        proj_num = self.project_data['project_number']
        proj_obj = self.model.get_project_object(proj_num)
        print(f'new info: {proj_data_dict}')
        # record_obj_dict = {key: value for key, value in proj_obj.__dict__.items() if not key.startswith('_')}
        # print(f'old info: {record_obj_dict}')
        for key, value in proj_data_dict.items():
            if getattr(proj_obj, key) != value:
                setattr(proj_obj, key, value)        

    def check_project_unique(self, parent):
        print('Executed check')
        data = self.project_data        
        proj_num_to_add = data['project_number']
        existing_proj_nums = self.model.query_proj_nums()
        print(existing_proj_nums)
        for existing_proj_num in existing_proj_nums:
            if proj_num_to_add in existing_proj_num:
                print('Fond a duplicate')
                messagebox.showwarning('Duplicate Project',
                                       f'Cannot add project. {proj_num_to_add} already exists.',
                                       parent=parent)
                return False
        return True        

    def update_table_data(self):
        return self.model.update_table_data()

    def commit_add(self):
        records_to_add = [self.set_project_record(),
                self.set_client_record(),
                self.set_pm_record(),
                self.set_me_record(),
                self.set_mc_record(),
                self.set_de_record(),
                self.set_se_record()
                ]
        for record in records_to_add:
            self.model.add_record(record)
        self.model.commit_changes()        

    def check_for_blanks(self, data, parent):
        empty_entries = self.check_empty(data)
        if empty_entries != {}:
            cln_empty_entries = self._clean_for_readability(empty_entries)
            self._produce_error_message(cln_empty_entries, parent)
            return False
        else: return True

    def check_empty(self, data):        
        empty_entries = {}
        for section, entry_dict in data.items():            
            for label, entry in entry_dict.items():                
                if entry == '':
                    if section in empty_entries:
                        empty_entries[section].append(label)
                    else:
                        empty_entries[section] = []
                        empty_entries[section].append(label)
        return(empty_entries)

    def _produce_error_message(self, cln_empty_entries, parent):
        message_lines = ['The following field(s) are missing.\n']
        for section, entries in cln_empty_entries.items():
            message_lines.append(f"{section.capitalize()}:")
            for entry in entries:
                message_lines.append(f" - {entry}")
            message_lines.append("")  # Add a blank line for spacing
        messagebox.showinfo('Missing Fields',"\n".join(message_lines),parent=parent)        

    def _clean_for_readability(self, empty_entries):         
        section_replacements = {'project': 'Project Info',
                                'client': 'Client',
                                'me': 'Mechanical Engineer',
                                'mc': 'Mechanical Contractor',
                                }
        field_replacements = {'project_number': 'Project Number',
                              'em_type': 'EM Type',
                              'job_phase': 'Job Phase',
                              'submit_date': 'Submit Date',
                              'pm_first_name' : 'Project Manager',
                              'pm_last_name' : '',
                              'de_first_name' : 'Design Engineer',
                              'de_last_name' : '',
                              'se_first_name' : 'Sales Engineer',
                              'se_last_name' : '',
                              'client_name': 'Client Name',
                              'scope': 'Scope',
                              'name': 'Name',
                              'address': 'Address',
                              'city': 'City',
                              'state': 'State',
                              'zip_code': 'Zip Code',
                              'telephone': 'Telephone'}
        de_se_remove = {}
        section_remove = []
        for section, entry_list in empty_entries.items():
            idx = -1
            if section in section_replacements:
                section_remove.append(section)
            for entry in entry_list:                    
                if entry in field_replacements:
                    idx += 1                    
                    if 'last_name' in entry.lower():
                        if section in de_se_remove:
                            de_se_remove[section].append(entry)
                        else:
                            de_se_remove[section] = []
                            de_se_remove[section].append(entry)
                    else:                        
                        try:
                            empty_entries[section][idx] = field_replacements[entry]                
                            # empty_entries[section][idx] = section_replacements[entry]
                        except:
                            empty_entries[section][idx] = field_replacements[entry]
        if de_se_remove:
            for section, entries in de_se_remove.items():                
                for entry in entries:
                    if entry in empty_entries.get(section, []):
                        empty_entries[section].remove(entry)                    
        if section_remove:
            for section in section_remove:
                empty_entries[section_replacements[section]] = empty_entries.pop(section)        
        return empty_entries

    def set_se_record(self):
        return SalesEngineer(first_name = self.project_data['se_first_name'],
                                  last_name = self.project_data['se_last_name']
                                  )

    def set_de_record(self):
        return DesignEngineer(first_name = self.project_data['de_first_name'],
                              last_name = self.project_data['de_last_name']
                              )

    def set_mc_record(self):
        return MechanicalContractor(name = self.mc_data['name'],
                                  address = self.mc_data['address'],
                                  city = self.mc_data['city'],
                                  state = self.mc_data['state'],
                                  zip_code = self.mc_data['zip_code'],
                                  telephone = self.mc_data['telephone'],
                                  )

    def set_me_record(self):
        return MechanicalEngineer(name = self.me_data['name'],
                                  address = self.me_data['address'],
                                  city = self.me_data['city'],
                                  state = self.me_data['state'],
                                  zip_code = self.me_data['zip_code']
                                  )

    def set_pm_record(self):
        return ProjectManager(first_name = self.project_data['pm_first_name'],
                              last_name = self.project_data['pm_last_name']
                              )

    def set_client_record(self): 
        return Client(client_name = self.client_data['client_name'],
                      scope = self.client_data['scope'],
                      address = self.client_data['address'],
                      city = self.client_data['city'],
                      state = self.client_data['state'],
                      zip_code = self.client_data['zip_code'],
                      )       

    def set_project_record(self):        
        return Project(project_number = self.project_data['project_number'],
                       em_type = self.project_data['em_type'],
                       job_phase = self.project_data['job_phase'],
                       submit_date = self.project_data['submit_date'],
                       client_id = session.query(Client).filter_by(client_name=self.client_data['client_name']).first().id,
                       projectmanager_id = session.query(ProjectManager).filter_by(first_name=self.project_data['pm_first_name'],last_name=self.project_data['pm_last_name']).first().id,
                       mechanicalengineer_id = session.query(MechanicalEngineer).filter_by(name=self.me_data['name']).first().id,
                       mechanicalcontractor_id = session.query(MechanicalContractor).filter_by(name=self.mc_data['name']).first().id,
                       designengineer_id = session.query(DesignEngineer).filter_by(first_name=self.project_data['de_first_name'],last_name=self.project_data['de_last_name']).first().id,
                       salesengineer_id = session.query(SalesEngineer).filter_by(first_name=self.project_data['se_first_name'],last_name=self.project_data['se_last_name']).first().id,
                       )

    def add_button_command(self):
        self.add_window = ProjectAddModifyWindow(title='Add New Project', parent=self.view, controller=self)

    def modify_button_command(self):
        if self.validate_modify_selection():
            self.modify_window = ProjectAddModifyWindow(title='Modify Project', parent=self.view, controller=self,is_modify=True)

    def validate_modify_selection(self):
        tree_selection = self.view.tree_frame.tree.selection()
        if len(tree_selection) == 0:
            messagebox.showinfo('Select Project','Select a project to be modified.',parent=self.view.root)
            return False
        elif len(tree_selection) > 1:
            messagebox.showinfo('Select Project','Please select only (1) project to be modified.',parent=self.view.root)
            return False
        else:            
            return True

    def get_combobox_options(self):        
        model_list = [ProjectManager, DesignEngineer, SalesEngineer]
        results = {model.__tablename__: [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).order_by(model.first_name).all()] for model in model_list}        
        return results
    
    def fetch_record_data(self):
        tree_selection = self.view.tree_frame.tree.selection()        
        selected_record_iid = tree_selection[0] # The item identifier (iid) is the project ID        
        # selected_record_obj = session.query(Project).get(selected_record_iid)
        project = session.query(Project).filter_by(id=selected_record_iid).first()
        client = session.query(Client).filter_by(id=project.client_id).first()
        pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
        me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
        mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
        de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
        se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
        return {'project':project, 'client':client, 'pm':pm, 'me':me, 'mc':mc, 'de':de, 'se':se}
        
        


        
        
        