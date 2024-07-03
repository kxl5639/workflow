from projectlistwindow_model import ProjectListWindowModel
from projectlistwindow_view import ProjectAddModifyWindow
from project.project_view import open_add_project_window, open_delete_project_window, open_modify_project_window
from view import ListWindow

class ProjectListWindowController:
    def __init__(self, parent=None) -> None:
        self.parent = parent        
        self.model = ProjectListWindowModel()
        self.column_map = self.model.colump_map
        self.table_data = self.model.table_data
        self.button_info = [("Add", lambda: ProjectAddModifyWindow(title='Add New Project', parent=self.view)),
                    ("Modify", None),
                    ("Delete", None)]        
        # self.button_info = [("Add", lambda: open_add_project_window(self.parent)),
        #                     ("Modify", lambda: open_modify_project_window(self.parent)),
        #                     ("Delete", lambda: open_delete_project_window(self.parent))]        
        self.view = ListWindow(title = 'Projects List', parent=self.parent, controller=self)
        
        
        