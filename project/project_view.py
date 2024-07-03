import tkinter as tk
from tkinter import ttk
from project.project_controller import column_map, fetch_names, fetch_record_data, get_entry_data, set_entry_state, set_entry_text
from project.project_model import delete_selected_projects
from utils import create_tree_button_frame, create_button_frame
from configs import testing
from model import ProjectManager, DesignEngineer, SalesEngineer, Project, Client, MechanicalContractor, MechanicalEngineer, session
from view import BaseWindow

#region create project window
def create_project_window():    
    project_window = tk.Toplevel(name='project_window')
    project_window.title("Projects")
    project_window.grid_rowconfigure(0, weight=1)
    project_window.grid_columnconfigure(0, weight=1)
    
    from project.project_controller import update_table_data    
    table_data = update_table_data()
    tree_but_frame = create_tree_button_frame(project_window,                                                    
                                                    column_map,
                                                    table_data,                                                                                                        
                                                    add_command=lambda: open_add_project_window(project_window),                                                    
                                                    modify_command=lambda: open_modify_project_window(project_window),                                                                                                                                                   
                                                    delete_command=lambda: open_delete_project_window(project_window))
    
    tree_but_frame.grid(row=0, padx=20, pady=20, sticky="nsew")

    # Center the window after adding widgets
    BaseWindow.center_window(project_window)    
    project_window.focus_force()
    
    return project_window
#endregion

#region Call project add/modify/delete window
def open_add_project_window(project_window):   
    
    create_add_modify_window(project_window,'Add New Projects','Add',selected_record=None)

def open_modify_project_window(project_window):    
    
    from project.project_controller import modify_record_properly_selected
    table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree
    selected_record = modify_record_properly_selected(table_window_tree,session,Project)
    if selected_record is not None:    
        create_add_modify_window(project_window, 'Modify Projects', 'Modify', selected_record=selected_record)

def open_delete_project_window(project_window):
    
    from project.project_controller import delete_records_properly_selected
    table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree
    selected_records, good_selection = delete_records_properly_selected(table_window_tree,session,Project)    
    if good_selection is not False:
        delete_selected_projects(project_window, selected_records)
#endregion

#region create project add/modify window
def create_label_entry(parent, label_text, row, column, default_text='', testing=False):
    ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
    if testing == 1:
        set_entry_text(entry, 'Testing')
    else:
        set_entry_text(entry, default_text)
    return entry

def create_frame(parent, text, row, column):
    frame = ttk.Labelframe(parent, text=text)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
    frame.grid_columnconfigure(1, weight=1)
    return frame

def create_combobox(parent, label_text, values, row, column):
    ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
    combobox = ttk.Combobox(parent, values=values, state="readonly")
    combobox.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
    return combobox

