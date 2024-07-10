import tkinter as tk
from tkinter import ttk, font
from class_collection import View, ButtonsFrame

class TitleView(View):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.initiate_testing_values(0)
        self.root.resizable(width=True, height=True)
        self.project_number = project_number
        self.title_column_break = 10
        self.header_font = font.Font(family="Helvetica", size=9, weight="bold")
        self.title_col_frames_list = []
        
        self.create_project_number_frame()
        self.create_and_populate_titles_frame()
        self.create_right_toolbar_frame()

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

    def create_project_number_frame(self):
        project_number_frame = self.create_frame(self.base_frame, 0, 0,
                                                 padx=0, pady=(0,10), sticky='nsew',
                                                 relief = self.relief)
        
        self.create_label(project_number_frame, f'EM: {self.project_number}',
                          0, 0, padx=0, pady=0,
                          sticky='w', relief=self.relief)
    
    def create_and_populate_titles_frame(self):

        def create_titles_frame():
            self.titles_label_frame = self.create_label_frame(self.base_frame, 'Titles', 1, 0,
                                                    padx=(0,10),pady=0,sticky='nsew',
                                                    relief=self.relief)
            return self.titles_label_frame

        def create_title_col_frame(cidx):
            if cidx == 0: xpad = 10
            else: xpad = (0,10)
            title_col_frame = self.create_frame(self.titles_label_frame, 0, cidx,
                                                padx=xpad, pady=10, sticky='nsew',
                                                relief='solid')
            return title_col_frame
                    
        def create_title_header_frame(parent):
            title_header = self.create_label(parent, 'Title', 0, 1, (0,10), (0,5), sticky='nsew')
            title_header.config(font=self.header_font, relief=self.relief, anchor ='center')
            diagram_header = self.create_label(parent, 'Diagram', 0, 2, (0,10), (0,5), sticky='nsew')
            diagram_header.config(font=self.header_font, relief=self.relief, anchor ='center')
            system_header = self.create_label(parent, 'System', 0, 3, 0, (0,5), sticky='nsew')
            system_header.config(font=self.header_font, relief=self.relief, anchor ='center')

        def create_title_data_frame(ridx, dwgno, title, diagram_name, system_name):
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

            title_entry = self.create_entry_widget(title_data_frame, ridx, 1, (0,10), 0)
            title_entry.insert(0, title)
            title_entry.config(width = 50)

            diagram_combo = self.create_combobox(title_data_frame, ridx, 2, (0,10), 0, state='readonly')
            diagram_combo.set(diagram_name)
            diagram_combo.config(values=self.controller.diagram_options,
                                 width=max(len(option) for option in self.controller.diagram_options))
            
            system_combo = self.create_combobox(title_data_frame, ridx, 3, 0, 0, state='readonly')
            system_combo.set(system_name)
            system_combo.config(values=self.controller.systems_list,
                                width=max(len('system'), max(len(option) for option in self.controller.systems_list)))
            
    ####### create_and_populate_titles_frame() MAIN CODE STARTS HERE ##############################  
          
        self.titles_label_frame = create_titles_frame()

        all_title_data_dict_generator = self.controller.generate_all_title_data_dict()
        self.max_title_length = 0
        for title_data_dict in all_title_data_dict_generator:

            dwgno = title_data_dict['dwgno']
            title = title_data_dict['title']
            diagram_id = title_data_dict['diagram_id']
            diagram_name = self.controller.get_diagram_name_from_id(diagram_id)
            system_id = title_data_dict['system_id']
            system_name = self.controller.get_system_name_from_id(system_id)
            if dwgno % self.title_column_break == 0:
                in_column = dwgno // self.title_column_break -1
                in_row = self.title_column_break
            else:
                in_column = dwgno // self.title_column_break
                in_row = dwgno - (in_column*self.title_column_break)

            if len(title) > self.max_title_length:
                self.max_title_length = len(title)
        
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

        def add_title_btn_cmd(self):
                pass
        def move_btn_cmd(self, direction):
            pass
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