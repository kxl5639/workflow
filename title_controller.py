from title_view import TitleView
from title_model import TitleModel, DwgTitle

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
    
    def update_new_page_title_dict(self):
        entry_widget_list = self.view.get_all_entry_widgets(self.view.root)
        new_titles, removed_indices = self.model._remove_end_blanks([title.get() for title in entry_widget_list])    
        pages_to_be_deleted_from_screen = [item+1 for item in removed_indices]
        new_page_title_dict = {idx+1: title for idx, title in enumerate(new_titles)} 
        return new_page_title_dict, pages_to_be_deleted_from_screen
    
    def commit_titles(self, project_number): 

        project_obj = self.get_project_object(project_number)
        existing_title_record_objs = self.get_title_object(project_obj)        
        new_page_title_dict, pages_to_be_deleted_from_screen = self.update_new_page_title_dict()
        existing_page_titleobj_dict = {existing_title_record_objs.index(title_obj)+1 : title_obj for title_obj in existing_title_record_objs}
        
        # Destroy the end title entry widgets that are blank (view)
        if pages_to_be_deleted_from_screen != []:
            self.view.destroy_frames_if_labels_match(pages_to_be_deleted_from_screen)
            new_page_title_dict, pages_to_be_deleted_from_screen = self.update_new_page_title_dict()            
            print(f'\nNew page title dict: {new_page_title_dict.items()}')

        # Get list of title objects to be deleted as well as entry widgets that need to be popped
        title_record_obj_to_delete = []
        for existing_page_number in list(existing_page_titleobj_dict.keys()):
            if existing_page_number not in new_page_title_dict:
                title_record_obj_to_delete.append(existing_page_titleobj_dict[existing_page_number])
                existing_page_titleobj_dict.pop(existing_page_number)
        
        # Delete records from table (model)
        self.model.delete_record(title_record_obj_to_delete)
        
        # Continue to update/add new title records(model)
        for new_page_number, new_title_name in new_page_title_dict.items():
            if new_page_number in existing_page_titleobj_dict:
                # This page already exist. We are just updating the existing title name
                existing_page_titleobj_dict[new_page_number].title = new_title_name
                # print(f'DWG-{new_page_number}: {existing_page_titleobj_dict[new_page_number].title} --> {new_title_name}')
            else:
                # This is a new page that we are adding
                # print(f'DWG-{new_page_number} title to be added: {new_title_name}')
                new_title_record = DwgTitle(dwgno=new_page_number, title = new_title_name, project_id=project_obj.id)
                self.model.add_record(new_title_record)

        # Commit changes
        self.model.commit_changes()
#endregion
    