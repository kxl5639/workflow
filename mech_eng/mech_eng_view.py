import tkinter as tk
from tkinter import ttk
from components.buttons import create_addmodifydelete_buttons # type: ignore
from utils import create_table_window #type:ignore 
from mech_eng.mech_eng_add.mech_eng_add_view import open_add_mech_eng_window   # type: ignore
from mech_eng.mech_eng_modify.mech_eng_modify_view import open_modify_mech_eng_window # type: ignore 
from mech_eng.mech_eng_delete.mech_eng_delete_controller import delete_selected_mech_engs # type: ignore
from mech_eng.mech_eng_model import MechEng, field_metadata, session # type: ignore

def create_mech_eng_window():    
    create_table_window(
        window_title="Mechanical Engineers",
        table=MechEng,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_mech_eng_window,
        modify_command=open_modify_mech_eng_window,
        delete_command=delete_selected_mech_engs
    )
