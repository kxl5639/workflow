# sales_eng_delete_controller.py
from tkinter import messagebox
from sales_eng.sales_eng_model import session, SalesEng #type:ignore
from sales_eng.sales_eng_controller import columns_to_display #type:ignore
from utils import show_custom_error_message, show_custom_confirmation_message, refresh_table #type:ignore

def delete_sales_eng(sales_eng):
    try:
        session.delete(sales_eng)
        session.commit()
    except Exception as e:
        return str(e)  # Return the error message
    return None

def delete_selected_sales_engs(tree):
    selected_items = tree.selection()
    
    if not selected_items:
        show_custom_error_message(tree, "Error", "Please select at least one Sales engineer to delete.")
        return
    
    sales_eng_names = [f"{session.query(SalesEng).get(item).first_name} {session.query(SalesEng).get(item).last_name}" for item in selected_items]
    sales_eng_names_str = "\n".join(sales_eng_names)
    
    if len(selected_items) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete Sales engineer {sales_eng_names[0]}?"):
            sales_eng_id = selected_items[0]
            sales_eng = session.query(SalesEng).get(sales_eng_id)
            error_message = delete_sales_eng(sales_eng)
            if error_message:
                show_custom_error_message(tree, "Error", f"Error deleting Sales engineer {sales_eng_names[0]}: {error_message}")
            else:
                refresh_table(tree, SalesEng, session, columns_to_display)
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete Sales engineers:\n\n{sales_eng_names_str}"):
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete Sales engineers:\n\n{sales_eng_names_str}"):
                for sales_eng_id in selected_items:
                    sales_eng = session.query(SalesEng).get(sales_eng_id)
                    error_message = delete_sales_eng(sales_eng)
                    if error_message:
                        show_custom_error_message(tree, "Error", f"Error deleting Sales engineer {sales_eng_names[sales_eng_names.index(f'{sales_eng.first_name} {sales_eng.last_name}')]}: {error_message}")
                        break
                refresh_table(tree, SalesEng, session, columns_to_display)




