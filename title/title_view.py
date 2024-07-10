import tkinter as tk
from tkinter import ttk
from class_collection import View, ButtonsFrame
from model import session, Project

class TitleView(View):
    def __init__(self, title, parent, controller, project_number, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.project_number = project_number
        self.title_column_break = 15
        self.root.resizable(width=True, height=True)
        self.testing = 1
        if self.testing == 0:
            self.relief = None
        else:
            self.relief = 'solid'
    
        self.create_project_number_frame()
        self.create_titles_frame()
        self.create_right_toolbar_frame()

        self.center_window(self.root)

#####################################################################################

####################### Frame Structure #######################
#                                                             #
#  base_frame [-> titles_frame -> entry_frame]                #
#              -> project_number_frame]                       #
#              -> right_toolbar_frame [-> menu_frame]         #
#                                      -> autocad_scr_frame]  #
#                                                             # 
###############################################################

    def create_project_number_frame(self):
        project_number_frame = self.create_frame(self.base_frame, 0, 0,
                                                 padx=0, pady=(0,10), sticky='nsew',
                                                 relief = self.relief)
        project_number_label = self.create_label(project_number_frame, f'EM: {self.project_number}',
                                                 0, 0, padx=0, pady=0,
                                                 sticky='w', relief=self.relief)
    
    def create_titles_frame(self):

        def populate_titles_frame():

            self.controller.fetch_all_title_data_dict()

            # def create_title_col_frame(ridx, cidx):
            #     title_col_frame = self.create_frame(self.titles_frame, ridx, cidx,
            #                                         padx=0, pady=0, sticky='nsew',
            #                                         relief=self.relief)

            # # Get number of title objects from controller
            # num_title_obj = len(self.controller.dwgtitle_table_dict_list)
            # # title_dict = self.controller.title_dict
            # # # print(title_dict)
            
            # if num_title_obj:
            #     pass # Create entry frames based on titles
            # else:
            #     pass # Create default entries such as com riser, general notes, master panel, etc...

        self.titles_frame = self.create_label_frame(self.base_frame, 'Titles', 1, 0,
                                                 padx=(0,10),pady=0,sticky='nsew',
                                                 relief=self.relief)
        populate_titles_frame()
    
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