def create_add_or_modify_frame(master, is_modify=False, selected_record_id=None):

    add_mod_frame = ttk.Frame(master)
    add_mod_frame.grid_rowconfigure(0, weight=1)
    add_mod_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Fetch names for comboboxes
    pm_names = fetch_names(ProjectManager)
    de_names = fetch_names(DesignEngineer)
    se_names = fetch_names(SalesEngineer)


    #region Creates labels and entry/combo widgets and fills in the data
    proj_info_frame = create_frame(add_mod_frame, "Project Info", 0, 0)
    proj_info_entries = {
        "project_number": create_label_entry(proj_info_frame, "Project Number", 0, 0, '', testing=testing),
        "em_type": create_label_entry(proj_info_frame, "EM Type", 1, 0, 'B', testing=testing),
        "job_phase": create_label_entry(proj_info_frame, "Job Phase", 2, 0, '1', testing=testing),
        "submit_date": create_label_entry(proj_info_frame, "Submit Date", 3, 0, 'XX/XX/XX', testing=testing),
    }
    proj_info_entries.update({
        "pm_name": create_combobox(proj_info_frame, "Project Manager", pm_names, 4, 0),
        "de_name": create_combobox(proj_info_frame, "Design Engineer", de_names, 5, 0),
        "se_name": create_combobox(proj_info_frame, "Sales Engineer", se_names, 6, 0),
    })    
    client_frame = create_frame(add_mod_frame, "Client", 0, 1)
    client_entries = {
        "client_name": create_label_entry(client_frame, "Client", 0, 0, '', testing=testing),
        "scope": create_label_entry(client_frame, "Scope", 1, 0, '', testing=testing),
        "address": create_label_entry(client_frame, "Address", 2, 0, '', testing=testing),
        "city": create_label_entry(client_frame, "City", 3, 0, '', testing=testing),
        "state": create_label_entry(client_frame, "State", 4, 0, '', testing=testing),
        "zip_code": create_label_entry(client_frame, "Zip Code", 5, 0, '', testing=testing)
    }

    me_frame = create_frame(add_mod_frame, "Mechanical Engineer", 0, 2)
    me_entries = {
        "name": create_label_entry(me_frame, "Name", 0, 0, '', testing=testing),
        "address": create_label_entry(me_frame, "Address", 1, 0, '', testing=testing),
        "city": create_label_entry(me_frame, "City", 2, 0, '', testing=testing),
        "state": create_label_entry(me_frame, "State", 3, 0, '', testing=testing),
        "zip_code": create_label_entry(me_frame, "Zip Code", 4, 0, '', testing=testing)
    }

    mc_frame = create_frame(add_mod_frame, "Mechanical Contractor", 0, 3)
    mc_entries = {
        "name": create_label_entry(mc_frame, "Name", 0, 0, '', testing=testing),
        "address": create_label_entry(mc_frame, "Address", 1, 0, '', testing=testing),
        "city": create_label_entry(mc_frame, "City", 2, 0, '', testing=testing),
        "state": create_label_entry(mc_frame, "State", 3, 0, '', testing=testing),
        "zip_code": create_label_entry(mc_frame, "Zip Code", 4, 0, '', testing=testing),
        "telephone": create_label_entry(mc_frame, "Telephone", 5, 0, '', testing=testing)
    }

    if is_modify and selected_record_id:        
        project, client, pm, me, mc, de, se = fetch_record_data(selected_record_id)
        set_entry_text(proj_info_entries["project_number"], project.project_number)
        set_entry_state(proj_info_entries["project_number"], 'readonly')        
        set_entry_text(proj_info_entries["em_type"], project.em_type)
        set_entry_text(proj_info_entries["job_phase"], str(project.job_phase))
        set_entry_text(proj_info_entries["submit_date"], project.submit_date)

        set_entry_text(client_entries["client_name"], client.client_name)
        set_entry_text(client_entries["scope"], client.scope)
        set_entry_text(client_entries["address"], client.address)
        set_entry_text(client_entries["city"], client.city)
        set_entry_text(client_entries["state"], client.state)
        set_entry_text(client_entries["zip_code"], str(client.zip_code))

        set_entry_text(me_entries["name"], me.name)
        set_entry_text(me_entries["address"], me.address)
        set_entry_text(me_entries["city"], me.city)
        set_entry_text(me_entries["state"], me.state)
        set_entry_text(me_entries["zip_code"], str(me.zip_code))

        set_entry_text(mc_entries["name"], mc.name)
        set_entry_text(mc_entries["address"], mc.address)
        set_entry_text(mc_entries["city"], mc.city)
        set_entry_text(mc_entries["state"], mc.state)
        set_entry_text(mc_entries["zip_code"], str(mc.zip_code))
        set_entry_text(mc_entries["telephone"], mc.telephone)

        proj_info_entries["pm_name"].set(f"{pm.first_name} {pm.last_name}")
        proj_info_entries["de_name"].set(f"{de.first_name} {de.last_name}")
        proj_info_entries["se_name"].set(f"{se.first_name} {se.last_name}")
    #endregion

    # Creates a dictionary of the dictionary of entries. For example proj_info_entries is a dictionary of the label and the entry object.
    entry_dict = {Project.__tablename__:proj_info_entries, 
                  Client.__tablename__:client_entries,
                  MechanicalEngineer.__tablename__:me_entries,
                  MechanicalContractor.__tablename__:mc_entries}
    
    return add_mod_frame, entry_dict

def create_add_modify_window(master, title='Add New _________', button_text='Add or Modify?', selected_record=None):
    from project.project_model import add_mod_project
    from utils import highlight_tree_item 

# Tree grabbed from project window 
    table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree    

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
            highlight_tree_item(master, table_window_tree, project_id)  # Highlight the newly added or modified item

    button_frame = create_button_frame(add_mod_window, [(button_text, lambda: on_add_modify()),
                                                                ('Cancel', add_mod_window.destroy)])
    button_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

    BaseWindow.center_window(add_mod_window)
    add_mod_window.grab_set()
    add_mod_window.focus_force()
    master.wait_window(add_mod_window)
#endregion

