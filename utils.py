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

def create_tree_frame_from_db_table(master,columns, session, model):    
    tree_frame = ttk.Frame(master)    
    tree_frame.grid_rowconfigure(0,weight=1) 
    tree_frame.grid_columnconfigure(0,weight=1) 
    
    tree = ttk.Treeview(tree_frame,columns=columns, show='headings')    
    tree.grid(row=0,column=0, sticky='nsew')
    
    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=10, anchor='center')  # Initial minimum width

    resize_max_width_of_tree_columns(tree, session,model,columns)

    populate_treeview(tree, model, session, columns)
    tree_frame.tree = tree
    return tree_frame

def create_standard_tree_but_frame(master, columns, session, model, add_command=None, modify_command=None, delete_command=None ):
    tree_addmoddel_frame = ttk.Frame(master, name='tree_addmoddel_frame')        
    tree_addmoddel_frame.grid_rowconfigure((0), weight=1)
    tree_addmoddel_frame.grid_rowconfigure((1), weight=0)
    tree_addmoddel_frame.grid_columnconfigure(0, weight=1)    
    
    tree_frame = create_tree_frame_from_db_table(tree_addmoddel_frame,columns, session, model)
    tree_frame.grid(row=0, padx=0, pady=(0,20), sticky="nsew")    

    addmoddel_buttons_frame = create_dynamic_button_frame(tree_addmoddel_frame,[("Add", add_command), ("Modify", modify_command), ("Delete", delete_command)])
    addmoddel_buttons_frame.grid(row=1, column=0, pady=0, padx=0)    

    tree_addmoddel_frame.tree_frame = tree_frame
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

def create_add_or_modify_frame(master, entry_data, model, metadata, session,return_dividing_frames=False):    

    # Obtain list of fields from Project table in DB to create labels, frame association, max frames
    db_fields, frame_assoc, max_frames = fields_data_from_dbtable(metadata)    

    # Create frame to be returned
    add_or_mod_frame = ttk.Frame(master)    
    add_or_mod_frame.grid_rowconfigure(0, weight=1)    
    for i in range(max_frames):
        add_or_mod_frame.grid_columnconfigure(i*2, weight=1)

    # Creates the number of grids to separate TMBA info, Project info, Mech Eng info, and Mech Con info
    dividing_frames = {i: ttk.Frame(add_or_mod_frame) for i in range(1, max_frames+1)} # Note that range starts at 1 and ends at max_frames
    # Places frames in add_or_mod_frame frame  
    for i, dividing_frame in dividing_frames.items():        
        dividing_frame.grid(row=0, column=(i-1)*2, padx=10, pady=0, sticky="nsew")  
        dividing_frame.grid_columnconfigure(0, weight=0)  
        dividing_frame.grid_columnconfigure(1, weight=1)  
            
    # Add vertical separators between frames
    for i in range(1, max_frames):
        separator = ttk.Separator(add_or_mod_frame, orient='vertical')
        separator.grid(row=0, column=(i*2)-1, padx=(5), pady=0, sticky='ns')

    # Initializing variables to start generating the labels and entries
    row_counters = {i: 0 for i in range(1, max_frames+1)}
    first_entry = None
    entry_widget_width = 15
    entries = {} # Eventually collects all the entries that will be submitted via the Add or Modify button    

    for db_field in db_fields:  
    # Creates the label widgets iteratively      
        frame_index = frame_assoc[db_field] #extracts the frame that the current db_field should be in
        dividing_frame = dividing_frames[frame_index]         
        label = ttk.Label(dividing_frame, text=db_field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=(0,10), pady=5, sticky=tk.W)

    # Creates entry widgets iteratively        
        # For each db_field, we are going to get the entry method
            #and if entry method is dropdown or lookup, we will also grab which table
            #we will pull the data from to populate said dropdown or lookup                
        # Generate the entry widgets    
        if model.__tablename__ != 'tblProject':            
            entry_method = 'manual'
        else:
            entry_method, dropdown_or_tree_data = get_entry_method_and_table_ref(db_field,metadata,session)        
        match entry_method:
            case 'manual':
                entry_widg = ttk.Entry(dividing_frame,width = entry_widget_width)
                entry_widg.insert(0, entry_data.get(db_field, ""))
                entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
                entries[db_field] = entry_widg
            case 'dropdown':
                entry_widg = ttk.Combobox(dividing_frame, values=dropdown_or_tree_data, state="readonly", width=entry_widget_width)
                entry_widg.set(entry_data.get(db_field, ""))        
            # case 'lookup':
            #     entry_widg = ttk.Entry(dividing_frame, width=entry_widget_width)
            #     entry_widg.insert(0, entry_data.get(db_field, ""))
            #     entry_widg.bind("<Button-1>", lambda event: open_lookup_window(window))                
            case _:
                entry_widg = ttk.Entry(dividing_frame,width = entry_widget_width)
                entry_widg.insert(0, entry_data.get(db_field, ""))
                entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
                entries[db_field] = entry_widg
        
            # if entry_method == "manual":
            #         entry_widg = ttk.Entry(dividing_frame,width = entry_widget_width)
            #         entry_widg.insert(0, entry_data.get(db_field, ""))
            #         entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
            #         entries[db_field] = entry_widg
            # elif entry_method == "dropdown":        
            #     entry_widg = ttk.Combobox(dividing_frame, values=dropdown_or_tree_data, state="readonly", width=entry_widget_width)
            #     entry_widg.set(entry_data.get(db_field, ""))   
            # # elif entry_method == "lookup":
            # #     entry_widg = ttk.Entry(dividing_frame, width=entry_widget_width)
            # #     entry_widg.insert(0, entry_data.get(db_field, ""))
            # #     entry_widg.bind("<Button-1>", lambda event: open_lookup_window(window))
            # else:
            #     # Default to manual if entry_method is not recognized
            #     entry_widg = ttk.Entry(dividing_frame, width=entry_widget_width)
            #     entry_widg.insert(0, entry_data.get(db_field, ""))

        entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky='ew')
        entries[db_field] = entry_widg

        if first_entry is None:
            first_entry = entry_widg
        
        row_counters[frame_index] += 1

    if first_entry is not None:
        first_entry.focus_set()       
    
    if return_dividing_frames:
        return add_or_mod_frame, entries, dividing_frames, row_counters
    else:
        return add_or_mod_frame, entries

