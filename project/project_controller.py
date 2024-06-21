from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
from utils import show_custom_error_message
import tkinter as tk
from datetime import datetime

#region Formatting data to pass to project tree
columns_to_display = ['project_number', 'submittal_date', 'client', 'scope', 'address',
               'project_manager', 'mechanical_engineer', 'mechanical_contractor', 'design_engineer', 'sales_engineer']

unformatted_table_data = session.query(
    Project.id,  # Include the primary key
    Project.project_number,
    Project.submit_date,
    Client.client_name,
    Client.scope,
    Client.address,
    ProjectManager.first_name,
    ProjectManager.last_name,
    MechanicalEngineer.name,
    MechanicalContractor.name,
    DesignEngineer.first_name,
    DesignEngineer.last_name,
    SalesEngineer.first_name,
    SalesEngineer.last_name
).join(Client, Project.client_id == Client.id)\
 .join(ProjectManager, Project.projectmanager_id == ProjectManager.id)\
 .join(MechanicalEngineer, Project.mechanicalengineer_id == MechanicalEngineer.id)\
 .join(MechanicalContractor, Project.mechanicalcontractor_id == MechanicalContractor.id)\
 .join(DesignEngineer, Project.designengineer_id == DesignEngineer.id)\
 .join(SalesEngineer, Project.salesengineer_id == SalesEngineer.id)\
 .all()

# Combine first and last names for project manager, design engineer, and sales engineer
table_data = [
    (
        project[0],  # Primary key
        project[1], project[2], project[3], project[4], project[5],
        f"{project[6]} {project[7]}", project[8], project[9],
        f"{project[10]} {project[11]}", f"{project[12]} {project[13]}"
    ) for project in unformatted_table_data
]

# Example usage
column_map = {
    "project_number": 1,
    "submit_date": 2,
    "client": 3,
    "client_scope": 4,
    "client_address": 5,
    "project_manager": 6,
    "mech_eng": 7,
    "mech_contractor": 8,
    "design_eng": 9,
    "sales_eng": 10
}
#endregion


def fetch_record_data(record_id):    
    project = session.query(Project).filter_by(id=record_id).first()
    client = session.query(Client).filter_by(id=project.client_id).first()
    pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
    me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
    mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
    de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
    se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
    return project, client, pm, me, mc, de, se

def fetch_names(model):
    return [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).all()]

def get_entry_data(entries):
    return {key: entry.get() for key, entry in entries.items()}

def set_entry_state(entry, state):
    entry.config(state=state)

def set_entry_text(entry_widget, text):
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, text)

def is_valid_data(master, entry_dict): # Validates data to be added or updated to database

    # Check for blank fields and provide pop up message
    if has_blank_entries(master, entry_dict):
        return False

    #Validate Date format
    if is_valid_date_entry(master, entry_dict):
        return True    
    

def has_blank_entries(master, entry_dict):
    # Define the table name mappings
    table_name_map = {
        'projects': 'Project',
        'clients': 'Client',
        'mechanicalengineers': 'Mechanical Engineer',
        'mechanicalcontractors': 'Mechanical Contractor'
    }

    # Define the label name mappings (example)
    label_name_map = {
        'project_number': 'Project Number',
        'em_type': 'EM Type',
        'job_phase': 'Job Phase',
        'submit_date': 'Submit Date',
        'client_name': 'Name',
        'me_name': 'Name',
        'mc_name': 'Name',
        'pm_name': 'Project Manager',
        'de_name': 'Design Engineer',
        'se_name': 'Sales Engineer'
    }

    # Define the function to check if an entry or combobox is empty
    def is_empty(widget):
        return not widget.get().strip()

    # Collect the empty fields information
    empty_fields = []
    first_empty_entry = None
    current_table = None

    for table, entries in entry_dict.items():
        for label, widget in entries.items():
            if is_empty(widget):
                # Get the human-readable table name
                human_readable_table = table_name_map.get(table, table)
                # Get the human-readable label name
                human_readable_label = label_name_map.get(label, label.replace('_', ' ').title())

                # Add a new line if the table changes
                if current_table != human_readable_table:
                    if current_table is not None:  # Not the first table
                        empty_fields.append("")  # Add a blank line to separate tables
                    current_table = human_readable_table

                empty_fields.append(f"{human_readable_table} - {human_readable_label}")
                if first_empty_entry is None:
                    first_empty_entry = widget

    if empty_fields:
        show_custom_error_message(master, "Error", f"The following fields cannot be empty:\n\n" + "\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()
        return True
    return False

def is_valid_date_entry(master, entry_dict):

    def extract_submit_dates(entry_dict):        
        for entries in entry_dict.values():
            if 'submit_date' in entries:
                submit_date_widget = entries['submit_date']
                submit_date_value = submit_date_widget.get().strip()                        
        return submit_date_value, submit_date_widget

    submit_date_str, submit_date_widget = extract_submit_dates(entry_dict)

    def validate_date_format(master, date_str):    
        if date_str != "XX/XX/XX":
            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
                return True  # Return formatted date and no error
            except ValueError:
                show_custom_error_message(master, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
                submit_date_widget.focus_set()
                submit_date_widget.selection_range(0, tk.END)
                return False
        return True
    
    if validate_date_format(master, submit_date_str):
        return True
    return False
        
        




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
 
# def validate_date_format(master, date_str):    
#     if date_str != "XX/XX/XX":
#         try:
#             date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
#             return date_obj.strftime('%m/%d/%y'), None  # Return formatted date and no error
#         except ValueError:
#             show_custom_error_message(master, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
#             return None, "Invalid Date Format"
#     return date_str, None  # Return the original placeholder and no error





# for db_field in db_fields:  
# # Creates the label widgets iteratively      
#     frame_index = frame_assoc[db_field] #extracts the frame that the current db_field should be in
#     dividing_frame = dividing_frames[frame_index]         
#     label = ttk.Label(dividing_frame, text=db_field.replace("_", " ").title())
#     label.grid(row=row_counters[frame_index], column=0, padx=(0,10), pady=5, sticky=tk.W)

# # Creates entry widgets iteratively        
#     # For each db_field, we are going to get the entry method
#         #and if entry method is dropdown or lookup, we will also grab which table
#         #we will pull the data from to populate said dropdown or lookup                
#     # Generate the entry widgets    
#     if model.__tablename__ != 'tblProject':            
#         entry_method = 'manual'
#     else:
#         entry_method, dropdown_or_tree_data = get_entry_method_and_table_ref(db_field,metadata,session)        
#     match entry_method:
#         case 'manual':
#             entry_widg = ttk.Entry(dividing_frame,width = entry_widget_width)
#             entry_widg.insert(0, entry_data.get(db_field, ""))
#             entry_widg.grid(row=row_counters[frame_index], column=1, padx=10, pady=5, sticky=tk.W)
#             entries[db_field] = entry_widg