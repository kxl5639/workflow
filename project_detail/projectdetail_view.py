from class_collection import BaseWindow

class ProjectDetailWindow(BaseWindow):
    def __init__(self, title, parent, project_number, is_root=False):
        super().__init__(title, parent, is_root)
        self.project_number = project_number

        

        BaseWindow.center_window(self.root)