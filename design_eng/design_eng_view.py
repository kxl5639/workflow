import tkinter as tk
from tkinter import ttk
from utils import create_table_window #type:ignore 
from design_eng.design_eng_add.design_eng_add_view import open_add_design_eng_window   # type: ignore
from design_eng.design_eng_modify.design_eng_modify_view import open_modify_design_eng_window # type: ignore 
from design_eng.design_eng_delete.design_eng_delete_controller import delete_selected_design_engs # type: ignore
from design_eng.design_eng_model import DesignEng, field_metadata, session # type: ignore

def create_design_eng_window():    
    create_table_window(
        window_title="Design Engineers",
        table=DesignEng,
        field_metadata=field_metadata,
        session=session,
        add_command=open_add_design_eng_window,
        modify_command=open_modify_design_eng_window,
        delete_command=delete_selected_design_engs
    )
