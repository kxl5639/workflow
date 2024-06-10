import tkinter as tk
from tkinter import Toplevel, ttk
from components.buttons import create_addmodifydelete_buttons #type:ignore 
from design_eng.design_eng_model import session, DesignEng # type: ignore
from sales_eng.sales_eng_model import session, SalesEng # type: ignore
from project_manager.project_manager_model import session, ProjectManager # type: ignore

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

def create_table_window( #creates the main view to show table data
        window_title: str,
        table,
        field_metadata: dict,
        session,
        add_command,
        modify_command,
        delete_command):
    
    window = tk.Toplevel()
    window.title(window_title)

    # Create the treeview
    columns = columns_to_display(field_metadata)
    tree = ttk.Treeview(window, columns=columns, show='headings')

    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    # Fetch the entity data and insert it into the treeview
    populate_treeview(tree, table, session, field_metadata)

    tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        window,
        add_command=lambda: add_command(tree),
        modify_command=lambda: modify_command(tree),
        delete_command=lambda: delete_command(tree)
    )
    button_frame.pack(pady=10)
  
    # Center the window after adding widgets
    center_window(window)

    # Bring the window to the front and set focus
    window.focus_force()

def create_add_or_modify_window( #creates view for adding/modifying tables
        window,
        metadata,
        window_title: str,
        prefilled_data,
        button_text,
        submit_callback
        ):
    
    window.title(window_title)

    fields = metadata.keys()
    field_to_frame = {field: metadata[field]["frame"] for field in fields}

    entries = {}

    #Calculate the max number of frames from the metadata
    max_frames = max([value["frame"] for value in metadata.values()])

    frames = {i: ttk.Frame(window, padding="5 5 5 5") for i in range(1, max_frames+1)}
    for i, frame in frames.items():
        frame.grid(row=0, column=(i-1)*2, padx=10, pady=10, sticky="n")

    # Add vertical separators between frames
    for i in range(1, max_frames):
        separator = ttk.Separator(window, orient='vertical')
        separator.grid(row=0, column=(i*2)-1, padx=(0, 10), pady=10, sticky='ns')

    window.grid_rowconfigure(0, weight=1)
    for i in range(max_frames):
        window.grid_columnconfigure(i*2, weight=1)

    row_counters = {i: 0 for i in range(1, max_frames+1)}
    first_entry = None

    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)

        field_width = 15
        if field == "design_engineer":
            design_engs = session.query(DesignEng).all()
            design_eng_names = [f"{de.first_name} {de.last_name}" for de in design_engs]
            entry = ttk.Combobox(frame, values=design_eng_names, state="readonly", width = field_width)
            entry.set(prefilled_data.get(field, ""))
        elif field == "sales_engineer":
            sales_engs = session.query(SalesEng).all()
            sales_eng_names = [f"{de.first_name} {de.last_name}" for de in sales_engs]
            entry = ttk.Combobox(frame, values=sales_eng_names, state="readonly", width = field_width)
            entry.set(prefilled_data.get(field, ""))
        elif field == "project_manager":
            project_managers = session.query(ProjectManager).all()
            project_manager_names = [f"{de.first_name} {de.last_name}" for de in project_managers]
            entry = ttk.Combobox(frame, values=project_manager_names, state="readonly", width = field_width)
            entry.set(prefilled_data.get(field, ""))
        else:
            entry = ttk.Entry(frame, width = field_width)
            entry.insert(0, prefilled_data.get(field, ""))

        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
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