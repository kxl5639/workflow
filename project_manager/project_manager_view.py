import tkinter as tk
from tkinter import ttk
from components.buttons import create_addmodifydelete_buttons # type: ignore
from utils import create_table_window #type:ignore 
from project_manager.project_manager_add.project_manager_add_view import open_add_project_manager_window   # type: ignore
from project_manager.project_manager_modify.project_manager_modify_view import open_modify_project_manager_window # type: ignore 
from project_manager.project_manager_delete.project_manager_delete_controller import delete_selected_project_managers # type: ignore
from project_manager.project_manager_model import ProjectManager, field_metadata, session # type: ignore

def create_project_manager_window():    
    create_table_window(
        window_title="Project Manager Engineers",
        table=ProjectManager,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_project_manager_window,
        modify_command=open_modify_project_manager_window,
        delete_command=delete_selected_project_managers
    )
