import tkinter as tk
from tkinter import Toplevel, Listbox, StringVar, Entry, END
from tkinter import Toplevel, ttk
from sqlalchemy.inspection import inspect
from utils.controller import populate_treeview
from utils.button import create_addmodifydelete_button_frame, create_dynamic_button_frame
from utils.controller import fields_data_from_dbtable, get_entry_method_and_table_ref

def center_window(window):        
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_tree_frame_from_db_table(master,columns, session, model):    
    tree_frame = ttk.Frame(master)    
    tree_frame.grid_rowconfigure(0,weight=1) 
    tree_frame.grid_columnconfigure(0,weight=1) 
    
    tree = ttk.Treeview(tree_frame,columns=columns, show='headings')    
    tree.grid(row=0,column=0, sticky='nsew')
    
    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    populate_treeview(tree, model, session, columns)
    return tree_frame

def create_standard_tree_but_frame(master, columns, session, model, add_command=None, modify_command=None, delete_command=None ):
    tree_addmoddel_frame = ttk.Frame(master)        
    tree_addmoddel_frame.grid_rowconfigure((0), weight=1)
    tree_addmoddel_frame.grid_rowconfigure((1), weight=0)
    tree_addmoddel_frame.grid_columnconfigure(0, weight=1)    
    
    tree_frame = create_tree_frame_from_db_table(tree_addmoddel_frame,columns, session, model)
    tree_frame.grid(row=0, padx=0, pady=(0,20), sticky="nsew")    

    #addmoddel_buttons_frame = create_addmodifydelete_button_frame(tree_addmoddel_frame, add_command, modify_command=None, delete_command=None)    
    addmoddel_buttons_frame = create_dynamic_button_frame(tree_addmoddel_frame,[("Add", add_command), ("Modify", None), ("Delete", None)])
    addmoddel_buttons_frame.grid(row=1, column=0, pady=0, padx=0)
    #addmoddel_buttons_frame.grid(row=1, column=0, pady=0, padx=0, sticky="nsew")

    return tree_addmoddel_frame

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

def create_add_or_modify_window( #creates frame for adding/modifying table entries
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
    
    print("Place holder to prevent app call issues")

def create_add_or_modify_frame(master, metadata, default_entry_data,session):

    # Obtain list of fields from Project table in DB to create labels, frame association, max frames
    db_fields, frame_assoc, max_frames = fields_data_from_dbtable(metadata)

    # Create frame to me return
    add_or_mod_frame = ttk.Frame(master)    
    add_or_mod_frame.grid_rowconfigure(0, weight=1)    
    for i in range(max_frames):
        add_or_mod_frame.grid_columnconfigure(i*2, weight=1)

    # Creates the number of grids to separate TMBA info, Project info, Mech Eng info, and Mech Con info
    dividing_frames = {i: ttk.Frame(add_or_mod_frame) for i in range(1, max_frames+1)} # Note that range starts at 1 and ends at max_frames
    # Places frames in add_or_mod_frame frame  
    for i, dividing_frame in dividing_frames.items():        
        dividing_frame.grid(row=0, column=(i-1)*2, padx=10, pady=0, sticky="nsew")    
            
    # Add vertical separators between frames
    for i in range(1, max_frames):
        separator = ttk.Separator(add_or_mod_frame, orient='vertical')
        separator.grid(row=0, column=(i*2)-1, padx=(5), pady=0, sticky='ns')

    # Initializing variables to start generating the labels and entries
    row_counters = {i: 0 for i in range(1, max_frames+1)}
    first_entry = None
    entry_widget_width = 15
    entries = {} # Eventually collects all the entries that will be submitted to the Add or Modify button

    for db_field in db_fields:  
    # Creates the label widgets iteratively      
        frame_index = frame_assoc[db_field] #extracts the frame that the current db_field should be in
        dividing_frame = dividing_frames[frame_index] 
        #dividing_frame.grid_rowconfigure(row_counters[frame_index], weight=1) #Not sure if I want this to happen, this allows labels to stretch
        label = ttk.Label(dividing_frame, text=db_field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=(0,10), pady=5, sticky=tk.W)

    # Creates entry widgets iteratively        
        # For each db_field, we are going to get the entry method
            #and if entry method is dropdown or lookup, we will also grab which table
            #we will pull the data from to populate said dropdown or lookup
        entry_method, dropdown_or_tree_data = get_entry_method_and_table_ref(db_field,metadata,session)        
        # Generate the entry widgets
        if entry_method == "manual":
                entry_widg = ttk.Entry(dividing_frame,width = entry_widget_width)
                entry_widg.insert(0, default_entry_data.get(db_field, ""))
                entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
                entries[db_field] = entry_widg
        elif entry_method == "dropdown":        
            entry_widg = ttk.Combobox(dividing_frame, values=dropdown_or_tree_data, state="readonly", width=entry_widget_width)
            entry_widg.set(default_entry_data.get(db_field, ""))   
        # elif entry_method == "lookup":
        #     entry_widg = ttk.Entry(dividing_frame, width=entry_widget_width)
        #     entry_widg.insert(0, default_entry_data.get(db_field, ""))
        #     entry_widg.bind("<Button-1>", lambda event: open_lookup_window(window))
        else:
            # Default to manual if entry_method is not recognized
            entry_widg = ttk.Entry(dividing_frame, width=entry_widget_width)
            entry_widg.insert(0, default_entry_data.get(db_field, ""))
        entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
        entries[db_field] = entry_widg

        if first_entry is None:
            first_entry = entry_widg
        
        row_counters[frame_index] += 1

    if first_entry is not None:
        first_entry.focus_set()       
    
    return add_or_mod_frame
