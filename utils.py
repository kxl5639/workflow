import tkinter as tk
from tkinter import Toplevel, ttk, Listbox, StringVar, messagebox, Entry, END
from datetime import datetime
from sqlalchemy.inspection import inspect
from configs import testing

#region View Functions

def center_window(window):        
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_tree_frame_from_db_table(master,column_map):   
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
    
    populate_treeview(tree, column_map)

    resize_max_width_of_tree_columns(tree, column_map)

    
    tree_frame.tree = tree
    return tree_frame

def create_standard_tree_but_frame(master, column_map, add_command=None, modify_command=None, delete_command=None ):
    tree_addmoddel_frame = ttk.Frame(master, name='tree_addmoddel_frame')        
    tree_addmoddel_frame.grid_rowconfigure((0), weight=1)
    tree_addmoddel_frame.grid_rowconfigure((1), weight=0)
    tree_addmoddel_frame.grid_columnconfigure(0, weight=1)    
    
    tree_frame = create_tree_frame_from_db_table(tree_addmoddel_frame, column_map)
    tree_frame.grid(row=0, padx=0, pady=(0,20), sticky="nsew")    

    addmoddel_buttons_frame = create_button_frame(tree_addmoddel_frame,[("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)])
    addmoddel_buttons_frame.grid(row=1, column=0, pady=0, padx=0)    

    tree_addmoddel_frame.tree_frame = tree_frame
    return tree_addmoddel_frame



#endregion

#region Controller Functions

def populate_treeview(tree, column_map):    
    """
    Populate a TreeView with the provided data.

    Parameters:
    - tree: The TreeView widget.    
    - column_map: Dictionary mapping of column names to their positions in the data tuples.
    """    
    from project.project_controller import update_table_data    
    table_data = update_table_data()
    for row in table_data:
        values = [row[column_map[col]] for col in tree["columns"]]        
        tree.insert("", "end", iid=row[0], values=values)

def column_map_to_list(column_map):
    # Sort the dictionary by the values (positions) and extract the keys (column names)
    return [col for col, pos in sorted(column_map.items(), key=lambda item: item[1])]

def refresh_tree(tree, column_map): 
    for item in tree.get_children():
        tree.delete(item)

    resize_max_width_of_tree_columns(tree, column_map)

    populate_treeview(tree, column_map)


def resize_max_width_of_tree_columns(tree, column_map):
    from project.project_controller import update_table_data    
    table_data = update_table_data()

    columns =  column_map_to_list(column_map) 

    # Determine the maximum width needed for each column
    column_widths = {col: len(col) * 10 for col in columns}

    for row in table_data:
        values = [str(row[column_map[col]]) for col in columns]
        for col, value in zip(columns, values):
            column_widths[col] = max(column_widths[col], len(value) * 10)        
    
    for col in columns:
        tree.column(col, width=column_widths[col])

def only_one_record_selected(tree): #record refers to a record in a table.
    selected_items = tree.selection()    
    if len(selected_items) > 1:
        return False
    else:
        return True

def modify_record_properly_selected(tree,session,model):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a record to modify.")
        return None
    if only_one_record_selected(tree) is True:
        record_id = selected_item[0]  # The item identifier (iid) is the project ID
        record = session.query(model).get(record_id)
        return record
    else:
        show_custom_error_message(tree, "Error", "Only one record can be selected to modify.")
        return None


#endregion

#region Model Functions


#endregion

#region msgbox Functions

def show_custom_error_message(parent_window, title, message):
    error_message_window = tk.Toplevel()
    error_message_window.transient(parent_window)
    error_message_window.title(title)
    error_message_window.resizable(False, False)  # Make the window non-resizable
    #error_message_window.overrideredirect(True)  # Remove title bar and window controls
    # error_message_window.wm_attributes('-toolwindow', 'true')

    ttk.Label(error_message_window, text=message).pack(padx=10, pady=10)
    ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    
    center_window(error_message_window)

    error_message_window.grab_set()  # Make the window modal
    error_message_window.focus_force()  # Focus on the error message window
    parent_window.wait_window(error_message_window)  # Wait until the error message window is closed

def show_custom_confirmation_message(parent_window, title, message):
    confirmation_window = tk.Toplevel()
    confirmation_window.transient(parent_window)
    confirmation_window.title(title)
    confirmation_window.resizable(False, False)  # Make the window non-resizable
    # confirmation_window.wm_attributes('-toolwindow', 'true')
    #confirmation_window.overrideredirect(True)  # Remove title bar and window controls
    result = {'value': None}

    def on_yes():
        result['value'] = True
        confirmation_window.destroy()

    def on_no():
        result['value'] = False
        confirmation_window.destroy()

    ttk.Label(confirmation_window, text=message).pack(padx=10, pady=10)
    button_frame = ttk.Frame(confirmation_window)
    button_frame.pack(pady=5)
    ttk.Button(button_frame, text="Yes", command=on_yes).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="No", command=on_no).pack(side=tk.RIGHT, padx=5)
    # Bind the close button to on_no
    confirmation_window.protocol("WM_DELETE_WINDOW", on_no)

    center_window(confirmation_window)
    confirmation_window.grab_set()
    confirmation_window.focus_force()
    parent_window.wait_window(confirmation_window)

    return result['value']

#endregion

#region Button Functions

def create_button_frame(master, button_info):
    # - button_info: A list of tuples, each containing the button label and command.
    #               Example: [("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)]
   
    button_frame = ttk.Frame(master)    
    gen_pad = 5
    
    # Configure grid layout
    button_frame.grid_rowconfigure(0, weight=1)
    for i in range(len(button_info)):
        button_frame.grid_columnconfigure(i, weight=1)
    
    # Create buttons based on button_info
    for index, (label, command) in enumerate(button_info):
        button = ttk.Button(button_frame, text=label, command=command)
        button.grid(row=0, column=index, padx=(gen_pad if index != 0 else 0, gen_pad if index != len(button_info) - 1 else 0), pady=0, sticky="nsew")
    
    return button_frame

#endregion

#region Create Window Functions



#endregion



