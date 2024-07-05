import tkinter as tk
from tkinter import Toplevel, ttk, Listbox, StringVar, messagebox, Entry, END
from sqlalchemy.inspection import inspect
from view import BaseWindow

# #region View Functions

# def create_tree_frame_from_db_table(master,column_map, table_data):   
#     columns = column_map_to_list(column_map)     

#     tree_frame = ttk.Frame(master)   
#     tree_frame.grid(row=0, column=0, sticky='nsew') 
#     tree_frame.grid_rowconfigure(0,weight=1) 
#     tree_frame.grid_columnconfigure(0,weight=1) 
    
#     tree = ttk.Treeview(tree_frame,columns=columns, show='headings')
#     tree.grid(row=0,column=0, sticky='nsew')    
    
#     # Define the column headings and set a minimum width
#     for col in columns:
#         tree.heading(col, text=col.replace("_", " ").title())
    
#     populate_treeview(tree, column_map, table_data)
#     resize_max_width_of_tree_columns(tree, column_map, table_data)
    
#     tree_frame.tree = tree
#     return tree_frame

# def create_tree_button_frame(master, column_map, table_data, add_command=None, modify_command=None, delete_command=None ):
#     tree_addmoddel_frame = ttk.Frame(master, name='tree_addmoddel_frame')        
#     tree_addmoddel_frame.grid_rowconfigure((0), weight=1)
#     tree_addmoddel_frame.grid_rowconfigure((1), weight=0)
#     tree_addmoddel_frame.grid_columnconfigure(0, weight=1)    
    
#     tree_frame = create_tree_frame_from_db_table(tree_addmoddel_frame, column_map, table_data)
#     tree_frame.grid(row=0, padx=0, pady=(0,20), sticky="nsew")    

#     addmoddel_buttons_frame = create_button_frame(tree_addmoddel_frame,[("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)])
#     addmoddel_buttons_frame.grid(row=1, column=0, pady=0, padx=0)    

#     tree_addmoddel_frame.tree_frame = tree_frame
#     return tree_addmoddel_frame

# def highlight_tree_item(master, tree, item_id):    
#     tree.selection_set(item_id)
#     tree.see(item_id)

# #endregion

# #region Controller Functions

# def populate_treeview(tree, column_map, table_data):    
#     """
#     Populate a TreeView with the provided data.

#     Parameters:
#     - tree: The TreeView widget.    
#     - column_map: Dictionary mapping of column names to their positions in the data tuples.
#     """    
#     for row in table_data:
#         values = [row[column_map[col]] for col in tree["columns"]]        
#         tree.insert("", "end", iid=row[0], values=values)

# def column_map_to_list(column_map):
#     # Sort the dictionary by the values (positions) and extract the keys (column names)
#     return [col for col, pos in sorted(column_map.items(), key=lambda item: item[1])]

# def refresh_tree(tree, column_map, table_data): 
#     for item in tree.get_children():
#         tree.delete(item)

#     resize_max_width_of_tree_columns(tree, column_map, table_data)

#     populate_treeview(tree, column_map, table_data)

# def resize_max_width_of_tree_columns(tree, column_map, table_data):
#     columns =  column_map_to_list(column_map) 

#     # Determine the maximum width needed for each column
#     column_widths = {col: len(col) * 10 for col in columns}

#     for row in table_data:
#         values = [str(row[column_map[col]]) for col in columns]
#         for col, value in zip(columns, values):
#             column_widths[col] = max(column_widths[col], len(value) * 10)        
    
#     for col in columns:
#         tree.column(col, width=column_widths[col])

# def only_one_record_selected(tree): #record refers to a record in a table.    
#     if num_record_selected(tree) > 1:
#         return False
#     else:
#         return True

# def num_record_selected(tree): #record refers to a record in a table.
#     selected_items = tree.selection()    
#     num_record_selected = len(selected_items)
#     return num_record_selected

# class MsgBox:    
#     def __init__(self, title, message, main_window, parent) -> None:
#         self.title = title
#         self.message = message
#         self.main_window = main_window
#         self.parent = parent
#         self.popup_count = 0        
#         self.msgbox_response = self.showmsgbox()

#     def disable_windows(self, window):
#         for child in window.winfo_children(): # Get all the child widgets of the window
#             if isinstance(child, tk.Tk) or isinstance(child, Toplevel): # Check if the child is a Tk or Toplevel window so that we can disable them
#                 child.attributes('-disabled', True)
#                 self.disable_windows(child)

