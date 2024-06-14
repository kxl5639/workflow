from sqlalchemy.inspection import inspect
from configs import testing

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

