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

    def add_record(self, record_obj):
        session.add(record_obj)

    def commit_changes(self):
        session.commit()

    def _remove_end_blanks(self, list_obj):
        '''Remove blank items at the end of a list. Retains blank items in middle of list.'''        
        # Check if the last item is a blank
        if list_obj and list_obj[-1] != '':
            print(f'\nLast object not blank: {list_obj}')
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
        print(f'\nModified list: {modified_list}')
        return modified_list, removed_indices