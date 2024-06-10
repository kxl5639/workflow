from tkinter import messagebox
from design_eng.design_eng_model import session, DesignEng
from design_eng.design_eng_utils import refresh_design_eng_table
from utils import show_custom_error_message, only_one_record_selected

def modify_design_eng_properly_selected(tree):
    selected_item = tree.selection()
    if not selected_item:    
        show_custom_error_message(tree, "Error", "Please select a design engineer to modify.")
        return
    if only_one_record_selected(tree) is True:
        design_eng_id = selected_item[0]  # The item identifier (iid) is the design_eng ID
        design_eng = session.query(DesignEng).get(design_eng_id)
        return design_eng
    else:
        show_custom_error_message(tree, "Error", "Only one design engineer can be selected to modify.")
        return     

def modify_design_eng_wrapper(entries, design_eng, modify_window, tree):
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
        setattr(design_eng, field, value)

    session.commit()
    refresh_design_eng_table(tree)
    
    modify_window.destroy()