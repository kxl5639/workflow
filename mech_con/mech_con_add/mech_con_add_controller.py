# mech_con_add_controller.py
from tkinter import messagebox, Toplevel, ttk
from datetime import datetime
from mech_con.mech_con_model import session, MechCon #type:ignore
from mech_con.mech_con_controller import columns_to_display #type:ignore
from utils import show_custom_error_message, refresh_table #type:ignore

def add_mech_con(formatted_entries):
    try:
        new_mech_con = MechCon(**formatted_entries)
        session.add(new_mech_con)
        session.commit()
        return None  # No error message
    except Exception as e:
        return str(e)  # Return the error message

def add_mech_con_wrapper(entries, tree, add_window):
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        if not entry.get().strip():
            empty_fields.append(field.replace("_", " ").title())
            if first_empty_entry is None:
                first_empty_entry = entry

    if empty_fields:
        show_custom_error_message(add_window, "Error", f"The following fields cannot be empty:\n" + "\n" + "\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()
        return

    formatted_entries = {field: entry.get() for field, entry in entries.items()}
    
    error_message = add_mech_con(formatted_entries)
    if error_message:
        messagebox.showerror("Error", error_message)
    else:
        refresh_table(tree, MechCon, session, columns_to_display)
        add_window.destroy()