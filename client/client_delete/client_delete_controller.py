from utils import delete_record_properly_selected, delete_record, refresh_table, show_custom_error_message
from client.client_model import Client, session
from client.client_controller import columns_to_display

def delete_selected_clients(client_window):
    table_window_tree = client_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    
    # Checks if at least 1 record was selected.
    record_ids, ready_to_delete = delete_record_properly_selected(table_window_tree,session,Client,'first_name','last_name')
    if not ready_to_delete is True:              
        return
    else:
        for record_id in record_ids:
            record = session.query(Client).get(record_id)
            error_message = delete_record(record, session)
            if error_message:
                show_custom_error_message(table_window_tree, "Error", f"Error deleting record.{error_message}")
            else:
                refresh_table(table_window_tree, Client, session, columns_to_display)