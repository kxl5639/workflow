import tkinter as tk
from tkinter import ttk, font, messagebox
from class_collection import View, ButtonsFrame

class TitleView(View):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.initiate_testing_values(0)
        # self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.resizable(width=True, height=True)
        self.project_number = project_number
        self.title_column_break = 30
        self.header_font = font.Font(family="Helvetica", size=9, weight="bold")
        self.title_col_frames_list = []
        self.title_diagram_system_dwgno_list = []
        self.active_data_widget = None
        self.final_data_dict_list = []
        self.update_stack_dict_list = []
        
        self.create_project_number_frame()
        self.create_and_populate_titles_frame()
        self.create_right_toolbar_frame()
        self.initial_data_dict_list = []
        self.initial_data_dict_list = self.get_all_data_from_widgets()

        self.close_frame = ButtonsFrame(self.base_frame, [('Close', self.on_close)])
        self.close_frame.button_frame.grid(row=10, column=10, padx=10, pady=10, sticky='nsew')
        self.center_window(self.root)

#####################################################################################

############################## Frame Structure ###############################
#                                                                            #
#  base_frame [-> titles_frame -> [ -> title_col_frame - > title_data_frame] #
#                                   ...                                      #
#                                   -> title_col_frame - > title_data_frame] #
#              -> project_number_frame]                                      #
#              -> right_toolbar_frame [-> menu_frame]                        #
#                                      -> autocad_scr_frame]                 #
#                                                                            # 
##############################################################################
    
    def on_close(self):

        # Get data from all widgets on close
        self.final_data_dict_list = self.get_all_data_from_widgets()

        # Generate update stack
        self.controller.generate_update_stack()
        print(self.update_stack_dict_list)

        self.root.destroy()

        
    def get_other_key_of_two_key_dict(self, known_key, dictionary):
        for key in dictionary.keys():
            if key != known_key:
                return key

    def create_project_number_frame(self):
        project_number_frame = self.create_frame(self.base_frame, 0, 0,
                                                 padx=0, pady=(0,10), sticky='nsew',
                                                 relief = self.relief)
        
        self.create_label(project_number_frame, f'EM: {self.project_number}',
                          0, 0, padx=0, pady=0,
                          sticky='w', relief=self.relief)
    
    def calc_col_row_for_pop_title_data_frame(self, dwgno):
        if dwgno % self.title_column_break == 0:
            in_column = dwgno // self.title_column_break -1
            in_row = self.title_column_break
        else:
            in_column = dwgno // self.title_column_break
            in_row = dwgno - (in_column*self.title_column_break)

        return in_row, in_column

    def create_and_populate_titles_frame(self):

        def create_titles_frame():
            self.titles_label_frame = self.create_label_frame(self.base_frame, 'Titles', 1, 0,
                                                    padx=(0,10),pady=0,sticky='nsew',
                                                    relief=self.relief)
            return self.titles_label_frame
        
        # Create titles frame
        self.titles_label_frame = create_titles_frame()

        # Populate titles frame
        all_title_data_dict_generator = self.controller.generate_all_title_data_dict()
        for title_data_dict in all_title_data_dict_generator:

            # Unpack data from title_data_dict
            dwgno = title_data_dict['dwgno']
            title = title_data_dict['title']
            diagram_id = title_data_dict['diagram_id']
            diagram_name = self.controller.get_diagram_name_from_id(diagram_id)
            system_id = title_data_dict['system_id']
            system_name = self.controller.get_system_name_from_id(system_id)

            # Calculate column and row based on self.title_column_break
            in_row, in_column = self.calc_col_row_for_pop_title_data_frame(dwgno)

            self.create_n_pop_title_col_frame(in_row, in_column, dwgno, title, diagram_name, system_name)

    def get_all_data_from_widgets(self):
        '''
        Takes self.title_diagram_system_dwgno_list, which is a list of ALL entry/combobox/label widget objects,
        and returns a list of dictionaries such as {'dwgno': 10, 'title': 'VAV FLOW DIAGRAM'}.
        '''
        def loop_title_diagram_system_dwgno_list():
            print(self.title_diagram_system_dwgno_list)
            for idx in range(len(self.title_diagram_system_dwgno_list)):
                for i in range(3):
                    target_widget = self.title_diagram_system_dwgno_list[idx][i]
                    yield target_widget
        
        def get_respective_dwgno_n_dwg_prop(widget):
            for item in self.title_diagram_system_dwgno_list:
                for i, dwg_prop in key_mapping.items():
                    if widget == item[i]:
                        dwgno = int(str(item[3].cget('text')).strip())
                        # print(f'dwgno: {dwgno}, dwg_prop: {dwg_prop}')
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

        

    def create_n_pop_title_col_frame(self, in_row, in_column, dwgno, title, diagram_name, system_name):
        #region Functions
        def create_title_col_frame(cidx):
            if cidx == 0: xpad = 10
            else: xpad = (0,10)
            title_col_frame = self.create_frame(self.titles_label_frame, 0, cidx,
                                                padx=xpad, pady=10, sticky='nsew',
                                                relief='solid')
            return title_col_frame

        def create_title_header_frame(parent):
            widgets = [
                self.create_label(parent, 'Title', 0, 1, (0,10), (0,5), sticky='nsew'),
                self.create_label(parent, 'Diagram', 0, 2, (0,10), (0,5), sticky='nsew'),
                self.create_label(parent, 'System', 0, 3, 0, (0,5), sticky='nsew')
            ]
            for widget in widgets:
                widget.config(font=self.header_font, relief=self.relief, anchor='center')

        def create_title_data_frame(ridx, dwgno, title, diagram_name, system_name):

            def get_active_data_widget(data_widget):
                self.active_data_widget = data_widget
                for lst in self.title_diagram_system_dwgno_list:
                    if data_widget in lst:
                        lst[3].config(font=self.header_font)
                    else:
                        lst[3].config(font='')

            def create_title_entry(parent, ridx):
                title_entry = self.create_entry_widget(parent, ridx, 1, (0,10), 0)
                title_entry.insert(0, title)
                title_entry.config(width = 50)
                title_entry.bind("<FocusIn>", lambda event: get_active_data_widget(title_entry))
                return title_entry

            def create_diagram_combo(parent, ridx):
                diagram_combo = self.create_combobox(parent, ridx, 2, (0,10), 0, state='readonly')
                diagram_combo.set(diagram_name)
                diagram_combo.config(values=self.controller.diagram_options,
                                    width=max(len(option) for option in self.controller.diagram_options))
                diagram_combo.bind("<FocusIn>", lambda event: get_active_data_widget(diagram_combo))
                return diagram_combo

            def create_system_combo(parent, ridx):
                system_combo = self.create_combobox(parent, ridx, 3, 0, 0, state='readonly')
                system_combo.set(system_name)
                system_combo.config(values=self.controller.systems_list,
                                    width=max(len('system'), max(len(option) for option in self.controller.systems_list)))
                system_combo.bind("<FocusIn>", lambda event: get_active_data_widget(system_combo))
                return system_combo

            if ridx == 1:
                ypad = 10
            else:
                ypad = (0,10)
            title_data_frame = self.create_frame(self.title_col_frames_list[-1],
                                                 ridx, 0, 10, ypad, relief=self.relief)
            
            if ridx == 1: create_title_header_frame(title_data_frame)
            
            if 1 <= dwgno <= 9: clean_dwgno = f'  {dwgno}'
            else: clean_dwgno = (dwgno)
            dwgno_label = self.create_label(title_data_frame, clean_dwgno, ridx, 0, (0,5), 0)

            title_entry = create_title_entry(title_data_frame, ridx)
            diagram_combo = create_diagram_combo(title_data_frame, ridx)
            system_combo = create_system_combo(title_data_frame, ridx)
            self.title_diagram_system_dwgno_list.append([title_entry, diagram_combo, system_combo, dwgno_label])
        #endregion

        if int(in_row) == 1:
            title_col_frame = create_title_col_frame(in_column)
            self.title_col_frames_list.append(title_col_frame)
        
        create_title_data_frame(in_row, dwgno, title, diagram_name, system_name)
        
    def create_right_toolbar_frame(self):
        def create_menu_frame():
            menu_frame = self.create_label_frame(right_toolbar_frame, 'Menu', 0, 0,
                                        padx=0,pady=(0,10),sticky='nsew',
                                        relief=self.relief)
            return menu_frame
        
        def create_autocad_src_frame():
            scr_frame = self.create_label_frame(right_toolbar_frame, 'AutoCAD SCR', 1, 0,
                                        padx=0,pady=0,sticky='nsew',
                                        relief=self.relief)
            return scr_frame

        def add_title_btn_cmd(): 
            # See how many title_data_frames there are
            new_dwgno = len(self.title_diagram_system_dwgno_list)

            # Calculate next row and column
            in_row, in_column = self.calc_col_row_for_pop_title_data_frame(new_dwgno+1)

            # Create new title_data_frame
            self.create_n_pop_title_col_frame(in_row, in_column, new_dwgno+1, '', '', '')
            self.center_window(self.root)
            

        def move_btn_cmd(direction):
            
            idx, curr_title_data_obj_list, swap_title_data_obj_list = self.controller.get_data_to_be_swapped(direction)
            if idx is not None:
                # Upack data to prevent overwriting during swap
                curr_title = curr_title_data_obj_list[0].get()
                curr_diagram = curr_title_data_obj_list[1].get()
                curr_system = curr_title_data_obj_list[2].get()
                swap_title = swap_title_data_obj_list[0].get()
                swap_diagram = swap_title_data_obj_list[1].get()
                swap_system = swap_title_data_obj_list[2].get()

                # Set index depending on direction
                if direction == 'up':
                    idx_new = idx-1
                else:
                    idx_new = idx+1

                # Perform swap
                self.title_diagram_system_dwgno_list[idx][0].delete(0, tk.END)
                self.title_diagram_system_dwgno_list[idx][0].insert(0, swap_title)
                self.title_diagram_system_dwgno_list[idx][1].set(swap_diagram)
                self.title_diagram_system_dwgno_list[idx][2].set(swap_system)

                self.title_diagram_system_dwgno_list[idx_new][0].delete(0, tk.END)
                self.title_diagram_system_dwgno_list[idx_new][0].insert(0, curr_title)
                self.title_diagram_system_dwgno_list[idx_new][1].set(curr_diagram)
                self.title_diagram_system_dwgno_list[idx_new][2].set(curr_system)

                # set focus back on active_data_widget
                self.active_data_widget = self.title_diagram_system_dwgno_list[idx_new][0]
                self.active_data_widget.focus_set()
            else:
                if self.active_data_widget:
                    self.active_data_widget.focus_set()

        def scr_btn_cmd(self):
            pass
        
        right_toolbar_frame = self.create_frame(self.base_frame, 1, 1,
                                                 padx=0,pady=0,sticky='nsew',
                                                 relief=self.relief)
        menu_frame = create_menu_frame()
        
        add_title_button = ButtonsFrame(menu_frame, [('(+) Title', lambda:add_title_btn_cmd())])
        add_title_button.button_frame.grid(row=0, column=0, padx=(10,10), pady=10, sticky='nsew')

        moveup_button = ButtonsFrame(menu_frame, [('Move Up', lambda:move_btn_cmd('up'))])
        moveup_button.button_frame.grid(row=1, column=0, padx=(10,10), pady=(0,10), sticky='nsew')
        
        movedown_button = ButtonsFrame(menu_frame, [('Move Down', lambda:move_btn_cmd('down'))])
        movedown_button.button_frame.grid(row=2, column=0, padx=(10,10), pady=(0,10), sticky='nsew')

        autocad_src_frame = create_autocad_src_frame()

        scr_button = ButtonsFrame(autocad_src_frame, [('Write SCR', lambda:scr_btn_cmd())])
        scr_button.button_frame.grid(row=0, column=0, padx=(10,10), pady=(10), sticky='nsew')

    def initiate_testing_values(self, testing):
        if testing == 0:
            self.relief = None
        else:
            self.relief = 'solid'

        #region This code checked against existing stack entries before adding.  
    # def update_update_stack_dict_list(self, updated_widget):     
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
        # if not self.to_update_stack_dict_list:
        #     # print(f'STACK LIST IS EMPTY, ADDING: {dwgno_updated_widget_dict = }')
        #     self.to_update_stack_dict_list.append(dwgno_updated_widget_dict)
        #     # print(f'(List was empty so adding:  {self.to_update_stack_dict_list}')
        #     return
        
        # # to_update_stack_dict_list has entries so we will check against it with dwgno
        # for widget_update_stack_dict in self.to_update_stack_dict_list:
        #     if dwgno_updated_widget_dict['dwgno'] == widget_update_stack_dict['dwgno']:
        #         # print(f'{dwgno_updated_widget_dict = } ANDDD {widget_update_stack_dict = }')
        #         # print(f'{dwgno_updated_widget_dict["dwgno"] = } EQUALSSS {widget_update_stack_dict['dwgno'] = }')
        #         updated_widget_prop_key = get_other_key_of_two_key_dict('dwgno', dwgno_updated_widget_dict)
        #         stack_prop_key = get_other_key_of_two_key_dict('dwgno', widget_update_stack_dict)
        #         if updated_widget_prop_key == stack_prop_key:
        #             # print(f'(matching {updated_widget_prop_key = })')
        #             if dwgno_updated_widget_dict[updated_widget_prop_key] != widget_update_stack_dict[updated_widget_prop_key]:
        #                 # print(f"{dwgno_updated_widget_dict[updated_widget_prop_key] = } DOESNT MATCH {widget_update_stack_dict[updated_widget_prop_key] = }\nSO WE POP {self.to_update_stack_dict_list.index(widget_update_stack_dict) = } AND ADD 'dwgno': {dwgno_updated_widget_dict['dwgno']}, 'updated_widget_prop_key': {dwgno_updated_widget_dict[updated_widget_prop_key]}")
        #                 self.to_update_stack_dict_list.pop(self.to_update_stack_dict_list.index(widget_update_stack_dict))
        #                 self.to_update_stack_dict_list.append({'dwgno': dwgno_updated_widget_dict['dwgno'],
        #                                                         updated_widget_prop_key: dwgno_updated_widget_dict[updated_widget_prop_key]})
        #                 # print(f'(There were changes made:    {self.to_update_stack_dict_list}')
        #                 return
        #             else:
        #                 # print(f'(There were NO changes made: {self.to_update_stack_dict_list}') 
        #                 # print(f"{dwgno_updated_widget_dict[updated_widget_prop_key] = } EQUALS {widget_update_stack_dict[updated_widget_prop_key] = } SO WE DO NOTHING")
        #                 return
        # # print(f'New entry to stack: {dwgno_updated_widget_dict = }')
        # self.to_update_stack_dict_list.append(dwgno_updated_widget_dict)     
        # # print(f'(New entry added to stack:   {self.to_update_stack_dict_list}')
    #endregion       