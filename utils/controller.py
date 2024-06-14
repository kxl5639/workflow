def only_one_record_selected(tree): #record refers to a record in a table.
    selected_items = tree.selection()    
    if len(selected_items) > 1:
        return False
    else:
        return True
    
def refresh_table(tree, model, session, columns): #
    for item in tree.get_children():
        tree.delete(item)
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
        print(values)
        tree.insert('', 'end', values=values, iid=tree_data.id)  # Use tree_data.id as the item identifier (iid)  

# Fields to display in Add/Modify Project Window
def fields_data_from_dbtable(metadata):
    fields = metadata.keys()
    frame_ass = {field: metadata[field]["frame"] for field in fields}
    max_frames = max([value["frame"] for value in metadata.values()])        
    return fields, frame_ass, max_frames

# Gets entry method as specified by metadata. Field arguement is the particular field of a table
def get_entry_method_and_table_ref(field,metadata):
    entry_method = metadata[field].get("entry_method", "manual")
    table_ref = metadata[field].get("table_ref")   
    return entry_method, table_ref