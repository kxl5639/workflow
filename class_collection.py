import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from model import session, Base, Diagram
from typing import List, Type

class BaseWindow(ABC):
    def __init__(self, title, parent, controller=None, is_root=False):
        import tkinter as tk
        from tkinter import ttk
        self.parent = parent
        self.controller = controller
        self.root = tk.Tk() if is_root else tk.Toplevel(self.parent.root)
        self.root.title(title)
        self.root.resizable(width=True, height=True)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.base_frame = self.create_base_frame(self.root)
    
    @staticmethod
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')  # Only set the position, not the size
        window.focus_force()

    @staticmethod
    def create_base_frame(parent):
        '''Create base frame'''
        base_frame = ttk.Frame(parent)
        base_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')        
        return base_frame
       
class TreeFrame:
    def __init__(self, parent, column_map, table_data) -> None:
        self.parent = parent
        self.column_map = column_map
        self.table_data = table_data

        self.columns_list = self.column_map_to_list()
        self.tree_frame = self.create_tree_frame()
        self.tree = self.create_tree()        
        self.populate_treeview(self.table_data)
        self.resize_width_of_columns()

    def refresh_tree(self, table_data): 
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview(table_data)
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

    def populate_treeview(self, table_data):
        for row in table_data:
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
        super().__init__(title, parent, controller, is_root)        
        self.root.resizable(width=True, height=True)            

        # Create TreeFrame
        self.tree_frame = TreeFrame(self.base_frame, self.controller.column_map, self.controller.table_data)
        self.tree_frame.tree_frame.grid(row=0, padx=0, pady=(0,10), sticky="nsew")
        self.tree_frame.tree.bind("<Double-1>", lambda event:self.on_double_click())
        # Create Button Frame
        self.button_frame = ButtonsFrame(self.base_frame, self.controller.button_info)
        self.button_frame.button_frame.grid(row=1, column=0, pady=0, padx=0)
        # Center Window
        BaseWindow.center_window(self.root)  

    @abstractmethod
    def on_double_click(self):
        pass

    def refresh_tree(self):
        self.tree_frame.refresh_tree(self.controller.update_table_data())

class ButtonsFrame:
    '''
    button_info: A list of tuples, each containing the button label and command.
    Example: [("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)]
    Outside padding of the returned frame is all 0. There is only padding in between the buttons.
    '''
    def __init__(self, parent, button_info) -> None:
        self.parent = parent
        self.button_info = button_info
        self.button_frame = self.create_button_frame()

    def create_button_frame(self):
        button_frame = ttk.Frame(self.parent)    
        gen_pad = 10
        
        # Configure grid layout
        button_frame.grid_rowconfigure(0, weight=1)
        for i in range(len(self.button_info)):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons based on button_info
        for index, (label, command) in enumerate(self.button_info):
            button = ttk.Button(button_frame, text=label, command=command)
            button.grid(row=0, column=index,
                        padx=(gen_pad if index != 0 else 0,
                            gen_pad if index != len(self.button_info) - 1 else 0),
                            pady=0, sticky="nsew")
        
        return button_frame
    
class Controller:
    def __init__(self, parent=None, project_number = None) -> None:
        self.parent = parent
        self.project_number = project_number

