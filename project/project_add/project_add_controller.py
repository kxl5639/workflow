# project_add_controller.py
from tkinter import messagebox, Toplevel, ttk
from project.project_model import session, Project
from project.project_utils import refresh_project_table
from utils import center_window

def add_project(formatted_entries):
    try:
        new_project = Project(**formatted_entries)
        session.add(new_project)
        session.commit()
        return None  # No error message
    except Exception as e:
        return str(e)  # Return the error message

def add_project_wrapper(entries, tree, add_window):
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        if not entry.get().strip():
            empty_fields.append(field.replace("_", " ").title())
            if first_empty_entry is None:
                first_empty_entry = entry

    if empty_fields:
        show_error_message(add_window, empty_fields)
        if first_empty_entry:
            first_empty_entry.focus_set()
        return
    
    formatted_entries = {field: entry.get() for field, entry in entries.items()}
    error_message = add_project(formatted_entries)
    if error_message:
        messagebox.showerror("Error", error_message)
    else:
        refresh_project_table(tree)
        add_window.destroy()

def show_error_message(parent_window, empty_fields):
    error_message_window = Toplevel()
    error_message_window.transient(parent_window)
    error_message_window.title("Error")
    ttk.Label(error_message_window, text=f"The following fields cannot be empty:\n" + "\n" + "\n".join(empty_fields)).pack(padx=10, pady=10)
    ttk.Button(error_message_window, text="OK", command=error_message_window.destroy).pack(pady=5)
    center_window(error_message_window)

    error_message_window.grab_set()  # Make the window modal
    error_message_window.focus_force()  # Focus on the error message window
    parent_window.wait_window(error_message_window)  # Wait until the error message window is closed
