import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy.orm import Session
from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
from utils import center_window
from project.project_utils import create_add_or_modify_frame
# Function to add project

def add_project():
  
    # project_number_entry = 
    # em_type_entry = 
    # job_phase_entry = 
    # submit_date_entry = 
    # projectmanager_entry = 
    # designengineer_entry = 
    # salesengineer_entry = 
    # client_entry = 
    # client_scope = 
    # client_address = 
    # client_city = 
    # client_state = 
    # client_zip_code = 
    # mecheng_name = 
    # mecheng_address = 
    # mecheng_city = 
    # mecheng_state = 
    # mecheng_zip_code = 
    # mechcon_name = 
    # mechcon_address = 
    # mechcon_city = 
    # mechcon_state = 
    # mechcon_zip_code = 
    # mechcon_phone = 



    pass

def extract_entry_widgets(parent, entry_widgets=None):
    if entry_widgets is None:
        entry_widgets = []
    
    for widget in parent.winfo_children():
        if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Entry):
            entry_widgets.append(widget)
        elif isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
            extract_entry_widgets(widget, entry_widgets)
    
    return entry_widgets



#region Create labels and entry boxes
# Create the main window
add_mod_window = tk.Tk()
add_mod_window.title("Add Project")
add_mod_window.grid_rowconfigure(0, weight=1)
add_mod_window.grid_columnconfigure(0, weight=1)
add_mod_window.resizable(height=False,width=True)

frame = create_add_or_modify_frame(add_mod_window)


# # Create submit button
# submit_button = tk.Button(add_mod_window, text="Add Project", command=add_project)
# submit_button.grid(row=10, columnspan=2)

center_window(add_mod_window)
# Start the main loop
add_mod_window.mainloop()






def add_mod_project(master, project_window, entry_dict, is_modify, selected_record=None):    
    from sqlalchemy.exc import IntegrityError
    from utils import refresh_tree, table_data, column_map

    project_id = None

    # Data Validation
    if is_valid_data(master, entry_dict, is_modify):    
        # Unpack entry_dict
        proj_info_entries = entry_dict[Project.__tablename__]
        client_entries = entry_dict[Client.__tablename__]
        me_entries = entry_dict[MechanicalEngineer.__tablename__]
        mc_entries = entry_dict[MechanicalContractor.__tablename__]     
        table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree

        try:
            new_client = Client(**get_entry_data(client_entries))
            session.add(new_client)
            session.commit()

            pm_first_name, pm_last_name = proj_info_entries["pm_name"].get().split()
            projectmanager_id = session.query(ProjectManager).filter_by(first_name=pm_first_name, last_name=pm_last_name).first().id

            de_first_name, de_last_name = proj_info_entries["de_name"].get().split()
            designengineer_id = session.query(DesignEngineer).filter_by(first_name=de_first_name, last_name=de_last_name).first().id

            se_first_name, se_last_name = proj_info_entries["se_name"].get().split()
            salesengineer_id = session.query(SalesEngineer).filter_by(first_name=se_first_name, last_name=se_last_name).first().id

            new_me = MechanicalEngineer(**get_entry_data(me_entries))
            session.add(new_me)
            session.commit()

            new_mc = MechanicalContractor(**get_entry_data(mc_entries))
            session.add(new_mc)
            session.commit()

            project_data = {
                "project_number": proj_info_entries["project_number"].get(),
                "em_type": proj_info_entries["em_type"].get(),
                "job_phase": proj_info_entries["job_phase"].get(),
                "submit_date": proj_info_entries["submit_date"].get(),
                "client_id": new_client.id,
                "projectmanager_id": projectmanager_id,
                "mechanicalengineer_id": new_me.id,
                "mechanicalcontractor_id": new_mc.id,
                "designengineer_id": designengineer_id,
                "salesengineer_id": salesengineer_id
            }

            need_refresh = False
            if is_modify:
                existing_project = session.query(Project).filter_by(id=selected_record.id).first()
                for key, value in project_data.items():
                    setattr(existing_project, key, value)
                session.commit()
                project_id = existing_project.id  # Get the ID of the modified project
                messagebox.showinfo("Success", "Project and related entities modified successfully!")
                need_refresh = True                
            else:
                existing_project = session.query(Project).filter_by(project_number=project_data["project_number"]).first()
                if existing_project:
                    raise IntegrityError("Project number already exists", None, None)
                new_project = Project(**project_data)
                session.add(new_project)
                session.commit()
                project_id = new_project.id  # Get the ID of the new project
                messagebox.showinfo("Success", "Project and related entities added successfully!")
                need_refresh = True

        except IntegrityError as e:
            session.rollback()
            messagebox.showerror("Error", "Project number already exists. Please use a unique project number.")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))

    if need_refresh:
        master.destroy()
        project_window.lift()
        project_window.focus_set()
        update_table_data()  # Refresh the data
        refresh_tree(table_window_tree, table_data, column_map)
        return project_id  # Return the project ID

    return None  # Return None if no refresh was needed


