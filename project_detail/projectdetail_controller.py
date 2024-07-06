from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetail_model import ProjectDetailModel
from model import session, Project, SystemDevice, System, Device

class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.parent = parent
        self.project_number = project_number
        self.max_device_data_char_dict = {}
        self.systems_devices_data_dict = {}
        self.model = ProjectDetailModel(self, project_number)
        self.view = ProjectDetailWindow(f'{project_number} Project Detail',
                                        parent, self, project_number)
    
    def get_systems_names_ids_list(self):
        proj_id = self.model.get_id_from_model_column_data(Project, 'project_number', self.project_number)
        systems_names = self.get_child_names_list(System, proj_id, 'project_id')        
        systems_ids = self.get_child_ids_list(System, proj_id, 'project_id')
        return systems_names, systems_ids

    def get_max_devices_data_char(self, systems_devices_data_dict, system_key):
        system_id = system_key[0]
        for cat in systems_devices_data_dict[system_id].keys():
            if cat not in self.max_device_data_char_dict:
                self.max_device_data_char_dict[cat] = 0
            for next in systems_devices_data_dict[system_id][cat]['data']:
                if cat == 'devices_qtys':
                    self.max_device_data_char_dict[cat] = 4
                else:
                    if len(next) > self.max_device_data_char_dict[cat]:
                        self.max_device_data_char_dict[cat] = len(next)
    
    def get_systems_devices_data(self):
        # Gets all systems keys of the project number
        systems_keys = self.get_systems_keys()
        # Gets all the device data (tag, desc, manf, etc...) for each system_key
            # Also gets the max character length for each device data
        for system_key in systems_keys:
            self.get_devices_data(system_key[0])
            self.get_max_devices_data_char(self.systems_devices_data_dict, system_key)
        # Update max char for each systems_devices_data_dict
        for system_key in systems_keys:
            system_id = system_key[0]
            for device_prop_key in self.systems_devices_data_dict[system_id]:
                self.systems_devices_data_dict[system_id][device_prop_key]['max_char']=self.max_device_data_char_dict[device_prop_key]
        print(f'\n{self.systems_devices_data_dict[1]}')
        print(f'\n{self.systems_devices_data_dict[2]}')

    def get_systems_keys(self):
        '''Generates the key as a tuple [ex: (1, 'AHU')] for self.systems_devices_data_dict.'''
        systems_ids = self.get_systems_ids_from_proj_num()
        systems_names = []
        systems_keys = []
        for idx, system_id in enumerate(systems_ids):
            system_obj = self.model.get_objs_from_column_data(System,'id',system_id)
            system_name = system_obj[0].name
            systems_keys.append((system_id, system_name))
        print(f'\nsystem keys: {systems_keys}')
        return systems_keys

    def get_systems_ids_from_proj_num(self):
        proj_id = self.model.get_id_from_model_column_data(Project, 'project_number', self.project_number)
        systems_objs = self.model.get_objs_from_column_data(System, 'project_id', proj_id)
        systems_ids = []
        for system_obj in systems_objs:
            systems_ids.append(system_obj.id)
        return systems_ids

    def get_devices_data(self, system_id):
            systemdevices_ids = self.get_child_ids_list(SystemDevice, system_id, 'system_id')
            devices_ids = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'device_id')
            devices_tags = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'tag')
            devices_qtys = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'qty')
            devices_descs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'description')
            devices_manfs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'manufacturer')
            devices_models = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'model')
            self.systems_devices_data_dict[system_id] = {'devices_tags' : {'data':devices_tags, 'max_char':0},
                                                         'devices_qtys' : {'data':devices_qtys, 'max_char':0},
                                                          'devices_descs' : {'data':devices_descs, 'max_char':0},
                                                          'devices_manfs' : {'data':devices_manfs, 'max_char':0},
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
    