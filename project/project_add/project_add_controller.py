# project_add_controller.py
from tkinter import messagebox, Toplevel, ttk
from project.project_model import session, Project
from project.project_utils import refresh_project_table
from utils import show_custom_error_message
from datetime import datetime

def add_project(formatted_entries):
    try:
        new_project = Project(**formatted_entries)
        session.add(new_project)
        session.commit()
        return None  # No error message
    except Exception as e:
        return str(e)  # Return the error message

def add_project_wrapper(entries, tree, add_window):
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        if not entry.get().strip():
            empty_fields.append(field.replace("_", " ").title())
            if first_empty_entry is None:
                first_empty_entry = entry

    if empty_fields:
        show_custom_error_message(add_window, "Error", f"The following fields cannot be empty:\n" + "\n" + "\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()
        return

    formatted_entries = {field: entry.get() for field, entry in entries.items()}
    
    submittal_date_str = formatted_entries.get("submittal_date")
 
    # Try to parse the date if it is not a placeholder
    if submittal_date_str != "XX/XX/XX":
        try:
            submittal_date = datetime.strptime(submittal_date_str, '%m/%d/%y').date()
            #submittal_date_str = submittal_date.isoformat()
            formatted_entries["submittal_date"] = submittal_date.strftime('%m/%d/%y')

        except ValueError:
            show_custom_error_message(add_window, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
            return

    error_message = add_project(formatted_entries)
    if error_message:
        messagebox.showerror("Error", error_message)
    else:
        refresh_project_table(tree)
        add_window.destroy()