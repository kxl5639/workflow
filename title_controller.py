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
        project_obj = self.get_project_object(project_number)
        existing_title_objs = self.get_title_object(project_obj)
        existing_titles = [title_object.title for title_object in existing_title_objs]        
        new_titles, removed_indices = self.model._remove_end_blanks([title.get() for title in entry_widget_list])        
        to_be_deleted_pages = [item+1 for item in removed_indices]
        existing_page_titleobj_dict = {existing_title_objs.index(title_obj)+1 : title_obj for title_obj in existing_title_objs}
        new_page_title_dict = {new_titles.index(title)+1 : title for title in new_titles}

        # Destroy the end title entry widgets that are blank (view)
        print(f'new titles: {new_titles}')
        print(f'pages to be deleted: {to_be_deleted_pages}')
        self.view.destroy_frames_if_labels_match(to_be_deleted_pages)

        # Get list of title objects to be deleted as well as entry widgets that need to be popped
        title_obj_to_delete = []
        
        for existing_page_number, existing_title_obj in existing_page_titleobj_dict.items():
            if existing_page_number not in new_page_title_dict:
                title_obj_to_delete.append(existing_title_obj)                  
        
        # # Delete records from table (model)
        
        # # Pop those entry frames (view)
        # # Continue to update/add new title records(model)
        
#endregion
    