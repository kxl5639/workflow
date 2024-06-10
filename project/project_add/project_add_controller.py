# project_add_controller.py
from tkinter import messagebox, Toplevel, ttk
from datetime import datetime
from project.project_model import session, Project, field_metadata #type:ignore
from project.project_utils import validate_date_format #type:ignore
from utils import show_custom_error_message, refresh_table #type:ignore

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
 
    # Validate the date format
    formatted_date, error_message = validate_date_format(submittal_date_str, add_window)
    if error_message:
        return

    formatted_entries["submittal_date"] = formatted_date

    error_message = add_project(formatted_entries)
    if error_message:
        messagebox.showerror("Error", error_message)
    else:
        refresh_table(tree, Project, session, field_metadata)
        add_window.destroy()