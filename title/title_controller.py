from title.title_view import TitleView
from title.title_model import TitleModel, DwgTitle
from tkinter import messagebox
from class_collection import Controller
from model import Project, DwgTitle, DwgTitleDiagram, System, Diagram
import copy

class TitleController(Controller):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.model = TitleModel(self)
        self.diagram_options = self.model.diagram_options
        self.project_id = self.get_project_id()
        self.all_title_data_dict_list = self.fetch_all_title_data_dict()
        self.systems_list = self.get_systems_list()

        self.view = TitleView(f'{self.project_number} Title Manager', self.parent, self, project_number=self.project_number)
        self.view.initial_data_dict_list = self.get_all_data_from_widgets()


#####################################################################################

    def get_project_id(self):
        project_obj_list = self.model.get_rec_objs_by_opt_filts(Project, {'project_number': self.project_number})
        self.project_id = project_obj_list[0].id
        return self.project_id
    
    def fetch_all_title_data_dict(self):

        def fetch_title_table_dict_list():
            '''
            Fetches a list of dictionaries from the DwgTitle table using known project_id.
            Note: 'id' refers to id of the DwgTitle table. Returned list is sorted by 'dwgno'

            Returns:
            [
                {'id': 1, 'title': 'AHU Sequence (Page 1 of 3)', 'dwgno': 1, 'system_id': 1},
                                ...
                {'id': 12, 'title': 'VAV CONTROL PANEL (page 2 of 2)', 'dwgno': 12, 'system_id': 2}
                ]
            '''
            dwgtitle_table_dict_list = self.model.get_vals_from_rec_objs(DwgTitle,
                                                                        ['id', 'title', 'dwgno', 'system_id'],
                                                                        filters = {'project_id': self.project_id},
                                                                        sort_by='dwgno')
            return dwgtitle_table_dict_list
        
        dwgtitle_table_dict_list = fetch_title_table_dict_list()

        all_title_data_dict_list = []
        for dwgtitle_table_dict in dwgtitle_table_dict_list:
            all_title_data_dict = {}
            for key, value in dwgtitle_table_dict.items():
                if key == 'id':
                    all_title_data_dict = dwgtitle_table_dict.copy()
                    diagram_id_dict = self.model.get_vals_from_rec_objs(DwgTitleDiagram,
                                                                       ['diagram_id'],
                                                                       filters={'dwgtitle_id': value})[0]
                    all_title_data_dict['diagram_id'] = diagram_id_dict['diagram_id']
                    all_title_data_dict_list.append(all_title_data_dict)
        return all_title_data_dict_list

    def get_systems_list(self):
        systems_dict_list = self.model.get_vals_from_rec_objs(System, ['name'],
                                                             filters = {'project_id': self.project_id},
                                                             sort_by='name')
        systems_list = []
        for systems_dict in systems_dict_list:
            for values in systems_dict.values():
                systems_list.append(values)
        return systems_list

    def generate_all_title_data_dict(self):
        for all_title_data_dict in self.all_title_data_dict_list:
            yield all_title_data_dict

    def get_diagram_name_from_id(self, diagram_id):
        diagram_name = self.model.get_vals_from_rec_objs(Diagram, ['type'], filters = {'id': diagram_id})
        return diagram_name[0]['type']
    
    def get_dwgtitle_id_from_dwgno(self, dwgno):
        dwgtitle_id = self.model.get_rec_objs_by_opt_filts(DwgTitle, 
                                                    {'project_id': self.project_id,
                                                        'dwgno': dwgno})
        return dwgtitle_id[0].id

    def get_system_name_from_id(self, system_id):
        system_name = self.model.get_vals_from_rec_objs(System, ['name'], filters = {'id': system_id})
        return system_name[0]['name']

    def get_data_to_be_swapped(self, direction):

        def swap_contents(idx, direction):
            curr_title_data_obj_list = self.view.title_diagram_system_dwgno_list[idx]
            if direction == 'up':
                above_title_data_obj_list = self.view.title_diagram_system_dwgno_list[idx-1]
                return idx, curr_title_data_obj_list, above_title_data_obj_list
            else:
                below_title_data_obj_list = self.view.title_diagram_system_dwgno_list[idx+1]
                return idx, curr_title_data_obj_list, below_title_data_obj_list

        for idx, (title, diagram, system, _) in enumerate(self.view.title_diagram_system_dwgno_list):
            if self.view.active_data_widget == title or self.view.active_data_widget == diagram or self.view.active_data_widget == system:
                if direction == 'up':
                    if idx > 0:
                        idx, curr_title_data_obj_list, above_title_data_obj_list = swap_contents(idx, direction)
                        return idx, curr_title_data_obj_list, above_title_data_obj_list
                    else:
                        return None, None, None
                elif direction == 'down':
                    if idx < len(self.view.title_diagram_system_dwgno_list)-1:
                        idx, curr_title_data_obj_list, below_title_data_obj_list = swap_contents(idx, direction)
                        return idx, curr_title_data_obj_list, below_title_data_obj_list
                    else:
                        return None, None, None
                break

        return None, None, None
    
    def get_other_key_of_two_key_dict(self, known_key, dictionary):
        for key in dictionary.keys():
            if key != known_key:
                return key
            
    def get_all_data_from_widgets(self):
        '''
        Takes self.title_diagram_system_dwgno_list, which is a list of ALL entry/combobox/label widget objects,
        and returns a list of dictionaries such as {'dwgno': 10, 'title': 'VAV FLOW DIAGRAM'}.
        '''
        def loop_title_diagram_system_dwgno_list():
            for idx in range(len(self.view.title_diagram_system_dwgno_list)):
                for i in range(3):
                    target_widget = self.view.title_diagram_system_dwgno_list[idx][i]
                    yield target_widget
        
        def get_respective_dwgno_n_dwg_prop(widget):
            for item in self.view.title_diagram_system_dwgno_list:
                for i, dwg_prop in key_mapping.items():
                    if widget == item[i]:
                        dwgno = int(str(item[3].cget('text')).strip())
                        return dwgno, dwg_prop

        def get_dwgno_updated_widget_dict(target_widget):
            dwgno, dwg_prop = get_respective_dwgno_n_dwg_prop(target_widget)
            dwgno_updated_widget_dict = {'dwgno': dwgno, dwg_prop: target_widget.get()}
            return dwgno_updated_widget_dict
        
        key_mapping = {0: 'title', 1: 'diagram', 2: 'system'}
        dwgno_updated_widget_dict = {}
        list_to_update = []

        # Returns ex: {'dwgno': 5, 'title': 'AHU CONTROL PANEL (page 1 of 2)'}
        target_widgets = loop_title_diagram_system_dwgno_list()
        for target_widget in target_widgets:
            dwgno_updated_widget_dict = get_dwgno_updated_widget_dict(target_widget)
            list_to_update.append(dwgno_updated_widget_dict)

        return list_to_update

    def on_close_command(self):

        def generate_update_stack(final_data_dict_list):

            def handle_items_to_be_deleted(final_data_dict_list):
                '''
                Trims the final_data_dict_list to remove any blank titles.
                Appends any deleted items to the commit_stack_dict['delete'] list.
                '''

                def trim_final_data_dict_list(data):
                    if int(data['dwgno']) in blank_title_dwgno_list:
                            final_data_dict_list_trimmed.remove(data)

                def update_delete_commit_stack(data):
                    if data['dwgno'] in blank_title_dwgno_list and data['dwgno'] in [item['dwgno'] for item in self.view.initial_data_dict_list]:
                            if self.get_other_key_of_two_key_dict('dwgno', data) == 'title':
                                commit_stack_dict['delete'].append(data)

                blank_title_dwgno_list = []
                for data in reversed(final_data_dict_list):
                    if self.get_other_key_of_two_key_dict('dwgno', data) == 'title':
                        if data['title'] == '' or 'Filler for deleted' in data['title']:
                            blank_title_dwgno_list.append(data['dwgno'])
                        else:
                            break

                final_data_dict_list_trimmed = list(final_data_dict_list)

                for data in final_data_dict_list:
                    trim_final_data_dict_list(data)
                    update_delete_commit_stack(data)
                return final_data_dict_list_trimmed

            def get_update_data(final_data_dict_list_trimmed):
                for initial_dict, final_dict in zip(self.view.initial_data_dict_list, final_data_dict_list_trimmed):
                    if final_dict['dwgno'] == initial_dict['dwgno']:
                        initial_dict_other_key = self.get_other_key_of_two_key_dict('dwgno', initial_dict)
                        final_dict_other_key = self.get_other_key_of_two_key_dict('dwgno', final_dict)
                        if final_dict_other_key == initial_dict_other_key:
                            if final_dict[final_dict_other_key] != initial_dict[initial_dict_other_key]:
                                commit_stack_dict['update'].append(final_dict)                        
                
            def get_new_data(final_data_dict_list_trimmed):
                len_final = len(final_data_dict_list_trimmed)
                len_initial = len(self.view.initial_data_dict_list)
                if len_final > len_initial:
                    for i in range(len_initial, len_final):
                        commit_stack_dict['add'].append(final_data_dict_list_trimmed[i])

            # Initialize commit_stack_dict
            commit_stack_dict = {}
            commit_stack_dict['add'] = []
            commit_stack_dict['delete'] = []
            commit_stack_dict['update'] = []

            final_data_dict_list_trimmed = handle_items_to_be_deleted(final_data_dict_list)    

            if len(final_data_dict_list_trimmed) > len(self.view.initial_data_dict_list):
                # If final list is longer, then need to add and/or update
                get_update_data(final_data_dict_list_trimmed)
                get_new_data(final_data_dict_list_trimmed)
                
            elif len(final_data_dict_list_trimmed) < len(self.view.initial_data_dict_list) or len(final_data_dict_list_trimmed) == len(self.view.initial_data_dict_list):
                # If final list is shorter, then only need to update since delete already happened
                # If final list is same length as initial list, then only need to update
                get_update_data(final_data_dict_list_trimmed)

            return commit_stack_dict

        def validate_to_addupdate_data(commit_stack_dict):
            
            invalid_data_dict = {}
            invalid_data_dict['blank_title'] = []
            invalid_data_dict['empty_diagram'] = []
            invalid_data_dict['empty_system'] = []
            for data in commit_stack_dict['add'] + commit_stack_dict['update']:
                if self.get_other_key_of_two_key_dict('dwgno', data) == 'title':
                    if data['title'] == '':
                        invalid_data_dict['blank_title'].append(f'DWG {data['dwgno']}')
                    if data['title'] != '':
                        for diagram_system_dict in commit_stack_dict['add'] + commit_stack_dict['update']:
                            if diagram_system_dict['dwgno'] == data['dwgno'] and self.get_other_key_of_two_key_dict('dwgno', diagram_system_dict) == 'diagram':
                                if diagram_system_dict['diagram'] == '(None)':
                                    invalid_data_dict['empty_diagram'].append(f'DWG {data['dwgno']}')
                            elif diagram_system_dict['dwgno'] == data['dwgno'] and self.get_other_key_of_two_key_dict('dwgno', diagram_system_dict) == 'system':
                                if diagram_system_dict['system'] == '(None)':
                                    invalid_data_dict['empty_system'].append(f'DWG {data['dwgno']}')
                        
            blank_title_list = '\n'.join(invalid_data_dict['blank_title'])
            empty_diagram_list = '\n'.join(invalid_data_dict['empty_diagram'])
            empty_system_list = '\n'.join(invalid_data_dict['empty_system'])

            errors = []
            if invalid_data_dict['blank_title']:
                errors.append(f'\nThe following title(s) are blank:\n\n{blank_title_list}')
            if invalid_data_dict['empty_diagram']:
                errors.append(f'\nSelect a diagram for the following drawings:\n\n{empty_diagram_list}')
            if invalid_data_dict['empty_system']:
                errors.append(f'\nSelect a system for the following drawings:\n\n{empty_system_list}')

            if errors:
                messagebox.showerror('Invalid Entry', '\n\n'.join(errors), parent=self.view.root)
                return False
            else: return True

        def commit_to_database(commit_stack_dict):

            def get_system_id_from_name(system_name):
                system_id = self.model.get_rec_objs_by_opt_filts(System, 
                                                                {'project_id': self.project_id,
                                                                'name': system_name})
                return system_id[0].id

            def get_diagram_id_from_name(diagram_name):
                diagram_id = self.model.get_vals_from_rec_objs(Diagram, ['id'], filters = {'type': diagram_name})
                return diagram_id[0]['id']

            def add_commit(commit_stack_dict):

                def get_add_list(commit_stack_dict):
                    add_data_list = [] # List of dictionaries of dwgno,title,diagram,system to be added
                    for commit_action, data_dict_list in commit_stack_dict.items():
                        if commit_action == 'add':
                            for data_dict in data_dict_list:
                                    if not any(add_dict.get('dwgno') == data_dict['dwgno'] for add_dict in add_data_list):
                                        add_data_list.append(data_dict)
                                    else:
                                        for add_dict in add_data_list:
                                            if add_dict['dwgno'] == data_dict['dwgno']:
                                                other_data_dict_key = self.get_other_key_of_two_key_dict('dwgno', data_dict)
                                                add_dict[other_data_dict_key] = data_dict[other_data_dict_key]
                    return add_data_list

                def get_add_dwgtitle_obj_list(add_data_list):

                    add_dwgtitle_obj_list = []
                    for add_dict in add_data_list:
                        system_id = get_system_id_from_name(add_dict['system'])
                        add_dwgtitle_obj_list.append(DwgTitle(title = add_dict['title'],
                                                              dwgno = add_dict['dwgno'],
                                                              project_id = self.project_id,
                                                              system_id = system_id))
                    return add_dwgtitle_obj_list
   
                def get_add_dwgtitlediagram_obj_list(add_data_list):
                    # Add record to DwgTitleDiagram table after adding to DwgTitle table
                    add_dwgtitlediagram_obj_list = []
                    for add_dict in add_data_list:
                        diagram_id = get_diagram_id_from_name(add_dict['diagram'])
                        dwgtitle_id = self.get_dwgtitle_id_from_dwgno(add_dict['dwgno'])
                        add_dwgtitlediagram_obj_list.append(DwgTitleDiagram(dwgtitle_id = dwgtitle_id,
                                                                            diagram_id = diagram_id,))
                    return add_dwgtitlediagram_obj_list
                
                add_data_list = get_add_list(commit_stack_dict)

                add_dwgtitle_obj_list = get_add_dwgtitle_obj_list(add_data_list)
                for add_dwgtitle_obj in add_dwgtitle_obj_list:
                    self.model.add_record(add_dwgtitle_obj)

                add_dwgtitlediagram_obj_list = get_add_dwgtitlediagram_obj_list(add_data_list)
                for add_dwgtitlediagram_obj in add_dwgtitlediagram_obj_list:
                    self.model.add_record(add_dwgtitlediagram_obj)

            def update_commit(commit_stack_dict):

                def update_dwgtitle_table(dwgno, other_key, data_dict):
                    # Check list to see if dwgtitle object for that dwgno has already been queried
                    obj_here_dict = self.find_dict_with_key_value_from_list('dwgno', dwgno, dwgno_dwgtitleobj_dict_list)
                    if not obj_here_dict:
                        # Query the dwgtitle object
                        dwgtitle_obj = self.model.get_rec_objs_by_opt_filts(DwgTitle,
                                                                            {'dwgno' : dwgno,
                                                                                'project_id' : self.project_id})[0]   
                        # Add it to dwgno_dwgtitleobj_dict_list
                        dwgno_dwgtitleobj_dict_list.append({dwgno : dwgtitle_obj})
                        obj_here_dict = self.find_dict_with_key_value_from_list('dwgno', dwgno, dwgno_dwgtitleobj_dict_list)
                        
                    # Update the dwgtitle object
                    dwgtitle_obj = obj_here_dict[dwgno]
                    if other_key == 'title':
                        # Get the dwgtitle object and set the column of that object to the value
                        setattr(dwgtitle_obj, other_key, data_dict[other_key])
                    elif other_key == 'system':
                        # Get mapped system_id and set the column of that object to the system_id
                        system_id = get_system_id_from_name(data_dict[other_key])
                        setattr(dwgtitle_obj, 'system_id', system_id)

                def update_dwgtitlediagram_table(dwgno, other_key, data_dict):
                    # Get associated dwgtitlediagram object and set the column of that key to the value
                    dwgtitle_id = self.get_dwgtitle_id_from_dwgno(dwgno)
                    dwgtitlediagram_obj = self.model.get_rec_objs_by_opt_filts(DwgTitleDiagram, {'dwgtitle_id' : dwgtitle_id})[0]
                    diagram_id = int(get_diagram_id_from_name(data_dict[other_key]))
                    setattr(dwgtitlediagram_obj, 'diagram_id', diagram_id)

                # Loop through the update dictionary of the commit_stack_dict
                for commit_action, data_dict_list in commit_stack_dict.items():
                    if commit_action != 'update':
                        continue
                    for data_dict in data_dict_list:
                        dwgno = int(data_dict['dwgno'])
                        other_key = self.get_other_key_of_two_key_dict('dwgno', data_dict)

                        if other_key == 'diagram':
                            update_dwgtitlediagram_table(dwgno, other_key, data_dict)
                        else:
                            update_dwgtitle_table(dwgno, other_key, data_dict)

            def delete_commit(commit_stack_dict):
                delete_obj_list = []
                for commit_action, data_dict_list in commit_stack_dict.items():
                    if commit_action != 'delete':
                        continue
                    for data_dict in data_dict_list:
                        dwgno = int(data_dict['dwgno'])
                        dwgtitle_id = self.get_dwgtitle_id_from_dwgno(dwgno)
                        dwgtitle_obj = self.model.get_rec_objs_by_opt_filts(DwgTitle, {'id' : dwgtitle_id})[0]
                        delete_obj_list.append(dwgtitle_obj)
                    self.model.delete_record(delete_obj_list)

            add_commit(commit_stack_dict)
            update_commit(commit_stack_dict)
            delete_commit(commit_stack_dict)
            self.model.commit_changes()

        dwgno_dwgtitleobj_dict_list = [] # Store dwgno and respective dwgtitle object here to avoid multiple queries
        final_data_dict_list = self.get_all_data_from_widgets()
        commit_stack_dict = generate_update_stack(final_data_dict_list)
        if validate_to_addupdate_data(commit_stack_dict):
            commit_to_database(commit_stack_dict)
            return True
        else: 
            return False

