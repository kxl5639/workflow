import tkinter as tk
from tkinter import ttk
from configs import testing
from utils import center_window, create_dynamic_button_frame

def set_entry_text(entry_widget, testing, testing_text, production_text):
    entry_widget.insert(0, testing_text if testing == 1 else production_text)


def create_add_or_modify_frame(master):

    #region Create Frames, Labels, and Entry Widgets
    add_mod_frame = ttk.Frame(master)
    # add_mod_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')   
    add_mod_frame.grid_rowconfigure(0, weight=1)
    add_mod_frame.grid_columnconfigure(0, weight=1)
    add_mod_frame.grid_columnconfigure(1, weight=1)
    add_mod_frame.grid_columnconfigure(2, weight=1)
    add_mod_frame.grid_columnconfigure(3, weight=1)

    # Create labels and entry boxes
    proj_info_frame = ttk.Labelframe(add_mod_frame, text = "Project Info")
    proj_info_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
    proj_info_frame.grid_columnconfigure((1), weight=1)

    ttk.Label(proj_info_frame, text="Project Number").grid(row=0, column=0, padx=10, pady=10,sticky="w")
    project_number_entry = ttk.Entry(proj_info_frame)
    project_number_entry.grid(row=0, column=1,padx=(0,10),pady=10,sticky='ew')
    set_entry_text(project_number_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="EM Type").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
    em_type_entry = ttk.Entry(proj_info_frame)
    em_type_entry.grid(row=1, column=1,padx=(0,10), pady=(0,10), sticky='ew')
    set_entry_text(em_type_entry, testing, 'Testing', 'B')

    ttk.Label(proj_info_frame, text="Job Phase").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
    job_phase_entry = ttk.Entry(proj_info_frame)
    job_phase_entry.grid(row=2, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(job_phase_entry, testing, 'Testing', '1')

    ttk.Label(proj_info_frame, text="Submit Date").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
    submit_date_entry = ttk.Entry(proj_info_frame)
    submit_date_entry.grid(row=3, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(submit_date_entry, testing, 'Testing', 'XX/XX/XX')

    ttk.Label(proj_info_frame, text="PM First Name").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
    pm_first_name_entry = ttk.Entry(proj_info_frame)
    pm_first_name_entry.grid(row=4, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(pm_first_name_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="PM Last Name").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
    pm_last_name_entry = ttk.Entry(proj_info_frame)
    pm_last_name_entry.grid(row=5, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(pm_last_name_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="DE First Name").grid(row=6, column=0, padx=10, pady=(0,10),sticky="w")
    de_first_name_entry = ttk.Entry(proj_info_frame)
    de_first_name_entry.grid(row=6, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(de_first_name_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="DE Last Name").grid(row=7, column=0, padx=10, pady=(0,10),sticky="w")
    de_last_name_entry = ttk.Entry(proj_info_frame)
    de_last_name_entry.grid(row=7, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(de_last_name_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="SE First Name").grid(row=8, column=0, padx=10, pady=(0,10),sticky="w")
    se_first_name_entry = ttk.Entry(proj_info_frame)
    se_first_name_entry.grid(row=8, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(se_first_name_entry, testing, 'Testing', '')

    ttk.Label(proj_info_frame, text="SE Last Name").grid(row=9, column=0, padx=10, pady=(0,10),sticky="w")
    se_last_name_entry = ttk.Entry(proj_info_frame)
    se_last_name_entry.grid(row=9, column=1,padx=(0,10), pady=(0,10),sticky='ew')
    set_entry_text(se_last_name_entry, testing, 'Testing', '')

    client_frame = ttk.Labelframe(add_mod_frame, text = "Client")
    client_frame.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')
    client_frame.grid_columnconfigure((1), weight=1)
    
    ttk.Label(client_frame, text="Client").grid(row=0, column=0, padx=10, pady=10,sticky="w")
    client_entry = ttk.Entry(client_frame)
    client_entry.grid(row=0, column=1,padx=(0,10),sticky='ew')
    set_entry_text(client_entry, testing, 'Testing', '')
    
    ttk.Label(client_frame, text="Scope").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
    client_scope = ttk.Entry(client_frame)
    client_scope.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(client_scope, testing, 'Testing', '')

    ttk.Label(client_frame, text="Address").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
    client_address = ttk.Entry(client_frame)
    client_address.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(client_address, testing, 'Testing', '')

    ttk.Label(client_frame, text="City").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
    client_city = ttk.Entry(client_frame)
    client_city.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(client_city, testing, 'Testing', '')

    ttk.Label(client_frame, text="State").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
    client_state = ttk.Entry(client_frame)
    client_state.grid(row=4, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(client_state, testing, 'Testing', '')

    ttk.Label(client_frame, text="Zip Code").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
    client_zip_code = ttk.Entry(client_frame)
    client_zip_code.grid(row=5, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(client_zip_code, testing, 'Testing', '')

    mecheng_frame = ttk.Labelframe(add_mod_frame, text = "Mechanical Engineer")
    mecheng_frame.grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
    mecheng_frame.grid_columnconfigure((1), weight=1)

    ttk.Label(mecheng_frame, text="Name").grid(row=0, column=0, padx=10, pady=10,sticky="w")
    mecheng_name = ttk.Entry(mecheng_frame)
    mecheng_name.grid(row=0, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mecheng_name, testing, 'Testing', '')

    ttk.Label(mecheng_frame, text="Address").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
    mecheng_address = ttk.Entry(mecheng_frame)
    mecheng_address.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mecheng_address, testing, 'Testing', '')

    ttk.Label(mecheng_frame, text="City").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
    mecheng_city = ttk.Entry(mecheng_frame)
    mecheng_city.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mecheng_city, testing, 'Testing', '')

    ttk.Label(mecheng_frame, text="State").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
    mecheng_state = ttk.Entry(mecheng_frame)
    mecheng_state.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mecheng_state, testing, 'Testing', '')

    ttk.Label(mecheng_frame, text="Zip Code").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
    mecheng_zip_code = ttk.Entry(mecheng_frame)
    mecheng_zip_code.grid(row=4, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mecheng_zip_code, testing, 'Testing', '')

    mechcon_frame = ttk.Labelframe(add_mod_frame, text = "Mechanical Contractor")
    mechcon_frame.grid(row=0,column=3,padx=10,pady=10,sticky='nsew')
    mechcon_frame.grid_columnconfigure((1), weight=1)

    ttk.Label(mechcon_frame, text="Name").grid(row=0, column=0, padx=10, pady=10,sticky="w")
    mechcon_name = ttk.Entry(mechcon_frame)
    mechcon_name.grid(row=0, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_name, testing, 'Testing', '')

    ttk.Label(mechcon_frame, text="Address").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
    mechcon_address = ttk.Entry(mechcon_frame)
    mechcon_address.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_address, testing, 'Testing', '')

    ttk.Label(mechcon_frame, text="City").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
    mechcon_city = ttk.Entry(mechcon_frame)
    mechcon_city.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_city, testing, 'Testing', '')

    ttk.Label(mechcon_frame, text="State").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
    mechcon_state = ttk.Entry(mechcon_frame)
    mechcon_state.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_state, testing, 'Testing', '')

    ttk.Label(mechcon_frame, text="Zip Code").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
    mechcon_zip_code = ttk.Entry(mechcon_frame)
    mechcon_zip_code.grid(row=5, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_zip_code, testing, 'Testing', '')

    ttk.Label(mechcon_frame, text="Telephone").grid(row=6, column=0, padx=10, pady=(0,10),sticky="w")
    mechcon_phone = ttk.Entry(mechcon_frame)
    mechcon_phone.grid(row=6, column=1,padx=(0,10),pady=(0,10),sticky='ew')
    set_entry_text(mechcon_phone, testing, 'Testing', '')
    #endregion
    #region Get Entry data
    # Add Client
    client_data = {
        "client_name": client_entry.get(),
        "scope": client_scope.get(),
        "address": client_address.get(),
        "city": client_city.get(),
        "state": client_state.get(),
        "zip_code": client_zip_code.get()
    }
    # Add Project Manager
    pm_data = {
        "first_name": pm_first_name_entry.get(),
        "last_name": pm_last_name_entry.get()
    }
    # Add Mechanical Engineer
    me_data = {
        "name": mecheng_name.get(),
        "address": mecheng_address.get(),
        "city": mecheng_city.get(),
        "state": mecheng_state.get(),
        "zip_code": mecheng_zip_code.get()
    }
    # Add Mechanical Contractor
    mc_data = {
        "name": mechcon_name.get(),
        "address": mechcon_address.get(),
        "city": mechcon_city.get(),
        "state": mechcon_state.get(),
        "zip_code": mechcon_zip_code.get(),
        "telephone": mechcon_phone.get()
    }
    # Add Design Engineer
    de_data = {
        "first_name": de_first_name_entry.get(),
        "last_name": de_last_name_entry.get()
    }
    # Add Sales Engineer
    se_data = {
        "first_name": se_first_name_entry.get(),
        "last_name": se_last_name_entry.get()
    }
    # Add Project
    project_data = {
        "project_number": project_number_entry.get(),
        "em_type": em_type_entry.get(),
        "job_phase": job_phase_entry.get(),
        "submit_date": submit_date_entry.get()            
    }
    #endregion
    return add_mod_frame, client_data, pm_data, me_data, mc_data, de_data, se_data, project_data

def create_add_modify_window(master,title='Add New _________', button_text='Add or Modify?'):
    
    # Tree created from the parent window, need it so that we can pass it to the buttons to refresh the tree when we add/modify data the table
        # For modifying option, tree is used to determine if user has selected something    
    table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree    

    # # If modifying, this sets the entry data, aka existing record data, as well as the selected record being modified
    # if button_text == 'Modify':   
    #     #Run checks to see if only 1 entry is selected
    #     selected_record = modify_record_properly_selected(table_window_tree,session,model)        
    #     if selected_record is None:            
    #         return
    #     else:            
    #         selected_record_data = {field: getattr(selected_record, field) for field in selected_record.__table__.columns.keys()}
    #         entry_data = selected_record_data
    # else:
    #     default_entry_data = generate_default_entry_data(metadata)        
    #     entry_data = default_entry_data            
            
    # Creates the window
    add_mod_window = tk.Toplevel()
    add_mod_window.title(title)    
    add_mod_window.grid_rowconfigure(0, weight=1)
    add_mod_window.grid_columnconfigure(0, weight=1)
    add_mod_window.resizable(height=False,width=True)

    add_mod_frame, client_data, pm_data, me_data, mc_data, de_data, se_data, project_data = create_add_or_modify_frame(add_mod_window)
    add_mod_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    
    
    # # Adds buttons for adding new mechanical engineers/contractors
    # if model.__tablename__ == 'tblProject':
    #     # Adds an "Add Eng" button to the column of engineers
    #     mech_eng_frame = dividing_frame[3] # [3] represents the column that the mechanical engineer info is in
    #     butt_row = max_rows_in_dividing_frames[3]+1    
    #     add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Engineer', None)])
    #     add_mech_eng_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    #     # Adds an "Add Eng" button to the column of engineers
    #     mech_con_frame = dividing_frame[4]
    #     butt_row = max_rows_in_dividing_frames[4]+1    
    #     add_mech_con_but = create_dynamic_button_frame(mech_con_frame,[('Add Contractor', None)])
    #     add_mech_con_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

    #region Add Project Function
    def add_project_and_related_entities(client_data, pm_data, me_data, mc_data, de_data, se_data, project_data):
        try:
            from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
            from tkinter import messagebox
            # Add Client   
            new_client = Client(**client_data)
            session.add(new_client)
            session.commit()

            # Add Project Manager 
            new_pm = ProjectManager(**pm_data)
            session.add(new_pm)
            session.commit()

            # Add Mechanical Engineer        
            new_me = MechanicalEngineer(**me_data)
            session.add(new_me)
            session.commit()

            # Add Mechanical Contractor        
            new_mc = MechanicalContractor(**mc_data)
            session.add(new_mc)
            session.commit()

            # Add Design Engineer        
            new_de = DesignEngineer(**de_data)
            session.add(new_de)
            session.commit()

            # Add Sales Engineer        
            new_se = SalesEngineer(**se_data)
            session.add(new_se)
            session.commit()

            # Add Project
            project_data.update({
                "client_id": new_client.id,
                "projectmanager_id": new_pm.id,
                "mechanicalengineer_id": new_me.id,
                "mechanicalcontractor_id": new_mc.id,
                "designengineer_id": new_de.id,
                "salesengineer_id": new_se.id
            })
            new_project = Project(**project_data)
            session.add(new_project)
            session.commit()

            messagebox.showinfo("Success", "Project and related entities added successfully!")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
    #endregion

    # Creates the buttons at the bottom of the screen
    button_frame = create_dynamic_button_frame(add_mod_window, [(button_text, lambda:add_project_and_related_entities(client_data, pm_data, me_data, mc_data, de_data, se_data, project_data)),
                                                            ('Cancel', add_mod_window.destroy)])
    button_frame.grid(row=1,column=0,padx=10,pady=(0,10))
    # #Function that defines what the button click will do
    # def add_mod_button_cmd(button_text):     
    #    pass
    #     formatted_entries, error_message=prep_data_entry(add_mod_window,project_entries)            
    #     if error_message:
    #         return
    #     if button_text == 'Add':                      
    #         add_record_to_table(model,session,formatted_entries)
    #         refresh_table(table_window_tree, model, session,columns_to_display)
    #         add_mod_window.destroy()
    #     else:
    #         update_table(session,formatted_entries,selected_record)
    #         refresh_table(table_window_tree, model, session,columns_to_display)
            # add_mod_window.destroy()


    center_window(add_mod_window) 
    add_mod_window.grab_set()     
    add_mod_window.focus_force()  
    master.wait_window(add_mod_window)

