from model import session, Project, System, SystemDevice
from class_collection import Model

class ProjectDetailModel(Model):
    def __init__(self, project_number, controller=None) -> None:
        super().__init__(controller)
        self.project_number = project_number
    