from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetail_model import ProjectDetailModel
from model import session, Project, System

class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.model = ProjectDetailModel(self, project_number)
        self.parent = parent
        self.project_number = project_number
        self.view = ProjectDetailWindow(f'{project_number} Project Detail',
                                        parent, self, project_number)
    
    def get_systems_list(self):        
        proj_id = self.model.get_id_from_model_column_data(Project,
                                                           'project_number',
                                                           self.project_number)
        system_objs = self.model.get_objs_from_column_data(System,
                                                     'project_id',
                                                     proj_id)
        system_names = []
        for system_obj in system_objs:
            system_names.append(system_obj.name)
        return system_names
        

    
        