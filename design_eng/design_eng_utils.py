from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from design_eng.design_eng_model import session, DesignEng, field_metadata

def design_eng_columns_to_display():
    # Extract columns with display value set to 1
    return [field for field, meta in field_metadata.items() if meta['display'] == 1]    

def populate_treeview_with_design_engs(tree):
    # Define the columns
    columns = design_eng_columns_to_display()

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch design engineers
    design_eng = fetch_design_eng()
    
    # Insert design engineers into the treeview
    for design_eng in design_eng:
        values = tuple(getattr(design_eng, col) for col in columns)
        tree.insert('', 'end', values=values, iid=design_eng.id)  # Use design_eng.id as the item identifier (iid)

def fetch_design_eng():
    return session.query(DesignEng).all()