from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetail_model import ProjectDetailModel
from model import session, Project, SystemDevice, System, Device

class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.model = ProjectDetailModel(self, project_number)
        self.parent = parent
        self.project_number = project_number
        self.view = ProjectDetailWindow(f'{project_number} Project Detail',
                                        parent, self, project_number)
    
    def get_systems_names_ids_list(self):
        proj_id = self.model.get_id_from_model_column_data(Project, 'project_number', self.project_number)
        systems_names = self.get_child_names_list(System, proj_id, 'project_id')
        systems_ids = self.get_child_ids_list(System, proj_id, 'project_id')
        return systems_names, systems_ids

    def get_devices_ids_list(self, system_id):
        systemdevices_ids = self.get_child_ids_list(SystemDevice, system_id, 'system_id')
        devices_ids = []
        for systemdevice_id in systemdevices_ids:
            device_id = self.model.get_target_col_val_by_known_col_val(SystemDevice,'id', systemdevice_id, 'device_id')
            devices_ids.append(device_id)
        devices_names = []
        for device_id in devices_ids:
            device_name = self.model.get_target_col_val_by_known_col_val(Device,'id',device_id,'name')
            devices_names.append(device_name)
        return devices_names, devices_ids
    
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
    