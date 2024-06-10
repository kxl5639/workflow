# project_manager_delete_controller.py
from tkinter import messagebox
from project_manager.project_manager_model import session, ProjectManager, field_metadata #type:ignore
from utils import show_custom_error_message, show_custom_confirmation_message, refresh_table #type:ignore

def delete_project_manager(project_manager):
    try:
        session.delete(project_manager)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_project_managers(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one Project Manager to delete.")
        return
    
    project_manager_names = [f"{session.query(ProjectManager).get(item).first_name} {session.query(ProjectManager).get(item).last_name}" for item in selected_items]
    project_manager_names_str = "\n".join(project_manager_names)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete Project Manager {project_manager_names[0]}?"):
            project_manager_id = selected_items[0]
            project_manager = session.query(ProjectManager).get(project_manager_id)
            error_message = delete_project_manager(project_manager)
            if error_message:
                show_custom_error_message(tree, "Error", f"Error deleting Project Manager {project_manager_names[0]}: {error_message}")
            else:
                refresh_table(tree, ProjectManager, session, field_metadata)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete Project Managers:\n\n{project_manager_names_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete Project Managers:\n\n{project_manager_names_str}"):
                for project_manager_id in selected_items:
                    project_manager = session.query(ProjectManager).get(project_manager_id)
                    error_message = delete_project_manager(project_manager)
                    if error_message:
                        show_custom_error_message(tree, "Error", f"Error deleting Project Manager {project_manager_names[project_manager_names.index(f'{project_manager.first_name} {project_manager.last_name}')]}: {error_message}")
                        break
                refresh_table(tree, ProjectManager, session, field_metadata)




