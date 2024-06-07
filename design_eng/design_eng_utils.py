from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from design_eng.design_eng_model import session, DesignEng, field_metadata
from utils import center_window

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

def refresh_design_eng_table(tree):
    for item in tree.get_children():
        tree.delete(item)
    populate_treeview_with_design_engs(tree)

def create_design_eng_window(window, prefilled_data, button_text, submit_callback):
    fields = field_metadata.keys()    

    entries = {}

    # Create a single frame for the entries
    frame = ttk.Frame(window, padding="10 10 10 10")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    row_counter = 0
    first_entry = None
    for field in fields:
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counter, column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        
        entry.insert(0, prefilled_data.get(field, ""))
            
        entry.grid(row=row_counter, column=1, padx=10, pady=5)
        entries[field] = entry
        if first_entry is None:
            first_entry = entry
        row_counter += 1

    button_frame = ttk.Frame(window)
    button_frame.grid(row=1, column=0, pady=10)

    submit_button = ttk.Button(button_frame, text=button_text, command=lambda: submit_callback(entries))
    submit_button.grid(row=0, column=0, padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
    cancel_button.grid(row=0, column=1, padx=10)

    center_window(window)

    if first_entry is not None:
        first_entry.focus_set()

    return entries