class Model:
    def __init__(self, controller=None) -> None:
        self.controller = controller
        self.diagram_options = self.query_column_values(Diagram, 'type')

    def delete_record(self, object_list):
        for obj in object_list:
            session.delete(obj)

    def add_record(self, record_obj):
        session.add(record_obj)

    def commit_changes(self):
        session.commit()

    def get_objs_from_column_data(self, model: Type[Base], col_name, col_val) -> List[Base]:
        col_attr = getattr(model, col_name)
        return session.query(model).filter(col_attr == col_val).all()
    
    def query_multiple_columns_with_filter(self, model, columns: list[str], filter_column, filter_value, sort_column=None):
        '''
        Query specified columns from a SQLAlchemy model based on a filter condition.
        
        Parameters:
        - model: SQLAlchemy model class.
        - columns (list of str): A list of column names (as strings) to retrieve from the model.
        - filter_column (str): The name of the column to use for filtering the query.
        - filter_value (any): The value to filter the specified filter_column by.
        - sort_column (str, optional): The name of the column to sort the result by. Should be one of the columns in the 'columns' list.
        
        Returns:
        - list: A list of dictionaries, where each dictionary contains the values of the specified columns 
                for each row that matches the filter condition.
        
        Example:
        columns = ['name', 'age']
        filter_column = 'id' # This column is your given column, along with given filter_value.
        filter_value = 2
        sort_column = 'name'
        result = query_multiple_columns_with_filter(User, columns, filter_column, filter_value, sort_column)
        
        Returns a list of dictionaries with the key(column) value(column_value) for record object.
        '''
        filter_col_attr = getattr(model, filter_column)        
        record_objs_list = session.query(model).filter(filter_col_attr == filter_value).all()
        
        col_and_value_dict_list = []
        for record_obj in record_objs_list:
            individual_dict = {col: getattr(record_obj, col) for col in columns}
            col_and_value_dict_list.append(individual_dict)
        
        if sort_column and sort_column in columns:
            col_and_value_dict_list = sorted(col_and_value_dict_list, key=lambda x: x[sort_column])
        
        return col_and_value_dict_list
    
    def get_objs_list_with_filter(self, model, filters: dict) -> List[Base]: 
        '''
        Query specified objects based on multiple filter conditions.
        
        Parameters:
        - model: SQLAlchemy model class.
        - filters (dict): A dictionary where the keys are column names and values are the values to filter the specified columns by.
        
        Returns:
        - list: A list of objects.
        
        Example:
        filters = {'id': 2, 'city': 'New York'} # Filters based on multiple columns
        result = get_objs_list_with_filter(DwgTitle, {'dwgno' : 1, 'project_id' : 2})
        
        Returns a list of dictionaries with the key(column) value(column_value) for record object.
        '''
        query = session.query(model)
        
        for filter_column, filter_value in filters.items():
            filter_col_attr = getattr(model, filter_column)
            query = query.filter(filter_col_attr == filter_value)
            
        record_objs_list = query.all()        
        
        return record_objs_list

    
    def query_column_values(self, model, column):
        '''
        Query a specified column from a SQLAlchemy model.
        
        Parameters:
        - model: SQLAlchemy model class.
        - column (str): The name of the column to retrieve from the model.
        
        Returns:
        - list: A list of values from the specified column.
        
        Example:
        column = 'name'
        result = query_column_values(User, column)
        
        Returns a list of values from the 'name' column for all records.
        '''
        column_attr = getattr(model, column)
        values_list = session.query(column_attr).all()
        
        # Flatten the list of tuples to a list of values
        values_list = [value[0] for value in values_list]
        return values_list

    
class View(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)

    def create_entry_widget(self,
                            parent,
                            row: int,
                            col: int,
                            padx: int = None,
                            pady: int = None,
                            sticky: str = 'nsew'):
        entry_widget = ttk.Entry(parent)
        entry_widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return entry_widget
    
    def create_label(self,
                     parent,
                     text: str,
                     row: int,
                     col: int,
                     padx: int  = 0,
                     pady: int = 0,
                     sticky: str = 'nsew',
                     relief: str = None):
        label = ttk.Label(parent, text=text, relief=relief)
        label.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return label
    
    def create_frame(self,
                     parent,
                     row: int,
                     col: int,
                     padx: int  = 0,
                     pady: int = 0,
                     sticky: str = 'nsew',
                     relief: str = None):
        frame = ttk.Frame(parent, relief=relief)
        frame.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return frame
    
    def create_label_frame(self,
                           parent,
                           text: str,
                           row: int,
                           col: int,
                           padx: int  = 0,
                           pady: int = 0,
                           sticky: str = 'nsew',
                           relief: str = None):
        frame = ttk.LabelFrame(parent, text=text, relief=relief)
        frame.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return frame
    
    def create_combobox(self,
                        parent,
                        row: int,
                        col: int,
                        padx: int  = 0,
                        pady: int = 0,
                        sticky: str = 'nsew',
                        state: str = None,):
        combobox = ttk.Combobox(parent, state=state)
        combobox.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return combobox