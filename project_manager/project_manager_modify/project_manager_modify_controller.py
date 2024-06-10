from tkinter import messagebox
from project_manager.project_manager_model import session, ProjectManager, field_metadata #type:ignore
from utils import show_custom_error_message, only_one_record_selected, refresh_table #type:ignore

def modify_project_manager_properly_selected(tree):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a Project Manager to modify.")
        return
    if only_one_record_selected(tree) is True:
        project_manager_id = selected_item[0]  # The item identifier (iid) is the project_manager ID
        project_manager = session.query(ProjectManager).get(project_manager_id)
        return project_manager
    else:
        show_custom_error_message(tree, "Error", "Only one Project Manager can be selected to modify.")
        return     

def modify_project_manager_wrapper(entries, project_manager, modify_window, tree):
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
    
    for field, value in formatted_entries.items():
        setattr(project_manager, field, value)

    session.commit()
    refresh_table(tree, ProjectManager, session, field_metadata)
    
    modify_window.destroy()