import tkinter as tk
from tkinter import ttk
from utils import center_window
from project.project_add.project_add_controller import add_project_wrapper
from project.project_model import field_metadata
from app import testing

def open_add_project_window(tree):
    add_window = tk.Toplevel()
    add_window.title("Add Project")

    fields = field_metadata.keys()
    default_values = {field: field_metadata[field]["default"] for field in fields}
    field_to_frame = {field: field_metadata[field]["frame"] for field in fields}

    entries = {}

    frames = {i: ttk.Frame(add_window, padding="10 10 10 10") for i in range(1, 5)}
    for i, frame in frames.items():
        frame.grid(row=0, column=i-1, padx=10, pady=10, sticky="n")

    add_window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        add_window.grid_columnconfigure(i, weight=1)

    row_counters = {i: 0 for i in range(1, 5)}
    first_entry = None
    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        if testing:
            if field == "submittal_date":
                entry.insert(0, "XX/XX/XX")
            else:
                entry.insert(0, "TESTING")
        else:
            entry.insert(0, default_values[field])
        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5)
        entries[field] = entry
        if first_entry is None:
            first_entry = entry
        row_counters[frame_index] += 1

    add_button = ttk.Button(add_window, text="Add Project", command=lambda: add_project_wrapper(entries, tree, add_window))
    add_button.grid(row=1, column=0, columnspan=4, pady=10)

    center_window(add_window)

    if first_entry is not None:
        first_entry.focus_set()
