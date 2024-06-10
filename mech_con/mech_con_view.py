import tkinter as tk
from tkinter import ttk
from components.buttons import create_addmodifydelete_buttons # type: ignore
from utils import create_table_window #type:ignore 
from mech_con.mech_con_add.mech_con_add_view import open_add_mech_con_window   # type: ignore
from mech_con.mech_con_modify.mech_con_modify_view import open_modify_mech_con_window # type: ignore 
from mech_con.mech_con_delete.mech_con_delete_controller import delete_selected_mech_cons # type: ignore
from mech_con.mech_con_model import MechCon, field_metadata, session # type: ignore

def create_mech_con_window():    
    create_table_window(
        window_title="Mechanical Contractors",
        table=MechCon,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_mech_con_window,
        modify_command=open_modify_mech_con_window,
        delete_command=delete_selected_mech_cons
    )