def create_add_modify_window(master, title='Add New _________', button_text='Add or Modify?', selected_record=None):
    from project.project_model import add_mod_project
    from utils import highlight_tree_item

    is_modify = button_text.lower() == 'modify'
    add_mod_window = tk.Toplevel()
    add_mod_window.title(title)
    add_mod_window.grid_rowconfigure(0, weight=1)
    add_mod_window.grid_columnconfigure(0, weight=1)
    add_mod_window.resizable(height=False, width=True)

    add_mod_frame, entry_dict = create_add_or_modify_frame(add_mod_window, is_modify, selected_record.id if selected_record else None)
    add_mod_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def on_add_modify():
        project_id = add_mod_project(add_mod_window, master, entry_dict, is_modify, selected_record if selected_record else None)
        if project_id is not None:
            highlight_tree_item(master, project_id)  # Highlight the newly added or modified item

    button_frame = create_button_frame(add_mod_window, [(button_text, on_add_modify),
                                                        ('Cancel', add_mod_window.destroy)])
    button_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

    center_window(add_mod_window)
    add_mod_window.grab_set()
    add_mod_window.focus_force()
    master.wait_window(add_mod_window)









def fetch_record_data(record_id):    
    project = session.query(Project).filter_by(id=record_id).first()
    client = session.query(Client).filter_by(id=project.client_id).first()
    pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
    me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
    mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
    de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
    se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
    return project, client, pm, me, mc, de, se






       # Tree grabbed from project window 
        table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree
        



        
from utils import show_custom_confirmation_message

tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree
selected_record = modify_record_properly_selected(table_window_tree,session,Project)
if selected_record is None:        
    show_custom_error_message(project_window, "Error", "Please select at least one project to delete.")
    return

confirm = show_custom_confirmation_message(project_window, "Confirm Deletion", "Are you sure you want to delete the selected project(s)?")

if confirm:
    try:
        for item in selected_items:
            project_id = tree.item(item, "values")[0]
            project = session.query(Project).filter_by(id=project_id).first()
            if project:
                session.delete(project)
                session.commit()
                tree.delete(item)
        messagebox.showinfo("Success", "Selected project(s) deleted successfully!")
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", str(e))       


def delete_record_properly_selected(tree, session, model, *fields):
    selected_records = tree.selection()
    if not selected_records:
        show_custom_error_message(tree, "Error", "Please select at least one record to delete.")
        return None, False
    
    # Creates a string of list of record(s) that are selected to be deleted    
    records_labels = []
    for item in selected_records:
        instance = session.query(model).get(item)
        if instance:
            record_label = " ".join(str(getattr(instance, attr)) for attr in fields)
            records_labels.append(record_label)
    records_labels_str = "\n".join(records_labels)
    
    if len(selected_records) == 1:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Are you sure you want to delete record:\n\n {records_labels[0]}?\n") is False:
            return None, False
        else:            
            record_id = [selected_records[0]]            
            return record_id, True
    else:
        if show_custom_confirmation_message(tree, "Confirm Deletion", f"Confirm you want to delete delete records:\n\n{records_labels_str}\n") is False:
            return None, False
        else:
            if show_custom_confirmation_message(tree, "Confirm Deletion", f"FINAL warning! This cannot be undone.\n\nPlease confirm you want to delete delete records:\n\n{records_labels_str}\n") is False:
                return None, False
            else:
                record_ids = []
                for record_id in selected_records:    
                    record_ids.append(record_id)                
                return record_ids, True    
            
















def delete_selected_projects(project_window):
    table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree    
    # Checks if at least 1 record was selected.
    record_ids, ready_to_delete = delete_record_properly_selected(table_window_tree,session,Project,'project_number')
    print(record_ids)
    if not ready_to_delete is True:
        return
    else:
        for record_id in record_ids:
            record = session.query(Project).get(record_id)
            error_message = delete_record(record, session)
            if error_message:
                show_custom_error_message(table_window_tree, "Error", f"Error deleting record.{error_message}")
            else:
                refresh_table(table_window_tree, Project, session, columns_to_display)