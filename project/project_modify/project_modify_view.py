# project_modify_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window
from project.project_model import field_metadata

def open_modify_project_window(project, update_command):
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

    def update_project_wrapper():
        # Check if any entry is empty
        empty_fields = []
        first_empty_entry = None
        for field, entry in entries.items():
            if not entry.get().strip():
                empty_fields.append(field.replace("_", " ").title())
                if first_empty_entry is None:
                    first_empty_entry = entry

        if empty_fields:
            messagebox.showerror("Error", f"The following fields cannot be empty:\n" + "\n".join(empty_fields))
            if first_empty_entry:
                first_empty_entry.focus_set()  # Set focus to the first empty entry widget
            return

        # Convert entries keys to the expected format with underscores
        formatted_entries = {field: entry.get() for field, entry in entries.items()}

        update_command(project, formatted_entries)
        modify_window.destroy()

    update_button = ttk.Button(modify_window, text="Update Project", command=update_project_wrapper)
    update_button.grid(row=1, column=0, columnspan=4, pady=10)

    center_window(modify_window)
    modify_window.focus_force()
