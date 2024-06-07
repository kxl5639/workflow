from datetime import datetime
from tkinter import messagebox, Toplevel, ttk
from project.project_model import session, Project, field_metadata
from utils import show_custom_error_message

def project_columns_to_display():
    # Extract columns with display value set to 1
    return [field for field, meta in field_metadata.items() if meta['display'] == 1]

def fetch_projects():
    return session.query(Project).all()

def populate_treeview_with_projects(tree):
    # Define the columns
    columns = project_columns_to_display()

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch projects
    projects = fetch_projects()
    
    # Insert projects into the treeview
    for project in projects:
        values = tuple(getattr(project, col) for col in columns)
        tree.insert('', 'end', values=values, iid=project.id)  # Use project.id as the item identifier (iid)

def refresh_project_table(tree):
    for item in tree.get_children():
        tree.delete(item)
    populate_treeview_with_projects(tree)

def validate_date_format(date_str, parent_window):
    if date_str != "XX/XX/XX":
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
            return date_obj.strftime('%m/%d/%y'), None  # Return formatted date and no error
        except ValueError:
            show_custom_error_message(parent_window, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
            return None, "Invalid Date Format"
    return date_str, None  # Return the original placeholder and no error