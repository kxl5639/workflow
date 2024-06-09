from tkinter import messagebox
from project.project_model import session, Project, field_metadata #type:ignore
from project.project_utils import validate_date_format #type:ignore
from utils import show_custom_error_message, only_one_record_selected, refresh_table #type:ignore

def modify_project_properly_selected(tree):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a project to modify.")
        return
    if only_one_record_selected(tree) is True:
        project_id = selected_item[0]  # The item identifier (iid) is the project ID
        project = session.query(Project).get(project_id)
        return project
    else:
        show_custom_error_message(tree, "Error", "Only one project can be selected to modify.")
        return     

def modify_project_wrapper(entries, project, modify_window, tree):
    # Check if any entry is empty
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        if not entry.get().strip():
            empty_fields.append(field.replace("_", " ").title())
            if first_empty_entry is None:
                first_empty_entry = entry

    if empty_fields:
        show_custom_error_message(modify_window, "Error", f"The following fields cannot be empty:\n" + "\n" +"\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()  # Set focus to the first empty entry widget
        return

    # Convert entries keys to the expected format with underscores
    formatted_entries = {field: entry.get() for field, entry in entries.items()}

    submittal_date_str = formatted_entries.get("submittal_date")
    # Validate the date format
    formatted_date, error_message = validate_date_format(submittal_date_str, modify_window)
    if error_message:
        return
    formatted_entries["submittal_date"] = formatted_date

    for field, value in formatted_entries.items():
        setattr(project, field, value)

    session.commit()
    refresh_table(tree, Project, session, field_metadata)
    
    modify_window.destroy()