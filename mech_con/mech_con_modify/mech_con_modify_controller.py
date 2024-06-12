from tkinter import messagebox
from mech_con.mech_con_model import session, MechCon #type:ignore
from mech_con.mech_con_controller import columns_to_display #type:ignore
from utils import show_custom_error_message, only_one_record_selected, refresh_table #type:ignore

def modify_mech_con_properly_selected(tree):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a Mechanical Contractor to modify.")
        return
    if only_one_record_selected(tree) is True:
        mech_con_id = selected_item[0]  # The item identifier (iid) is the mech_con ID
        mech_con = session.query(MechCon).get(mech_con_id)
        return mech_con
    else:
        show_custom_error_message(tree, "Error", "Only one Mechanical Contractor can be selected to modify.")
        return     

def modify_mech_con_wrapper(entries, mech_con, modify_window, tree):
    # Check if any entry is empty
    empty_fields = []
    first_empty_entry = None
    for field, entry in entries.items():
        if not entry.get().strip():
            empty_fields.append(field.replace("_", " ").title())
            if first_empty_entry is None:
                first_empty_entry = entry

    if empty_fields:
        show_custom_error_message(modify_window, "Error", f"The following fields cannot be empty:\n" + "\n" +"\n".join(empty_fields))
        if first_empty_entry:
            first_empty_entry.focus_set()  # Set focus to the first empty entry widget
        return

    # Convert entries keys to the expected format with underscores
    formatted_entries = {field: entry.get() for field, entry in entries.items()}
    
    for field, value in formatted_entries.items():
        setattr(mech_con, field, value)

    session.commit()
    refresh_table(tree, MechCon, session, columns_to_display)
    
    modify_window.destroy()