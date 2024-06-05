import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window
from project.project_controller import add_project
from project.project_utils import populate_treeview_with_projects
from project.project_model import field_metadata
from app import testing  # Import the testing variable

def refresh_project_table(tree):
    for item in tree.get_children():
        tree.delete(item)

    populate_treeview_with_projects(tree)

def open_add_project_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Project")

    # Fetch fields and metadata from Project model
    fields = field_metadata.keys()
    default_values = {field: field_metadata[field]["default"] for field in fields}
    field_to_frame = {field: field_metadata[field]["frame"] for field in fields}

    entries = {}

    # Create frames
    frames = {i: ttk.Frame(add_window, padding="10 10 10 10") for i in range(1, 5)}
    for i, frame in frames.items():
        frame.grid(row=0, column=i-1, padx=10, pady=10, sticky="n")

    # Configure grid weights to ensure top alignment
    add_window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        add_window.grid_columnconfigure(i, weight=1)

    # Place fields in the specified frame
    row_counters = {i: 0 for i in range(1, 5)}
    first_entry = None  # Variable to store the first entry widget
    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)      
        if testing:  # Pre-fill values depending on testing mode or not
            if field == "submittal_date":
                entry.insert(0, "XX/XX/XX")
            else:
                entry.insert(0, "TESTING")
        else:  # Pre-fill values with specific default value in production mode
            entry.insert(0, default_values[field])   
        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5)
        entries[field] = entry
        if first_entry is None:
            first_entry = entry  # Store the first entry widget
        row_counters[frame_index] += 1

    def add_project_wrapper():
        # Convert entries keys to the expected format with underscores
        formatted_entries = {field.replace(" ", "_").lower(): entry for field, entry in entries.items()}
        
        error_message = add_project(formatted_entries)
        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            refresh_project_table(tree)
            add_window.destroy()

    add_button = ttk.Button(add_window, text="Add Project", command=add_project_wrapper)
    add_button.grid(row=1, column=0, columnspan=4, pady=10)

    center_window(add_window)

    if first_entry is not None:
        first_entry.focus_set()  # Set focus to the first entry widget
