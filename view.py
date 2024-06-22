import tkinter as tk
from tkinter import ttk
from sqlalchemy.inspection import inspect
from utils import center_window, create_tree_button_frame
from model import session, Base


class CRUDWindow:
    def __init__(self, master, table_name):
        self.root = master
        self.window = tk.Toplevel(master)
        self.table_name = table_name            
        self.table_titles = {
            'clients' : 'Clients',
            'mechanicalengineers': 'Mechanical Engineers',
            'mechanicalcontractors': 'Mechanical Contractors',
            'designengineers': 'Design Engineers',
            'salesengineers': 'Sales Engineers',
            'projectmanagers': 'Project Managers'
            }
        self.window.title(self.table_titles.get(table_name))
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.resizable(width=True, height=False)
        
                # Generate column map
        self.column_map = self.generate_column_map(table_name)

        # Generate table_data
        self.table_data = self.get_table_data(table_name)

        # # Create the main frame
        # self.main_frame = ttk.Frame(self.window)
        # self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        # self.main_frame.grid_columnconfigure(0, weight=1)
        # self.main_frame.grid_rowconfigure(0, weight=1)

        # # Create treeview
        # self.tree = create_tree_frame_from_db_table(self.main_frame, self.column_map, self.table_data)
        # self.tree.grid(row=0, column=0, sticky='nsew')        

        # Create the tree button frame
        self.tree_button_frame = create_tree_button_frame(self.window, self.column_map,self.table_data)
        self.tree_button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')    

        center_window(self.window)

    def generate_column_map(self, table_name):
        # Reflect the table from the database
        model_class = self.get_model_class(table_name)
        columns = inspect(model_class).columns
        column_map = {col.name: idx for idx, col in enumerate(columns) if col.name != 'id'}
        return column_map

    def get_model_class(self, table_name):
        # Dynamically get all subclasses of Base
        model_classes = {cls.__tablename__: cls for cls in Base.__subclasses__()}
        return model_classes[table_name]
    
    def get_table_data(self, table_name):
        model_class = self.get_model_class(table_name)
        columns = inspect(model_class).columns        
        column_objects = [getattr(model_class, col.name) for col in columns]
        table_data = session.query(*column_objects).all()
        return table_data
