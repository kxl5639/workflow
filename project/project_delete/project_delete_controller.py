# project_delete_controller.py
from tkinter import messagebox
from project.project_model import session, Project
from project.project_utils import refresh_project_table
from utils import show_custom_error_message, show_custom_confirmation_message, only_one_project_selected

def delete_project(project):
    try:
        session.delete(project)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_projects(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one project to delete.")
        return
    
    project_numbers = [session.query(Project).get(item).project_number for item in selected_items]
    project_numbers_str = "\n".join(project_numbers)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete project {project_numbers[0]}?"):
            project_id = selected_items[0]
            project = session.query(Project).get(project_id)
            error_message = delete_project(project)
            if error_message:
                show_custom_error_message(tree, "Error", error_message)
            else:
                refresh_project_table(tree)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete projects:\n\n{project_numbers_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning!\n\nPlease confirm you want to delete projects:\n\n{project_numbers_str}"):
                for project_id in selected_items:
                    project = session.query(Project).get(project_id)
                    error_message = delete_project(project)
                    if error_message:
                        show_custom_error_message(tree, "Error", error_message)
                        break
                refresh_project_table(tree)
