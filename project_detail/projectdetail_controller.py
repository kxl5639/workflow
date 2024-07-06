from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetail_model import ProjectDetailModel
from model import session, Project, SystemDevice, System

class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.model = ProjectDetailModel(self, project_number)
        self.parent = parent
        self.project_number = project_number
        self.view = ProjectDetailWindow(f'{project_number} Project Detail',
                                        parent, self, project_number)
    
    def get_systems_names_ids_list(self):
        proj_id = self.model.get_id_from_model_column_data(Project,
                                                           'project_number',
                                                           self.project_number)
        systems_names = self.get_child_name_list(System,
                                                proj_id,
                                                'project_id',)
        systems_ids = self.get_child_id_list(System,
                                             proj_id,
                                             'project_id',)
        return systems_names, systems_ids

    def get_devices_ids_list(self, system_id):
        devices_ids = self.get_child_id_list(SystemDevice,
                                        system_id,
                                        'system_id',)
        return devices_ids
    
    def get_child_name_list(self, child_model, parent_id, parent_col_id_name):
        child_objs = self.model.get_objs_from_column_data(child_model,
                                                          parent_col_id_name,
                                                          parent_id)
        childs_names = []        
        for child_obj in child_objs:
            childs_names.append(child_obj.name)            
        return childs_names

    def get_child_id_list(self, child_model, parent_id, parent_col_id_name):
        child_objs = self.model.get_objs_from_column_data(child_model,
                                                          parent_col_id_name,
                                                          parent_id)
        childs_ids = []
        for child_obj in child_objs:
            childs_ids.append(child_obj.id)
        return childs_ids
    