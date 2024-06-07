# project_modify_view.py
import tkinter as tk
from tkinter import ttk
from utils import center_window
from project.project_model import field_metadata
from project.project_modify.project_modify_controller import modify_project_properly_selected, modify_project_wrapper

def open_modify_project_window(tree):
    if modify_project_properly_selected(tree) == None:
        return
    else:
        project = modify_project_properly_selected(tree)

    modify_window = tk.Toplevel()
    modify_window.title("Modify Project")

    fields = field_metadata.keys()
    field_to_frame = {field: field_metadata[field]["frame"] for field in fields}
    entries = {}

    # Create frames
    frames = {i: ttk.Frame(modify_window, padding="10 10 10 10") for i in range(1, 5)}
    for i, frame in frames.items():
        frame.grid(row=0, column=i-1, padx=10, pady=10, sticky="n")

    # Configure grid weights to ensure top alignment
    modify_window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        modify_window.grid_columnconfigure(i, weight=1)

    # Place fields in the specified frame
    row_counters = {i: 0 for i in range(1, 5)}
    for field in fields:
        frame_index = field_to_frame[field]
        frame = frames[frame_index]
        label = ttk.Label(frame, text=field.replace("_", " ").title())
        label.grid(row=row_counters[frame_index], column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        entry.insert(0, getattr(project, field))  # Pre-fill with current project value
        entry.grid(row=row_counters[frame_index], column=1, padx=10, pady=5)
        entries[field] = entry
        row_counters[frame_index] += 1

    update_button = ttk.Button(modify_window, text="Update Project", command=lambda: modify_project_wrapper(entries, project, modify_window, tree))#, update_command))
    update_button.grid(row=1, column=0, columnspan=4, pady=10)

    center_window(modify_window)
    modify_window.focus_force()