#     def enable_windows(self, window):
#         for child in window.winfo_children(): # Get all the child widgets of the window
#             if isinstance(child , tk.Tk) or isinstance(child , Toplevel): # Check if the child is a Tk or Toplevel window so that we can enable them
#                 child.attributes('-disabled' , False)
#                 self.enable_windows(child)

#     def increase_popup_count(self):        
#         self.popup_count += 1
#         # if self.popup_count > 0: # Check if a popup is currently active so that we can disable the windows
#         #     # self.disable_windows(self.main_window)
#         #     self.disable_windows(self.parent)
#         # else: # Enable the windows if there is no active popup
#         #     # self.enable_windows(self.main_window)
#         #     # self.enable_windows(self.parent)
#         #     pass

#     def decrease_popup_count(self):        
#         self.popup_count -= 1
#         # if self.popup_count > 0: # Check if a popup is currently active so that we can disable the windows
#         #     # self.disable_windows(self.main_window)
#         #     self.disable_windows(self.parent)
#         # else: # Enable the windows if there is no active popup
#         #     # self.enable_windows(self.main_window)
#         #     # self.enable_windows(self.parent)
#         #     pass

#     def showmsgbox(self): # A custom showinfo funtion
#         self.increase_popup_count() # Increase the 'popup_count' when the messagebox shows up
#         response = messagebox.askyesno(self.title , self.message, parent=self.parent)
#         self.decrease_popup_count()
#         return response

        

# #endregion

# #region Model Functions

# def delete_record(record, session):
#     try:
#         session.delete(record)
#         session.commit()
#     except Exception as e:
#         return str(e)  # Return the error message
#     return None

# #endregion

# #region msgbox Functions

# def show_custom_error_message(parent_window, title, message):
#     error_message_window = tk.Toplevel()
#     error_message_window.transient(parent_window)
#     error_message_window.title(title)
#     error_message_window.resizable(False, False)  # Make the window non-resizable
#     #error_message_window.overrideredirect(True)  # Remove title bar and window controls
#     # error_message_window.wm_attributes('-toolwindow', 'true')

#     ttk.Label(error_message_window, text=message).pack(padx=10, pady=10)
#     ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    
#     BaseWindow.center_window(error_message_window)

#     error_message_window.grab_set()  # Make the window modal
#     error_message_window.focus_force()  # Focus on the error message window
#     parent_window.wait_window(error_message_window)  # Wait until the error message window is closed

# def show_custom_confirmation_message(parent_window, title, message):
#     confirmation_window = tk.Toplevel()
#     confirmation_window.transient(parent_window)
#     confirmation_window.title(title)
#     confirmation_window.resizable(False, False)  # Make the window non-resizable
#     # confirmation_window.wm_attributes('-toolwindow', 'true')
#     #confirmation_window.overrideredirect(True)  # Remove title bar and window controls
#     result = {'value': None}

#     def on_yes():
#         result['value'] = True
#         confirmation_window.destroy()

#     def on_no():
#         result['value'] = False
#         confirmation_window.destroy()

#     ttk.Label(confirmation_window, text=message).pack(padx=10, pady=10)
#     button_frame = ttk.Frame(confirmation_window)
#     button_frame.pack(pady=5)
#     ttk.Button(button_frame, text="Yes", command=on_yes).pack(side=tk.LEFT, padx=5)
#     ttk.Button(button_frame, text="No", command=on_no).pack(side=tk.RIGHT, padx=5)
#     # Bind the close button to on_no
#     confirmation_window.protocol("WM_DELETE_WINDOW", on_no)

#     BaseWindow.center_window(confirmation_window)
#     confirmation_window.grab_set()
#     confirmation_window.focus_force()
#     parent_window.wait_window(confirmation_window)

#     return result['value']

# #endregion

# #region Button Functions

def create_button_frame(master, button_info):
    '''
    button_info: A list of tuples, each containing the button label and command.
          Example: [("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)]
    Outside padding of the returned frame is all 0. There is only padding in between the buttons.
    '''
   
    button_frame = ttk.Frame(master)    
    gen_pad = 10
    
    # Configure grid layout
    button_frame.grid_rowconfigure(0, weight=1)
    for i in range(len(button_info)):
        button_frame.grid_columnconfigure(i, weight=1)
    
    # Create buttons based on button_info
    for index, (label, command) in enumerate(button_info):
        button = ttk.Button(button_frame, text=label, command=command)
        button.grid(row=0, column=index,
                    padx=(gen_pad if index != 0 else 0,
                          gen_pad if index != len(button_info) - 1 else 0),
                          pady=0, sticky="nsew")
    
    return button_frame

# #endregion