#endregion

#region Controller Functions

def only_one_record_selected(tree): #record refers to a record in a table.
    selected_items = tree.selection()    
    if len(selected_items) > 1:
        return False
    else:
        return True

def resize_max_width_of_tree_columns(tree, session,model,columns):
    # Fetch data from the database
    data = session.query(model).all()

    # Determine the maximum width needed for each column
    column_widths = {col: len(col.replace("_", " ").title()) * 10 for col in columns}
    
    for row in data:
        values = [str(getattr(row, col)) for col in columns]
        for col, value in zip(columns, values):
            column_widths[col] = max(column_widths[col], len(value) * 10)
    
    # Adjust column widths based on the content
    for col in columns:
        tree.column(col, width=column_widths[col])

def refresh_table(tree, model, session, columns): #
    for item in tree.get_children():
        tree.delete(item)

    resize_max_width_of_tree_columns(tree, session,model,columns)

    populate_treeview(tree, model, session, columns)

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

def generate_default_entry_data(metadata): #This function determines the default data when "Add New Project" window is opened.
    default_entry_data = {}
    if testing:
        for field in metadata.keys():
            if field == "submittal_date":
                default_entry_data[field] = "XX/XX/XX"
            elif field == "design_engineer":
                default_entry_data[field] = "Kevin Lee"
            else:
                default_entry_data[field] = "TESTING"
    else:
        for field in metadata.keys():
            default_entry_data[field] = metadata[field]["default"]
    return default_entry_data

# Fields to display in Add/Modify Project Window
def fields_data_from_dbtable(metadata):
    fields = metadata.keys()
    frame_ass = {field: metadata[field]["frame"] for field in fields}
    max_frames = max([value["frame"] for value in metadata.values()])        
    return fields, frame_ass, max_frames

