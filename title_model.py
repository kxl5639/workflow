from model import session, Project, DwgTitle

class TitleModel:

    def get_project_object(self, project_number):
        return session.query(Project).filter_by(project_number=project_number).first()
        
    def get_title_object(self, project_object):
        '''RETURNED TITLE OBJECT LIST IS SORTED BY DRAWING NUMBER'''
        return session.query(DwgTitle).filter_by(project_id=project_object.id).order_by(DwgTitle.dwgno).all() 
    

    def delete_title_record(self, existing_page_titleobj_dict, new_page_title_dict):
        for existing_page_number, existing_title_obj in existing_page_titleobj_dict.items():
            if existing_page_number not in new_page_title_dict:
                print(f'{existing_title_obj.title} to be deleted')
                session.delete(existing_title_obj)

    def delete_record(self, object_list):
        for obj in object_list:
            session.delete(obj)

    def commit_changes(self):
        session.commit()

    def commit_titles(self, project_number, entry_widget_list):        
        project_obj = self.get_project_object(project_number)
        existing_title_objs = self.get_title_object(project_obj)
        existing_titles = [title_object.title for title_object in existing_title_objs]        
        new_titles = self._remove_end_blanks([title.get() for title in entry_widget_list])        
        existing_page_titleobj_dict = {existing_title_objs.index(title_obj)+1 : title_obj for title_obj in existing_title_objs}
        new_page_title_dict = {new_titles.index(title)+1 : title for title in new_titles}
        print('******************************\n')
        for existing_page_number, existing_title_obj in existing_page_titleobj_dict.items():
            if existing_page_number not in new_page_title_dict:
                print(f'{existing_title_obj.title} to be deleted')
                session.delete(existing_title_obj)
        print('\n')
        for new_page_number, new_title_name in new_page_title_dict.items():            
            if new_page_number in existing_page_titleobj_dict:
                # This page already exist. We are just updating the existing title name
                existing_page_titleobj_dict[new_page_number].title = new_title_name
                print(f'DWG-{new_page_number}: {existing_page_titleobj_dict[new_page_number].title} --> {new_title_name}')
            else:
                # This is a new page that we are adding
                print(f'DWG-{new_page_number} title to be added: {new_title_name}')
                new_title_record = DwgTitle(dwgno=new_page_number, title = new_title_name, project_id=project_obj.id)
                session.add(new_title_record)
        session.commit()    
        

    def _remove_end_blanks(self, list_obj):
        '''Remove blank items at the end of a list. Retains blank items in middle of list.'''
        
        # Check if the last item is a blank
        if list_obj and list_obj[-1] != '':
            return list_obj, []  # If the last item is not a blank, return the original list and an empty list of removed indices
        
        # Find the first non-blank item from the end of the list
        last_non_blank_index = len(list_obj)
        
        for index in range(len(list_obj) - 1, -1, -1):
            if list_obj[index] != '':
                last_non_blank_index = index + 1
                break
        
        # Calculate the indices of the removed blank items
        removed_indices = list(range(last_non_blank_index, len(list_obj)))
        
        # Slicing to remove trailing blanks
        modified_list = list_obj[:last_non_blank_index]        
        
        return modified_list, removed_indices