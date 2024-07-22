import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from sqlalchemy import asc, desc
from model import session, Base, Diagram
from typing import Any, List, Dict, Optional, Type
from configs import testing

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

        if testing == 1:
            self.root.bind("<Key>", lambda event: on_keypress(event))
            def on_keypress(event):
                if event.char == 'q':
                    self.parent.root.destroy()
 
############ Frame Structure #############
#                                        #
#  root or toplevel -> system_base_frame #
#                                        #
##########################################

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

class View(BaseWindow):
    def __init__(self, title, parent, controller=None, is_root=False):
        super().__init__(title, parent, controller, is_root)
        if testing == 0:
            self.relief = None
        else:
            self.relief = 'solid'

    @staticmethod
    def create_entry_widget(parent,
                            row: int,
                            col: int,
                            padx: int = None,
                            pady: int = None,
                            sticky: str = 'nsew'):
        entry_widget = ttk.Entry(parent)
        entry_widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return entry_widget
    
    @staticmethod
    def create_label(parent,
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
    
class ListWindow(View):
    
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)        
        self.root.resizable(width=True, height=True)            

        # Create TreeFrame
        self.tree_frame = TreeFrame(self.base_frame, self.controller.column_map, self.controller.table_data)
        self.tree_frame.tree_frame.grid(row=0, padx=0, pady=(0,10), sticky="nsew")
        self.tree_frame.tree.bind("<Double-1>", lambda event:self.on_double_click())
        # # Create Button Frame
        # self.button_frame = ButtonsFrame(self.base_frame, self.controller.button_info)
        # self.button_frame.button_frame.grid(row=1, column=0, pady=0, padx=0)
        # Center Window
        
        BaseWindow.center_window(self.root)  

######### Frame Structure ##########
#                                  #
#  system_base_frame -> tree_frame #
#                                  #
####################################

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

    def find_dict_with_key_value_from_list(self, key: Any, value: Any, list_of_dicts: List[Dict[Any, Any]]) -> Optional[Dict[Any, Any]]:
        """
        Find and return the first dictionary that contains the specified key-value pair in a list of dictionaries.

        Args:
            key (Any): The key to look for in each dictionary.
            value (Any): The value to compare against the key in each dictionary.
            list_of_dicts (List[Dict[Any, Any]]): The list of dictionaries to search.

        Returns:
            Optional[Dict[Any, Any]]: The first dictionary that contains the key with the specified value, or None if no such dictionary is found.
        """
        for dictionary in list_of_dicts:

            for key in dictionary:
                if key == value:
                    return dictionary
        return None

class Model:
    def __init__(self, controller=None) -> None:
        self.controller = controller
        self.diagram_options = self.query_column_values(Diagram, 'type', exclude_id=1)

    def delete_record(self, object_list):
        for obj in object_list:
            session.delete(obj)

    def add_record(self, record_obj):
        session.add(record_obj)

    def commit_changes(self):
        session.commit()

    def get_rec_objs_by_opt_filts(self, model: Type[Base], filters: Dict[str, Any] = None, sort_by: Optional[str] = None, descending: bool = False) -> List[Base]:
        """
        Query the database for records from a specified model, applying filters and sorting if provided.

        Parameters:
        - model (Type[Base]): SQLAlchemy model class.
        - filters (dict, optional): A dictionary where keys are column names and values are the values to filter the columns by.
        - sort_by (str, optional): The column name to sort the results by.
        - descending (bool, optional): Whether to sort in descending order. Default is False (ascending).

        Returns:
        - list: A list of model instances that match the filter conditions, sorted if specified, or all records if no filters are provided.
        """
        query = session.query(model)
        
        if filters:
            for filter_column, filter_value in filters.items():
                filter_col_attr = getattr(model, filter_column)
                query = query.filter(filter_col_attr == filter_value)
        
        if sort_by:
            sort_col_attr = getattr(model, sort_by)
            if descending:
                query = query.order_by(desc(sort_col_attr))
            else:
                query = query.order_by(asc(sort_col_attr))
        
        return query.all()
    
    def get_vals_from_rec_objs(self, model: Type[Base], columns: List[str], filters: Dict[str, Any] = None, sort_by: Optional[str] = None, descending: bool = False) -> List[Dict[str, Any]]:
        """
        Filter out values for given column names from the query results, optionally sorting by a column.

        Parameters:
        - model (Type[Base]): SQLAlchemy model class.
        - filters (dict, optional): A dictionary where keys are column names and values are the values to filter the columns by.
        - columns (list): A list of column names to extract from each record.
        - sort_by (str, optional): The column name to sort the results by.
        - descending (bool, optional): Whether to sort in descending order. Default is False (ascending).

        Returns:
        - list: A list of dictionaries with specified column names and their values for each record.
        """
        query_results = self.get_rec_objs_by_opt_filts(model, filters, sort_by, descending)
        filtered_results = []

        for record in query_results:
            record_dict = {}
            for column in columns:
                record_dict[column] = getattr(record, column)
            filtered_results.append(record_dict)
        
        return filtered_results
    
    def query_column_values(self, model, column, exclude_id=None):
        '''
        Query values of specified column with option to exclude specific id.
        
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
        values_list = session.query(column_attr)
        if exclude_id is not None:
            values_list = values_list.filter(model.id != exclude_id).all()
        
        # Flatten the list of tuples to a list of values
        values_list = [value[0] for value in values_list]
        return values_list