# Gets entry method as specified by metadata. Field arguement is the particular field of a table
def get_entry_method_and_table_ref(field,metadata,session):
    entry_method = metadata[field].get("entry_method", "manual")
    table_ref = metadata[field].get("table_ref")    
    #Creates the dropdown or listbox data if the metadata is either dropdown or lookup
    dropdown_or_tree_data = []
    if table_ref:
        # Dynamically get the model class based on table_ref
        model = globals().get(table_ref)        
        if model:
            results = session.query(model).all()                
            # Get all attributes of the model for the dropdown                
            values = [column.key for column in inspect(model).mapper.column_attrs if column.key != 'id']                
            for row in results:
                row_data = " ".join(str(getattr(row, column)) for column in values)                    
                dropdown_or_tree_data.append(row_data)                        
            dropdown_or_tree_data.sort(key=lambda x: x.split()[0]) 
            print(dropdown_or_tree_data)
    return entry_method, dropdown_or_tree_data

def prep_data_entry(master, entries):     
    #Picks up empty fields and displays an error message to the user
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        entry_content = entry.get().strip()
        if not entry_content: 
            empty_fields.append(field.replace("_", " ").title())             
            if first_empty_entry is None:
                first_empty_entry = entry
    if empty_fields:
        show_custom_error_message(master, "Error", f"The following fields cannot be empty:\n" + "\n" + "\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()
        return None, empty_fields

    formatted_entries = {field: entry.get() for field, entry in entries.items()}  
    submittal_date_str = formatted_entries.get("submittal_date")
 
    if submittal_date_str is not None:
        # Validate the date format
        formatted_date, error_message = validate_date_format(master, submittal_date_str)
        if error_message:
            return None, error_message
        formatted_entries["submittal_date"] = formatted_date 

    return formatted_entries, None
 
def validate_date_format(master, date_str):    
    if date_str != "XX/XX/XX":
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
            return date_obj.strftime('%m/%d/%y'), None  # Return formatted date and no error
        except ValueError:
            show_custom_error_message(master, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
            return None, "Invalid Date Format"
    return date_str, None  # Return the original placeholder and no error

def modify_record_properly_selected(tree,session,model):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a record to modify.")
        return
    if only_one_record_selected(tree) is True:
        record_id = selected_item[0]  # The item identifier (iid) is the project ID
        record = session.query(model).get(record_id)
        return record
    else:
        show_custom_error_message(tree, "Error", "Only one record can be selected to modify.")
        return    

def delete_record_properly_selected(tree, session, model, *fields):
    selected_records = tree.selection()
    if not selected_records:
        show_custom_error_message(tree, "Error", "Please select at least one record to delete.")
        return None, False
    
    # Creates a string of list of record(s) that are selected to be deleted    
    records_labels = []
    for item in selected_records:
        instance = session.query(model).get(item)
        if instance:
            record_label = " ".join(str(getattr(instance, attr)) for attr in fields)
            records_labels.append(record_label)
    records_labels_str = "\n".join(records_labels)
    
    if len(selected_records) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete record:\n\n {records_labels[0]}?\n") is False:
            return None, False
        else:            
            record_id = [selected_records[0]]            
            return record_id, True
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete delete records:\n\n{records_labels_str}\n") is False:
            return None, False
        else:
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete delete records:\n\n{records_labels_str}\n") is False:
                return None, False
            else:
                record_ids = []
                for record_id in selected_records:    
                    record_ids.append(record_id)                
                return record_ids, True    

#endregion

#region Model Functions

def add_record_to_table(model,session,formatted_entries):
    try:
        new_record = model(**formatted_entries)
        session.add(new_record)
        session.commit()
        return None  # No error message
    except Exception as e:
        if str(e):  # Return the error message
            messagebox.showerror("Error", 'Unable to add entry.')

def update_table(session,formatted_entries,selected_record):
    for field, value in formatted_entries.items():
        setattr(selected_record, field, value)
    session.commit()

def delete_record(record, session):
    try:
        session.delete(record)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None
#endregion

#region msgbox Functions

def show_custom_error_message(parent_window, title, message):
    error_message_window = Toplevel()
    error_message_window.transient(parent_window)
    error_message_window.title(title)
    error_message_window.resizable(False, False)  # Make the window non-resizable
    #error_message_window.overrideredirect(True)  # Remove title bar and window controls
    error_message_window.wm_attributes('-toolwindow', 'true')

    ttk.Label(error_message_window, text=message).pack(padx=10, pady=10)
    ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    
    center_window(error_message_window)

    error_message_window.grab_set()  # Make the window modal
    error_message_window.focus_force()  # Focus on the error message window
    parent_window.wait_window(error_message_window)  # Wait until the error message window is closed

def show_custom_confirmation_message(parent_window, title, message):
    confirmation_window = Toplevel()
    confirmation_window.transient(parent_window)
    confirmation_window.title(title)
    confirmation_window.resizable(False, False)  # Make the window non-resizable
    confirmation_window.wm_attributes('-toolwindow', 'true')
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

def create_dynamic_button_frame(master, button_info):
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

def create_add_modify_window(master, model, session, metadata, columns_to_display, title='Add New _________', button_text='Add or Modify?'):
    
    # Tree created from the parent window, need it so that we can pass it to the buttons to refresh the tree when we add/modify data the table
        # For modifying option, tree is used to determine if user has selected something    
    table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree    

    # If modifying, this sets the entry data, aka existing record data, as well as the selected record being modified
    if button_text == 'Modify':   
        #Run checks to see if only 1 entry is selected
        selected_record = modify_record_properly_selected(table_window_tree,session,model)        
        if selected_record is None:            
            return
        else:            
            selected_record_data = {field: getattr(selected_record, field) for field in selected_record.__table__.columns.keys()}
            entry_data = selected_record_data
    else:
        default_entry_data = generate_default_entry_data(metadata)        
        entry_data = default_entry_data            
            
    # Creates the window
    add_mod_window = tk.Toplevel()
    add_mod_window.title(title)    
    add_mod_window.grid_rowconfigure(0, weight=1)
    add_mod_window.grid_columnconfigure(0, weight=1)
    add_mod_window.resizable(height=False,width=True)

    add_proj_frame, project_entries, dividing_frame, max_rows_in_dividing_frames = create_add_or_modify_frame(add_mod_window,
                                                                                                                entry_data,
                                                                                                                model,
                                                                                                                metadata,
                                                                                                                session,
                                                                                                                True)
    add_proj_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    
    
    # Adds buttons for adding new mechanical engineers/contractors
    if model.__tablename__ == 'tblProject':
        # Adds an "Add Eng" button to the column of engineers
        mech_eng_frame = dividing_frame[3] # [3] represents the column that the mechanical engineer info is in
        butt_row = max_rows_in_dividing_frames[3]+1    
        add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Engineer', None)])
        add_mech_eng_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

        # Adds an "Add Eng" button to the column of engineers
        mech_con_frame = dividing_frame[4]
        butt_row = max_rows_in_dividing_frames[4]+1    
        add_mech_con_but = create_dynamic_button_frame(mech_con_frame,[('Add Contractor', None)])
        add_mech_con_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    # Creates the buttons at the bottom of the screen
    button_frame = create_dynamic_button_frame(add_mod_window, [(button_text, lambda:add_mod_button_cmd(button_text)),
                                                            ('Cancel', add_mod_window.destroy)])
    button_frame.grid(row=1,column=0,padx=10,pady=(0,10))
    #Function that defines what the button click will do
    def add_mod_button_cmd(button_text):     
        formatted_entries, error_message=prep_data_entry(add_mod_window,project_entries)            
        if error_message:
            return
        if button_text == 'Add':                      
            add_record_to_table(model,session,formatted_entries)
            refresh_table(table_window_tree, model, session,columns_to_display)
            add_mod_window.destroy()
        else:
            update_table(session,formatted_entries,selected_record)
            refresh_table(table_window_tree, model, session,columns_to_display)
            add_mod_window.destroy()


    center_window(add_mod_window) 
    add_mod_window.grab_set()     
    add_mod_window.focus_force()  
    master.wait_window(add_mod_window)

    #endregion
