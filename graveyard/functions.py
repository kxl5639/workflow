#region [TitleView] This code checked against existing stack entries before adding.  
    # def update_commit_stack_dict_dict(self, updated_widget):     
        # key_mapping = {0: 'title', 1: 'diagram', 2: 'system'}
        # # From updated_widget, get the corresponding title_diagram_system_dict
        # dwgno_updated_widget_dict = {} # Returns ex: {'dwgno': 5, 'title': 'AHU CONTROL PANEL (page 1 of 2)'}

        # def get_dwgno_updated_widget_dict(updated_widget):
        #     for item in self.title_diagram_system_dwgno_list:
        #         for i, dwg_prop in key_mapping.items():
        #             if updated_widget == item[i]:
        #                 dwgno_updated_widget_dict = {'dwgno': int(str(item[3].cget('text')).strip()),
        #                                             dwg_prop: updated_widget.get()}
        #                 break
        #     return dwgno_updated_widget_dict
        
        # def get_other_key_of_two_key_dict(known_key, dictionary):
        #     for key, value in dictionary.items():
        #         if key != known_key:
        #             return key

        # # Returns ex: {'dwgno': 5, 'title': 'AHU CONTROL PANEL (page 1 of 2)'}
        # dwgno_updated_widget_dict = get_dwgno_updated_widget_dict(updated_widget)
        # # print(f'\n\n\nNEW {dwgno_updated_widget_dict = }')

        # # Check if list is empty
        # if not self.to_commit_stack_dict_dict:
        #     # print(f'STACK LIST IS EMPTY, ADDING: {dwgno_updated_widget_dict = }')
        #     self.to_commit_stack_dict_dict.append(dwgno_updated_widget_dict)
        #     # print(f'(List was empty so adding:  {self.to_commit_stack_dict_dict}')
        #     return
        
        # # to_commit_stack_dict_dict has entries so we will check against it with dwgno
        # for widget_update_stack_dict in self.to_commit_stack_dict_dict:
        #     if dwgno_updated_widget_dict['dwgno'] == widget_update_stack_dict['dwgno']:
        #         # print(f'{dwgno_updated_widget_dict = } ANDDD {widget_update_stack_dict = }')
        #         # print(f'{dwgno_updated_widget_dict["dwgno"] = } EQUALSSS {widget_update_stack_dict['dwgno'] = }')
        #         updated_widget_prop_key = get_other_key_of_two_key_dict('dwgno', dwgno_updated_widget_dict)
        #         stack_prop_key = get_other_key_of_two_key_dict('dwgno', widget_update_stack_dict)
        #         if updated_widget_prop_key == stack_prop_key:
        #             # print(f'(matching {updated_widget_prop_key = })')
        #             if dwgno_updated_widget_dict[updated_widget_prop_key] != widget_update_stack_dict[updated_widget_prop_key]:
        #                 # print(f"{dwgno_updated_widget_dict[updated_widget_prop_key] = } DOESNT MATCH {widget_update_stack_dict[updated_widget_prop_key] = }\nSO WE POP {self.to_commit_stack_dict_dict.index(widget_update_stack_dict) = } AND ADD 'dwgno': {dwgno_updated_widget_dict['dwgno']}, 'updated_widget_prop_key': {dwgno_updated_widget_dict[updated_widget_prop_key]}")
        #                 self.to_commit_stack_dict_dict.pop(self.to_commit_stack_dict_dict.index(widget_update_stack_dict))
        #                 self.to_commit_stack_dict_dict.append({'dwgno': dwgno_updated_widget_dict['dwgno'],
        #                                                         updated_widget_prop_key: dwgno_updated_widget_dict[updated_widget_prop_key]})
        #                 # print(f'(There were changes made:    {self.to_commit_stack_dict_dict}')
        #                 return
        #             else:
        #                 # print(f'(There were NO changes made: {self.to_commit_stack_dict_dict}') 
        #                 # print(f"{dwgno_updated_widget_dict[updated_widget_prop_key] = } EQUALS {widget_update_stack_dict[updated_widget_prop_key] = } SO WE DO NOTHING")
        #                 return
        # # print(f'New entry to stack: {dwgno_updated_widget_dict = }')
        # self.to_commit_stack_dict_dict.append(dwgno_updated_widget_dict)     
        # # print(f'(New entry added to stack:   {self.to_commit_stack_dict_dict}')
    #endregion       