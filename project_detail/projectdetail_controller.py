from project_detail.projectdetail_view import ProjectDetailWindow
class ProjectDetailController:
    def __init__(self, parent, project_number) -> None:
        self.parent = parent
        self.project_number = project_number
        self.view = ProjectDetailWindow('Project Detail', parent, project_number)