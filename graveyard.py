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
    tree = create_tree_from_db_table(window,['project_number', 'submittal_date', 'client', 'scope', 'address', 'project_manager', 'mechanical_engineer', 'mechanical_contractor', 'design_engineer', 'sales_engineer'],session,table)
    # # Create the treeview
    # columns = columns_to_display(field_metadata)
    # print(columns)
    # tree = ttk.Treeview(window, columns=columns, show='headings')

    # # Define the column headings and set a minimum width
    # for col in columns:
    #     tree.heading(col, text=col.replace("_", " ").title())
    #     tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    # # Fetch the entity data and insert it into the treeview
    # populate_treeview(tree, table, session, field_metadata)

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
    