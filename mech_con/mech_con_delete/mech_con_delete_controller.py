# mech_con_delete_controller.py
from tkinter import messagebox
from mech_con.mech_con_model import session, MechCon, field_metadata #type:ignore
from utils import show_custom_error_message, show_custom_confirmation_message, refresh_table #type:ignore

def delete_mech_con(mech_con):
    try:
        session.delete(mech_con)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_mech_cons(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one Mechanical Contractor to delete.")
        return
    
    mech_con_names = [f"{session.query(MechCon).get(item).mechanical_contractor}" for item in selected_items]
    mech_con_names_str = "\n".join(mech_con_names)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete Mechanical Contractor {mech_con_names[0]}?"):
            mech_con_id = selected_items[0]
            mech_con = session.query(MechCon).get(mech_con_id)
            error_message = delete_mech_con(mech_con)
            if error_message:
                show_custom_error_message(tree, "Error", f"Error deleting Mechanical Contractor {mech_con_names[0]}: {error_message}")
            else:
                refresh_table(tree, MechCon, session, field_metadata)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete Mechanical Contractors:\n\n{mech_con_names_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete Mechanical Contractors:\n\n{mech_con_names_str}"):
                for mech_con_id in selected_items:
                    mech_con = session.query(MechCon).get(mech_con_id)
                    error_message = delete_mech_con(mech_con)
                    if error_message:
                        show_custom_error_message(tree, "Error", f"Error deleting Mechanical Contractor {mech_con_names[mech_con_names.index(f'{mech_con.mechanical_contractor}')]}: {error_message}")
                        break
                refresh_table(tree, MechCon, session, field_metadata)




