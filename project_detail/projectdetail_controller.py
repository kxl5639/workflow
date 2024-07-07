from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetail_model import ProjectDetailModel
from model import session, Project, SystemDevice, System, Device

class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.parent = parent
        self.project_number = project_number
        self.max_device_data_char_dict = {}
        self.systems_devices_data_dict = {}
        self.model = ProjectDetailModel(self, self.project_number)
        self.view = ProjectDetailWindow(f'{self.project_number} Project Detail',
                                        self.parent, self, self.project_number)
    
    def open_ProjectDetailWindow(self):
        self.view = ProjectDetailWindow(f'{self.project_number} Project Detail',
                                        self.parent, self, self.project_number)

    def get_systems_devices_data(self):
        # Gets all systems keys of the project number
        systems_keys = self.get_systems_keys()
        # Gets all the device data (tag, desc, manf, etc...) for each system_key
            # Also gets the max character length for each device data
        for system_key in systems_keys:
            self.get_devices_data(system_key)
            self.get_max_devices_data_char(self.systems_devices_data_dict, system_key)
        # Update max char for each systems_devices_data_dict
        for system_key in systems_keys:
            # system_id = system_key[0]
            for device_prop_key in self.systems_devices_data_dict[system_key]:
                self.systems_devices_data_dict[system_key][device_prop_key]['max_char']=self.max_device_data_char_dict[device_prop_key]
        return self.systems_devices_data_dict
    
    def get_max_devices_data_char(self, systems_devices_data_dict, system_key):        
        for cat in systems_devices_data_dict[system_key].keys():
            if cat not in self.max_device_data_char_dict:
                if cat == 'devices_models':
                    self.max_device_data_char_dict[cat] = 6
                else:
                    self.max_device_data_char_dict[cat] = 0
            for next in systems_devices_data_dict[system_key][cat]['data']:
                if cat == 'devices_qtys':
                    self.max_device_data_char_dict[cat] = 5
                else:
                    if len(next) > self.max_device_data_char_dict[cat]:
                        self.max_device_data_char_dict[cat] = len(next)

    def get_systems_keys(self):
        '''Generates the key as a tuple [ex: (1, 'AHU')] for self.systems_devices_data_dict.'''
        systems_ids = self.get_systems_ids_from_proj_num()
        systems_keys = []
        for idx, system_id in enumerate(systems_ids):
            system_obj = self.model.get_objs_from_column_data(System,'id',system_id)
            system_name = system_obj[0].name
            systems_keys.append((system_id, system_name))
        return systems_keys

    def get_systems_ids_from_proj_num(self):
        proj_id = self.model.get_id_from_model_column_data(Project, 'project_number', self.project_number)
        systems_objs = self.model.get_objs_from_column_data(System, 'project_id', proj_id)
        systems_ids = []
        for system_obj in systems_objs:
            systems_ids.append(system_obj.id)
        return systems_ids

    def get_devices_data(self, system_key):
            system_id = system_key[0]
            systemdevices_ids = self.get_child_ids_list(SystemDevice, system_id, 'system_id')
            devices_ids = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'device_id')
            devices_tags = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'tag')
            devices_qtys = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'qty')
            devices_descs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'description')
            devices_manufs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'manufacturer')
            devices_models = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'model')
            self.systems_devices_data_dict[system_key] = {'devices_tags' : {'data':devices_tags, 'max_char':0},
                                                         'devices_qtys' : {'data':devices_qtys, 'max_char':0},
                                                          'devices_descs' : {'data':devices_descs, 'max_char':0},
                                                          'devices_manufs' : {'data':devices_manufs, 'max_char':0},
                                                          'devices_models' : {'data':devices_models, 'max_char':0}}

    def get_target_col_vals_list_by_known_col_val(self, model, known_col, known_vals, target_col):
        '''
        Gets target attribute value from the same table if a attribute value in that record is known
        '''
        target_attributes = []
        for known_val in known_vals:
            target_attr = self.model.get_target_col_val_by_known_col_val(model,known_col, known_val, target_col)
            target_attributes.append(target_attr)
        return target_attributes
    
    def get_child_names_list(self, child_model, parent_id, child_col_of_parent_id):
        '''
        Gets names list of child objects, given that parent_id column exists in child table.

        For example, we can retrieve a list of all system names of associated project_id.

        child_col_of_parent_id is column name in child table that refers to parent_id.
        '''
        child_objs = self.model.get_objs_from_column_data(child_model, child_col_of_parent_id, parent_id)
        childs_names = []        
        for child_obj in child_objs:
            childs_names.append(child_obj.name)            
        return childs_names

    def get_child_ids_list(self, child_model, parent_id, child_col_of_parent_id):
        '''
        Gets ids list of child objects, given that parent_id column exists in child table.

        For example, we can retrieve a list of all system ids of associated project_id.

        child_col_of_parent_id is column name in child table that refers to parent_id.
        '''
        child_objs = self.model.get_objs_from_column_data(child_model, child_col_of_parent_id, parent_id)
        childs_ids = []
        for child_obj in child_objs:
            childs_ids.append(child_obj.id)
        return childs_ids
    
    def add_system_to_db(self, entry_widget):
        new_system = entry_widget.get()
        if new_system:
            proj_id = self.model.get_id_from_model_column_data(Project,'project_number', self.project_number)
            new_system_record = System(name=new_system, project_id=proj_id)
            self.model.add_record(new_system_record)
            self.model.commit_changes()
            return True
