import tkinter as tk
from tkinter import ttk
from utils import create_table_window #type:ignore 
from project.project_add.project_add_view import open_add_project_window #type:ignore 
from project.project_modify.project_modify_view import open_modify_project_window #type:ignore 
from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
from project.project_model import Project, field_metadata, session # type: ignore


def create_project_window():    
    create_table_window(
        window_title="Projects",
        table=Project,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_project_window,
        modify_command=open_modify_project_window,
        delete_command=delete_selected_projects
    )