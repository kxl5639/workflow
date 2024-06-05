from tkinter import messagebox
from project.project_model import session, Project
from project.project_modify.project_modify_view import open_modify_project_window
from project.project_utils import populate_treeview_with_projects, refresh_project_table

def get_selected_project(tree):
    selected_item = tree.selection()    
    if not selected_item:
        return None
    project_id = selected_item[0]  # The item identifier (iid) is the project ID    
    project = session.query(Project).get(project_id)
    return project

def modify_project(tree):
    project = get_selected_project(tree)
    if project is None:
        messagebox.showerror("Error", "Please select a project to modify.")
        return

    def update_project(project, updated_values):
        for field, value in updated_values.items():
            setattr(project, field, value)
        session.commit()
        refresh_project_table(tree)

    open_modify_project_window(project, update_command=update_project)
