from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from project.project_model import session, Project, field_metadata
from utils import show_custom_error_message, center_window

def project_columns_to_display():
    # Extract columns with display value set to 1
    return [field for field, meta in field_metadata.items() if meta['display'] == 1]

def fetch_projects():
    return session.query(Project).all()

def populate_treeview_with_projects(tree):
    # Define the columns
    columns = project_columns_to_display()

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch projects
    projects = fetch_projects()
    
    # Insert projects into the treeview
    for project in projects:
        values = tuple(getattr(project, col) for col in columns)
        tree.insert('', 'end', values=values, iid=project.id)  # Use project.id as the item identifier (iid)

def refresh_project_table(tree):
    for item in tree.get_children():
        tree.delete(item)
    populate_treeview_with_projects(tree)

def validate_date_format(date_str, parent_window):
    if date_str != "XX/XX/XX":
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
            return date_obj.strftime('%m/%d/%y'), None  # Return formatted date and no error
        except ValueError:
            show_custom_error_message(parent_window, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
            return None, "Invalid Date Format"
    return date_str, None  # Return the original placeholder and no error


def create_project_window(window, prefilled_data, button_text, submit_callback):
    fields = field_metadata.keys()
    field_to_frame = {field: field_metadata[field]["frame"] for field in fields}

    entries = {}

    frames = {i: ttk.Frame(window, padding="10 10 10 10") for i in range(1, 5)}
    for i, frame in frames.items():
        frame.grid(row=0, column=(i-1)*2, padx=10, pady=10, sticky="n")

    # Add vertical separators between frames
    for i in range(1, 4):
        separator = ttk.Separator(window, orient='vertical')
        separator.grid(row=0, column=(i*2)-1, padx=(0, 10), pady=10, sticky='ns')

    window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        window.grid_columnconfigure(i*2, weight=1)

    row_counters = {i: 0 for i in range(1, 5)}
    first_entry = None
    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        
        entry.insert(0, prefilled_data.get(field, ""))
            
        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5)
        entries[field] = entry
        if first_entry is None:
            first_entry = entry
        row_counters[frame_index] += 1

    button_frame = ttk.Frame(window)
    button_frame.grid(row=1, column=0, columnspan=7, pady=10)

    submit_button = ttk.Button(button_frame, text=button_text, command=lambda: submit_callback(entries))
    submit_button.grid(row=0, column=0, padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
    cancel_button.grid(row=0, column=1, padx=10)


    center_window(window)

    if first_entry is not None:
        first_entry.focus_set()

    return entries