#region title SCR script generator
    def write_text_style(self, font):
        return ["-style\n", f"{font}\n", '\n', '0\n', '\n', '\n', '\n', '\n','\n',]   

    def create_layout_title_start_coord_arr(self, number_of_titles):
        start_point = {}
        start_point['x'] = 0
        start_point['y'] = -1
        textbox_height = 0.5
        coord_dict = {}    
        for i in range(number_of_titles):
            coord_dict[i] = [start_point['x'], start_point['y'] - (i*textbox_height)]
        return coord_dict

    def create_layout_title_end_coord_arr(self, number_of_titles):
        end_point = {}
        end_point['x'] = 1.75
        end_point['y'] = -1.5
        textbox_height = 0.5
        coord_dict = {}    
        for i in range(number_of_titles):
            coord_dict[i] = [end_point['x'], end_point['y'] - (i*textbox_height)]
        return coord_dict    

    def populate_layout_titles(self, number_of_titles, titles_list):
        txt_height = 0.07
        start_coord_dict = self.create_layout_title_start_coord_arr(number_of_titles)
        end_coord_dict = self.create_layout_title_end_coord_arr(number_of_titles)
        lines = []
        for i in range(number_of_titles):        
            lines.append("-mtext\n")
            lines.append(f'{start_coord_dict[i][0]},{start_coord_dict[i][1]}\n')
            lines.append("justify\n")
            lines.append("mc\n")
            lines.append("style\n")
            lines.append("romand\n")
            lines.append("height\n")
            lines.append(f'{txt_height}\n')
            lines.append("columns\n")
            lines.append("no\n")
            lines.append(f'{end_coord_dict[i][0]},{end_coord_dict[i][1]}\n')
            lines.append(f'{titles_list[i]}\n')
            lines.append("\n")
        return lines

    def populate_cover_page_toc(self, number_of_titles, titles):    
        start_point1 = {}
        start_point1['x'] = 1.1
        start_point1['y'] = 5.68
        start_coord_offset = 9
        cutoff = 30
        lines = []
        lines = ["-mtext\n", f'{start_point1["x"]},{start_point1["y"]}\n', "justify\n",
                "TL\n", "style\n", "romand\n", "height\n", "0.1\n", "columns\n", "no\n",
                f'{start_point1["x"]+start_coord_offset},{start_point1["y"]-start_coord_offset}\n']
        if number_of_titles > cutoff: 
            for i in range(cutoff):
                lines.append(f'{i+1}. {titles[i]}\n')
        else:
            for i in range(number_of_titles):
                lines.append(f'{i+1}. {titles[i]}\n')
        lines.append("\n")
        
        if number_of_titles > cutoff:
            start_point2 = {}
            start_point2['x'] = start_point1['x']+6.4
            start_point2['y'] = start_point1['y']
            lines.extend(["-mtext\n", f'{start_point2["x"]},{start_point2["y"]}\n', "justify\n",
                            "TL\n", "style\n", "romand\n", "height\n", "0.1\n", "columns\n", "no\n",
                            f'{start_point2["x"]+start_coord_offset},{start_point2["y"]-start_coord_offset}\n'])
            for i in range(cutoff, number_of_titles):
                lines.append(f'{i+1}. {titles[i]}\n')
        lines.append("\n")    
        return lines

    def populate_titles_of_dwgs(self, number_of_titles, titles):
        lines = ["-layer\n", "N\n", "ToCSCR\n", "color\n", "40\n", "ToCSCR\n", "M\n", "ToCSCR\n", "\n"]
        start_coord = {}
        start_coord['x'] = 18 + 7.0685 #7.0685 is half the width of the dwg box
        start_coord['y'] = 10
        text_y_offset = 0.0732
        vertical_spacing = 12
        horizontal_spacing = 16
        sheet_width = 14.137
        text_height = 0.12
        j = 0
        for i in range(number_of_titles):
            if i % 10 == 0:
                lines.extend(['-text\n', 'justify\n', 'tc\n'])
                coord10_start = {}
                coord10_start['x'] = start_coord["x"]
                coord10_start['y'] = start_coord["y"] - (j*vertical_spacing) - text_y_offset
                lines.append(f'{coord10_start['x']}, {coord10_start['y']}\n')
                lines.append(f'{text_height}\n')
                lines.extend(['\n'])
                lines.extend([f'%%u{titles[i]}\n'])
                j += 1
            else:
                lines.extend(['-text\n', 'justify\n', 'tc\n'])
                coord_non10_start = {}
                coord_non10_start['x'] = start_coord["x"] + ((i - ((j - 1) * 10)) * horizontal_spacing)
                coord_non10_start['y'] = start_coord["y"] - ((j - 1) * vertical_spacing) - text_y_offset
                lines.extend(f'{coord_non10_start['x']}, {coord_non10_start['y']}\n')
                lines.append(f'{text_height}\n')
                lines.extend(['\n'])
                lines.extend([f'%%u{titles[i]}\n'])
        return lines

    def write_scr(self, project_number):        
        save_titles = messagebox.askyesno('Save Titles', 'Tiltes must be saved before generating SCR script.\nDo you want to save titles now?', parent=self.view.root)
        if save_titles == True:
            self.commit_titles(self.view.project_number)
            project_obj = self.get_project_object(project_number)
            titles_objs = self.get_title_object(project_obj) 
            titles_list = [title_object.title for title_object in titles_objs]
            number_of_titles = len(titles_list)
            scr_dict = {'init_properties' : ["osmode\n", "0\n", "-layer\n", "N\n", "ToCSCR\n", "color\n",
                                                "green\n", "ToCSCR\n", "M\n", "ToCSCR\n", "\n",],
                        'romand_text_style' : self.write_text_style('romand'),
                        'romans_text_style' : self.write_text_style('romans'),
                        'populate_layout_titles' : self.populate_layout_titles(number_of_titles, titles_list),
                        'populate_cover_page_toc' : self.populate_cover_page_toc(number_of_titles, titles_list),
                        'populate_titles_of_dwgs' : self.populate_titles_of_dwgs(number_of_titles, titles_list),
                        'final_properties' : ["osmode\n", "7335\n", "-layer\n", "set\n", "1-1\n", "\n",]
                        }

            scr_script = []
            scr_script = [item for sublist in scr_dict.values() for item in sublist]

            with open('SRC.src', 'w') as file:
                file.writelines(scr_script)
            self.view.root.focus_force()
#endregion