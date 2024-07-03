from projectlistwindow_view import ProjectListWindow
from projectlistwindow_model import ProjectListWindowModel

class ProjectListWindowController:
    def __init__(self, parent=None) -> None:
        self.parent = parent        
        self.model = ProjectListWindowModel()
        self.column_map = self.model.colump_map
        self.table_data = self.model.table_data
        self.view = ProjectListWindow(title = 'Projects List', parent=self.parent, controller = self)
        
        
        