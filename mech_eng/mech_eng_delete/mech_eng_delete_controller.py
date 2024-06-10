# mech_eng_delete_controller.py
from tkinter import messagebox
from mech_eng.mech_eng_model import session, MechEng, field_metadata #type:ignore
from utils import show_custom_error_message, show_custom_confirmation_message, refresh_table #type:ignore

def delete_mech_eng(mech_eng):
    try:
        session.delete(mech_eng)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_mech_engs(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one Sales engineer to delete.")
        return
    
    mech_eng_names = [f"{session.query(MechEng).get(item).first_name} {session.query(MechEng).get(item).last_name}" for item in selected_items]
    mech_eng_names_str = "\n".join(mech_eng_names)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete Sales engineer {mech_eng_names[0]}?"):
            mech_eng_id = selected_items[0]
            mech_eng = session.query(MechEng).get(mech_eng_id)
            error_message = delete_mech_eng(mech_eng)
            if error_message:
                show_custom_error_message(tree, "Error", f"Error deleting Sales engineer {mech_eng_names[0]}: {error_message}")
            else:
                refresh_table(tree, MechEng, session, field_metadata)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete Sales engineers:\n\n{mech_eng_names_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete Sales engineers:\n\n{mech_eng_names_str}"):
                for mech_eng_id in selected_items:
                    mech_eng = session.query(MechEng).get(mech_eng_id)
                    error_message = delete_mech_eng(mech_eng)
                    if error_message:
                        show_custom_error_message(tree, "Error", f"Error deleting Sales engineer {mech_eng_names[mech_eng_names.index(f'{mech_eng.first_name} {mech_eng.last_name}')]}: {error_message}")
                        break
                refresh_table(tree, MechEng, session, field_metadata)




