from utils import delete_record_properly_selected, delete_record, refresh_table, show_custom_error_message
from proj_manager.proj_manager_model import ProjManager, session
from proj_manager.proj_manager_controller import columns_to_display

def delete_selected_proj_managers(proj_manager_window):
    table_window_tree = proj_manager_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    
    # Checks if at least 1 record was selected.
    record_ids, ready_to_delete = delete_record_properly_selected(table_window_tree,session,ProjManager,'first_name','last_name')
    if not ready_to_delete is True:              
        return
    else:
        for record_id in record_ids:
            record = session.query(ProjManager).get(record_id)
            error_message = delete_record(record, session)
            if error_message:
                show_custom_error_message(table_window_tree, "Error", f"Error deleting record.{error_message}")
            else:
                refresh_table(table_window_tree, ProjManager, session, columns_to_display)