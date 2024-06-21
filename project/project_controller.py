from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
from utils import show_custom_error_message, show_custom_confirmation_message, num_record_selected, only_one_record_selected
import tkinter as tk
from datetime import datetime

#region Formatting data to pass to project tree
columns_to_display = ['project_number', 'submittal_date', 'client', 'scope', 'address',
               'project_manager', 'mechanical_engineer', 'mechanical_contractor', 'design_engineer', 'sales_engineer']

def update_table_data():

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

    return table_data

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

def modify_record_properly_selected(tree,session,model):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a record to modify.")
        return None
    if only_one_record_selected(tree) is True:
        record_id = selected_item[0]  # The item identifier (iid) is the project ID
        record = session.query(model).get(record_id)
        return record
    else:
        show_custom_error_message(tree, "Error", "Only one record can be selected to modify.")
        return None

def delete_records_properly_selected(tree,session,model):

    selected_items = tree.selection()
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one record to delete.")
        return None
    
    projects_numbers = []
    for item_id in selected_items:
        project_record = session.query(model).get(item_id)
        if project_record:
            project_number = str(getattr(project_record, 'project_number'))
            projects_numbers.append(project_number)
    projects_numbers_str = "\n".join(projects_numbers)

    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete record:\n\n {projects_numbers[0]}?\n") is False:
            return None, False
        else:            
            record_id = [selected_items[0]]            
            return record_id, True
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete delete records:\n\n{projects_numbers_str}\n") is False:
            return None, False
        else:
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete delete records:\n\n{projects_numbers_str}\n") is False:
                return None, False
            else:
                record_ids = []
                for record_id in selected_items:    
                    record_ids.append(record_id)                
                return record_ids, True

def is_valid_addmodd_data(master, entry_dict, is_modify): # Validates data to be added or updated to database

    #region Functions  
    def extract_data_from_dict(entry_dict, to_extract):        
            for entries in entry_dict.values():
                if to_extract in entries:
                    to_extract_widget = entries[to_extract]
                    to_extract_value = to_extract_widget.get().strip()                        
            return to_extract_value, to_extract_widget
    
    def has_blank_entries(master, entry_dict):
        # Define the table name mappings
        table_name_map = {
            'projects': 'Project Info',
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
            return False
        return True

    def is_invalid_date_entry(master, entry_dict):
        import re
        submit_date_str, submit_date_widget = extract_data_from_dict(entry_dict, 'submit_date')
        date_pattern = re.compile(r'^\d{2}/\d{2}/\d{2}$')
        filler_date = 'XX/XX/XX'
        if submit_date_str != filler_date:
            if not date_pattern.match(submit_date_str):
                show_custom_error_message(master, "Error", f"Invalid Date Format. Please enter the date in MM/DD/YY format or {filler_date} if submittal has not been submitted yet.")
                submit_date_widget.focus_set()
                submit_date_widget.selection_range(0, tk.END)
                return False
            return True
        return True 

    def exist_project_number(master, entry_dict):
        curr_project_number, project_number_widget = extract_data_from_dict(entry_dict, 'project_number')
        existing_project = session.query(Project).filter_by(project_number=curr_project_number).first()
        if existing_project:
            show_custom_error_message(master, "Error", f'Project Number {curr_project_number} already exist. It cannot be added again.')
            project_number_widget.focus_set()
            project_number_widget.selection_range(0, tk.END)
            return False
        return True
    #endregion
            
    # Check if project number already exists if we are in modify
    if not is_modify:
        if not exist_project_number(master, entry_dict):
            return False

    # Check for blank fields and provide pop up message
    if not has_blank_entries(master, entry_dict):
        return False
    

    #Validate Date format
    if not is_invalid_date_entry(master, entry_dict):
        return False    
    
    return True
