from title_view import TitleView
from title_model import TitleModel

class TitleController:
    def __init__(self, parent=None, project_number=None) -> None:
        self.parent = parent
        self.project_number = project_number
        self.view = TitleView('Title Manager', self.parent, self, project_number=None)
        self.model = TitleModel()

#region View
    def add_entry(self, parent):
        self.view.create_entry_widget(parent)

    def moveup_entry(self):
        self.view.move_entry('up')

    def movedown_entry(self):
        self.view.move_entry('down')
    
    def on_project_combobox_selected(self):
        self.view.on_project_selected()
#endregion

#region Model
    def get_project_object(self, project_number):
        return self.model.get_project_object(project_number)
    
    def get_title_object(self, project_object):
        return self.model.get_title_object(project_object)
    
    def commit_titles(self, project_number, entry_widget_list):
        self.model.commit_titles(project_number, entry_widget_list)
#endregion
    