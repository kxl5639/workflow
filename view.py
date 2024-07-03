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

        # Create the tree button frame
        self.tree_button_frame = create_tree_button_frame(self.window, self.column_map, self.table_data)
        self.tree_button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')    

        center_window(self.window)
        self.window.focus_force()

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


class BaseWindow:
    def __init__(self, title, parent, is_root=False):
        self.parent = parent
        self.root = tk.Tk() if is_root else tk.Toplevel(self.parent)
        self.root.title(title)
        self.root.resizable(width=False, height=True)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        center_window(self.root)
        self.root.focus_force()
        

class TreeFrame:
    def __init__(self, parent, column_map, table_data) -> None:
        self.parent = parent
        self.column_map = column_map
        self.table_data = table_data

        self.columns_list = self.column_map_to_list()
        self.tree_frame = self.create_tree_frame()
        self.tree = self.create_tree()
        self.populate_treeview()
        self.resize_width_of_columns()

    def resize_width_of_columns(self):
        columns = self.columns_list 

        # Determine the maximum width needed for each column
        column_widths = {col: len(col) * 10 for col in columns}
        for row in self.table_data:
            values = [str(row[self.column_map[col]]) for col in columns]
            for col, value in zip(columns, values):
                column_widths[col] = max(column_widths[col], len(value) * 10)
        for col in columns:
            self.tree.column(col, width=column_widths[col])

    def populate_treeview(self):
        for row in self.table_data:
            values = [row[self.column_map[col]] for col in self.tree["columns"]]        
            self.tree.insert("", "end", iid=row[0], values=values)

    def create_tree(self):
        tree = ttk.Treeview(self.tree_frame, columns=self.columns_list, show='headings')
        tree.grid(row=0,column=0, sticky='nsew') 
        for col in self.columns_list:
            tree.heading(col, text=col.replace("_", " ").title())   
        return tree

    def create_tree_frame(self):
        tree_frame = ttk.Frame(self.parent)   
        tree_frame.grid(row=0, column=0, sticky='nsew') 
        tree_frame.grid_rowconfigure(0,weight=1) 
        tree_frame.grid_columnconfigure(0,weight=1)
        return tree_frame

    def column_map_to_list(self):
        # Sort the dictionary by the values (positions) and extract the keys (column names)
        return [col for col, pos in sorted(self.column_map.items(), key=lambda item: item[1])]
    
class ListWindow(BaseWindow):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, is_root)
        self.controller = controller
        self.root.resizable(width=True, height=True)            

        # Create Treeview
        TreeFrame(self.parent, self.controller.column_map, self.controller.table_data)
        
        center_window(self.root)
        self.root.focus_force()