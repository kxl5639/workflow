import tkinter as tk
from tkinter import Toplevel, Listbox, StringVar, Entry, END
from tkinter import Toplevel, ttk
from sqlalchemy.inspection import inspect
from components.buttons import create_addmodifydelete_buttons #type:ignore 
from design_eng.design_eng_model import session, DesignEng # type: ignore
from sales_eng.sales_eng_model import session, SalesEng # type: ignore
from project_manager.project_manager_model import session, ProjectManager # type: ignore
from mech_eng.mech_eng_model import session, MechEng # type: ignore
from mech_con.mech_con_model import session, MechCon # type: ignore

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

def create_tree_from_db_table(master,columns, session, model):    
    tree = ttk.Treeview(master,columns=columns, show='headings')

    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    populate_treeview(tree, model, session, columns)
    return tree

def refresh_table(tree, model, session, columns): #
    for item in tree.get_children():
        tree.delete(item)
    populate_treeview(tree, model, session, columns)

def create_entry_widget( #creates the entry box for add/modify. Determines if the entry box is a textbox, dropdown, etc....)
        window, frame, field, metadata, prefilled_data, session, field_width=15
        ):
    
    entry_method = metadata[field].get("entry_method", "manual")    
    table_ref = metadata[field].get("table_ref")   

    if table_ref: #Creates the dropdown or listbox data if the metadata is either dropdown or lookup
            # Dynamically get the model class based on table_ref
            model = globals().get(table_ref)                        
            output = []            
            if model:
                results = session.query(model).all()                
                # Get all attributes of the model for the dropdown                
                values = [column.key for column in inspect(model).mapper.column_attrs if column.key != 'id']                
                for row in results:
                    row_data = " ".join(str(getattr(row, column)) for column in values)                    
                    output.append(row_data)                        
                output.sort(key=lambda x: x.split()[0])

    entry = None

    def open_lookup_window(window):          
        lookup_window = Toplevel(frame)           
        lookup_window.title(f"Lookup {field.replace("_", " ").title()}")

        top_frame = ttk.Frame(lookup_window)
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        bottom_frame = ttk.Frame(lookup_window)
        bottom_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        #lookup_window.grid_rowconfigure(1, weight=1)
        #lookup_window.grid_columnconfigure(0, weight=1)

        lookup_label = ttk.Label(top_frame, text=field.replace("_", " ").title())
        lookup_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        lookup_var = StringVar()
        lookup_entry = ttk.Entry(top_frame, textvariable=lookup_var)
        lookup_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        top_frame.grid_columnconfigure(1, weight=1)

        result_listbox = Listbox(bottom_frame, width=50)
        result_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)

        def update_results(*args):
            lookup_term = lookup_var.get().lower()
            filtered_values = [value for value in output if lookup_term in value.lower()]
            result_listbox.delete(0, END)
            for value in filtered_values:
                result_listbox.insert(END, value)

        lookup_var.trace("w", update_results)

        def on_select(event):
            selected_value = result_listbox.get(result_listbox.curselection())
            entry.delete(0, END)
            entry.insert(0, selected_value)
            lookup_window.destroy()

        
        center_window(lookup_window)        
        lookup_window.focus_force() 
        lookup_entry.focus_set() 
        lookup_window.grab_set()  
        window.wait_window(lookup_window)  
        
        result_listbox.bind("<<ListboxSelect>>", on_select)
        
    if entry_method == "manual":
        entry = ttk.Entry(frame, width=field_width)        
        entry.insert(0, prefilled_data.get(field, ""))
    elif entry_method == "dropdown":        
        entry = ttk.Combobox(frame, values=output, state="readonly", width=field_width)
        entry.set(prefilled_data.get(field, ""))        
    elif entry_method == "lookup":
        entry = ttk.Entry(frame, width=field_width)
        entry.insert(0, prefilled_data.get(field, ""))
        entry.bind("<Button-1>", lambda event: open_lookup_window(window))
    else:
        # Default to manual if entry_method is not recognized
        entry = ttk.Entry(frame, width=field_width)
        entry.insert(0, prefilled_data.get(field, ""))
    
    return entry

def create_add_or_modify_window( #creates view for adding/modifying table entries
        window,
        metadata,
        session,
        window_title: str,
        prefilled_data,
        button_text,
        submit_callback,        
        field_width=20,
        placeholders=None
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

        entry = create_entry_widget(window,frame, field, metadata, prefilled_data, session, field_width)
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


def populate_treeview(tree, model, session, columns): 
    #Populates views with columns that have the display metadata = 1    

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch tree data
    tree_data = session.query(model).all()   

    # Insert tree_data into the treeview
    for tree_data in tree_data:
        values = tuple(getattr(tree_data, col) for col in columns)                
        tree.insert('', 'end', values=values, iid=tree_data.id)  # Use tree_data.id as the item identifier (iid)  
    