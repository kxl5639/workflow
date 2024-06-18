import tkinter as tk
from tkinter import Toplevel, ttk, Listbox, StringVar, messagebox, Entry, END
from project.project_controller import column_map, table_data, columns_to_display
from utils import center_window

def populate_treeview(tree, table_data, column_map):
    """
    Populate a TreeView with the provided data.

    Parameters:
    - tree: The TreeView widget.
    - table_data: List of tuples containing the data to be inserted.
    - column_map: Dictionary mapping of column names to their positions in the data tuples.
    """
    for row in table_data:
        values = [row[column_map[col]] for col in tree["columns"]]
        tree.insert("", "end", text=row[column_map["project_number"]], values=values)

def column_map_to_list(column_map):
    # Sort the dictionary by the values (positions) and extract the keys (column names)
    return [col for col, pos in sorted(column_map.items(), key=lambda item: item[1])]


def resize_max_width_of_tree_columns(tree, table_data, column_map):
    columns =  column_map_to_list(column_map) 

    # Determine the maximum width needed for each column
    column_widths = {col: len(col) * 10 for col in columns}

    for row in table_data:
        values = [str(row[column_map[col]]) for col in columns]
        for col, value in zip(columns, values):
            column_widths[col] = max(column_widths[col], len(value) * 10)        
    
    for col in columns:
        tree.column(col, width=column_widths[col])

    
    # column_widths = {col: len(col.replace("_", " ").title()) * 10 for col in columns}
    
    # for row in table_data:
    #     values = [str(getattr(row, col)) for col in columns]
    #     for col, value in zip(columns, values):
    #         column_widths[col] = max(column_widths[col], len(value) * 10)
    
    # # Adjust column widths based on the content
    # for col in columns:
    #     tree.column(col, width=column_widths[col])



def create_tree_frame_from_db_table(master,table_data, column_map):   
    columns = column_map_to_list(column_map)     

    tree_frame = ttk.Frame(master)   
    tree_frame.grid(row=0, column=0, sticky='nsew') 
    tree_frame.grid_rowconfigure(0,weight=1) 
    tree_frame.grid_columnconfigure(0,weight=1) 
    
    tree = ttk.Treeview(tree_frame,columns=columns, show='headings')    
    tree.grid(row=0,column=0, sticky='nsew')
    
    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
    
    populate_treeview(tree, table_data, column_map)

    resize_max_width_of_tree_columns(tree, table_data, column_map)

    
    tree_frame.tree = tree
    return tree_frame






root = tk.Tk()
root.title('Test')
center_window(root)
tree_frame = create_tree_frame_from_db_table(root,table_data, column_map)
root.grid_rowconfigure(0,weight=1) 
root.grid_columnconfigure(0,weight=1) 
root.mainloop()
