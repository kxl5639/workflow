import tkinter as tk
from tkinter import Toplevel, ttk

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_custom_error_message(parent_window, title, message):
    error_message_window = Toplevel()
    error_message_window.transient(parent_window)
    error_message_window.title(title)
    error_message_window.resizable(False, False)  # Make the window non-resizable
    ttk.Label(error_message_window, text=message).pack(padx=10, pady=10)
    ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    center_window(error_message_window)

    error_message_window.grab_set()  # Make the window modal
    error_message_window.focus_force()  # Focus on the error message window
    parent_window.wait_window(error_message_window)  # Wait until the error message window is closed

def only_one_record_selected(tree): #record refers to a record in a table.
    selected_items = tree.selection()    
    if len(selected_items) > 1:
        return False
    else:
        return True

def show_custom_confirmation_message(parent_window, title, message):
    confirmation_window = Toplevel()
    confirmation_window.transient(parent_window)
    confirmation_window.title(title)
    confirmation_window.resizable(False, False)
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

    center_window(confirmation_window)
    confirmation_window.grab_set()
    confirmation_window.focus_force()
    parent_window.wait_window(confirmation_window)

    return result['value']

def columns_to_display(metadata):
    # Extract columns with display value set to 1
    return [field for field, meta in metadata.items() if meta['display'] == 1]    

def populate_treeview(tree, table, session, metadata): 
    #Populates views with columns that have the display metadata = 1
    columns = columns_to_display(metadata) 

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch design engineers
    design_eng = session.query(table).all()
    
    # Insert design engineers into the treeview
    for design_eng in design_eng:
        values = tuple(getattr(design_eng, col) for col in columns)
        tree.insert('', 'end', values=values, iid=design_eng.id)  # Use design_eng.id as the item identifier (iid)

def refresh_table(tree, table, session, metadata): #
    for item in tree.get_children():
        tree.delete(item)
    populate_treeview(tree, table, session, metadata)

def create_add_or_modify_window(window, metadata, prefilled_data, button_text, submit_callback):
    fields = metadata.keys()
    field_to_frame = {field: metadata[field]["frame"] for field in fields}

    entries = {}

    frames = {i: ttk.Frame(window, padding="10 10 10 10") for i in range(1, 5)}
    for i, frame in frames.items():
        frame.grid(row=0, column=(i-1)*2, padx=10, pady=10, sticky="n")

    # Add vertical separators between frames
    for i in range(1, 4):
        separator = ttk.Separator(window, orient='vertical')
        separator.grid(row=0, column=(i*2)-1, padx=(0, 10), pady=10, sticky='ns')

    window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        window.grid_columnconfigure(i*2, weight=1)

    row_counters = {i: 0 for i in range(1, 5)}
    first_entry = None
    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        
        entry.insert(0, prefilled_data.get(field, ""))
            
        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5)
        entries[field] = entry
        if first_entry is None:
            first_entry = entry
        row_counters[frame_index] += 1

    button_frame = ttk.Frame(window)
    button_frame.grid(row=1, column=0, columnspan=7, pady=10)

    submit_button = ttk.Button(button_frame, text=button_text, command=lambda: submit_callback(entries))
    submit_button.grid(row=0, column=0, padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
    cancel_button.grid(row=0, column=1, padx=10)

    center_window(window)

    if first_entry is not None:
        first_entry.focus_set()

    return entries