# design_eng_delete_controller.py
from tkinter import messagebox
from design_eng.design_eng_model import session, DesignEng, field_metadata #type:ignore
from utils import show_custom_error_message, show_custom_confirmation_message, refresh_table #type:ignore

def delete_design_eng(design_eng):
    try:
        session.delete(design_eng)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_design_engs(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one design engineer to delete.")
        return
    
    design_eng_names = [f"{session.query(DesignEng).get(item).first_name} {session.query(DesignEng).get(item).last_name}" for item in selected_items]
    design_eng_names_str = "\n".join(design_eng_names)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete design engineer {design_eng_names[0]}?"):
            design_eng_id = selected_items[0]
            design_eng = session.query(DesignEng).get(design_eng_id)
            error_message = delete_design_eng(design_eng)
            if error_message:
                show_custom_error_message(tree, "Error", f"Error deleting design engineer {design_eng_names[0]}: {error_message}")
            else:
                refresh_table(tree, DesignEng, session, field_metadata)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete design engineers:\n\n{design_eng_names_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete design engineers:\n\n{design_eng_names_str}"):
                for design_eng_id in selected_items:
                    design_eng = session.query(DesignEng).get(design_eng_id)
                    error_message = delete_design_eng(design_eng)
                    if error_message:
                        show_custom_error_message(tree, "Error", f"Error deleting design engineer {design_eng_names[design_eng_names.index(f'{design_eng.first_name} {design_eng.last_name}')]}: {error_message}")
                        break
                refresh_table(tree, DesignEng, session, field_metadata)




