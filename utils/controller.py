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
        tree.insert('', 'end', values=values, iid=tree_data.id)  # Use tree_data.id as the item identifier (iid)  