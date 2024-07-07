import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class BaseWindow(ABC):
    def __init__(self, title, parent, controller=None, is_root=False):
        import tkinter as tk
        from tkinter import ttk
        self.parent = parent
        self.controller = controller
        self.root = tk.Tk() if is_root else tk.Toplevel(self.parent)
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