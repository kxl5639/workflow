# import tkinter as tk
# from tkinter import ttk
# from configs import testing
# from utils import center_window, create_dynamic_button_frame

# def set_entry_text(entry_widget, testing, testing_text, production_text):
#     entry_widget.insert(0, testing_text if testing == 1 else production_text)


# def create_add_or_modify_frame(master):

#     #region Create Frames, Labels, and Entry Widgets
#     add_mod_frame = ttk.Frame(master)
#     # add_mod_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')   
#     add_mod_frame.grid_rowconfigure(0, weight=1)
#     add_mod_frame.grid_columnconfigure(0, weight=1)
#     add_mod_frame.grid_columnconfigure(1, weight=1)
#     add_mod_frame.grid_columnconfigure(2, weight=1)
#     add_mod_frame.grid_columnconfigure(3, weight=1)

#     # Create labels and entry boxes
#     proj_info_frame = ttk.Labelframe(add_mod_frame, text = "Project Info")
#     proj_info_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
#     proj_info_frame.grid_columnconfigure((1), weight=1)

#     ttk.Label(proj_info_frame, text="Project Number").grid(row=0, column=0, padx=10, pady=10,sticky="w")
#     project_number_entry = ttk.Entry(proj_info_frame)
#     project_number_entry.grid(row=0, column=1,padx=(0,10),pady=10,sticky='ew')
#     set_entry_text(project_number_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="EM Type").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
#     em_type_entry = ttk.Entry(proj_info_frame)
#     em_type_entry.grid(row=1, column=1,padx=(0,10), pady=(0,10), sticky='ew')
#     set_entry_text(em_type_entry, testing, 'Testing', 'B')

#     ttk.Label(proj_info_frame, text="Job Phase").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
#     job_phase_entry = ttk.Entry(proj_info_frame)
#     job_phase_entry.grid(row=2, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(job_phase_entry, testing, 'Testing', '1')

#     ttk.Label(proj_info_frame, text="Submit Date").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
#     submit_date_entry = ttk.Entry(proj_info_frame)
#     submit_date_entry.grid(row=3, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(submit_date_entry, testing, 'Testing', 'XX/XX/XX')

#     ttk.Label(proj_info_frame, text="PM First Name").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
#     pm_first_name_entry = ttk.Entry(proj_info_frame)
#     pm_first_name_entry.grid(row=4, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(pm_first_name_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="PM Last Name").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
#     pm_last_name_entry = ttk.Entry(proj_info_frame)
#     pm_last_name_entry.grid(row=5, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(pm_last_name_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="DE First Name").grid(row=6, column=0, padx=10, pady=(0,10),sticky="w")
#     de_first_name_entry = ttk.Entry(proj_info_frame)
#     de_first_name_entry.grid(row=6, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(de_first_name_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="DE Last Name").grid(row=7, column=0, padx=10, pady=(0,10),sticky="w")
#     de_last_name_entry = ttk.Entry(proj_info_frame)
#     de_last_name_entry.grid(row=7, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(de_last_name_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="SE First Name").grid(row=8, column=0, padx=10, pady=(0,10),sticky="w")
#     se_first_name_entry = ttk.Entry(proj_info_frame)
#     se_first_name_entry.grid(row=8, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(se_first_name_entry, testing, 'Testing', '')

#     ttk.Label(proj_info_frame, text="SE Last Name").grid(row=9, column=0, padx=10, pady=(0,10),sticky="w")
#     se_last_name_entry = ttk.Entry(proj_info_frame)
#     se_last_name_entry.grid(row=9, column=1,padx=(0,10), pady=(0,10),sticky='ew')
#     set_entry_text(se_last_name_entry, testing, 'Testing', '')

#     client_frame = ttk.Labelframe(add_mod_frame, text = "Client")
#     client_frame.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')
#     client_frame.grid_columnconfigure((1), weight=1)
    
#     ttk.Label(client_frame, text="Client").grid(row=0, column=0, padx=10, pady=10,sticky="w")
#     client_entry = ttk.Entry(client_frame)
#     client_entry.grid(row=0, column=1,padx=(0,10),sticky='ew')
#     set_entry_text(client_entry, testing, 'Testing', '')
    
#     ttk.Label(client_frame, text="Scope").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
#     client_scope = ttk.Entry(client_frame)
#     client_scope.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(client_scope, testing, 'Testing', '')

#     ttk.Label(client_frame, text="Address").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
#     client_address = ttk.Entry(client_frame)
#     client_address.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(client_address, testing, 'Testing', '')

#     ttk.Label(client_frame, text="City").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
#     client_city = ttk.Entry(client_frame)
#     client_city.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(client_city, testing, 'Testing', '')

#     ttk.Label(client_frame, text="State").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
#     client_state = ttk.Entry(client_frame)
#     client_state.grid(row=4, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(client_state, testing, 'Testing', '')

#     ttk.Label(client_frame, text="Zip Code").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
#     client_zip_code = ttk.Entry(client_frame)
#     client_zip_code.grid(row=5, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(client_zip_code, testing, 'Testing', '')

#     mecheng_frame = ttk.Labelframe(add_mod_frame, text = "Mechanical Engineer")
#     mecheng_frame.grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
#     mecheng_frame.grid_columnconfigure((1), weight=1)

#     ttk.Label(mecheng_frame, text="Name").grid(row=0, column=0, padx=10, pady=10,sticky="w")
#     mecheng_name = ttk.Entry(mecheng_frame)
#     mecheng_name.grid(row=0, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mecheng_name, testing, 'Testing', '')

#     ttk.Label(mecheng_frame, text="Address").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
#     mecheng_address = ttk.Entry(mecheng_frame)
#     mecheng_address.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mecheng_address, testing, 'Testing', '')

#     ttk.Label(mecheng_frame, text="City").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
#     mecheng_city = ttk.Entry(mecheng_frame)
#     mecheng_city.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mecheng_city, testing, 'Testing', '')

#     ttk.Label(mecheng_frame, text="State").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
#     mecheng_state = ttk.Entry(mecheng_frame)
#     mecheng_state.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mecheng_state, testing, 'Testing', '')

#     ttk.Label(mecheng_frame, text="Zip Code").grid(row=4, column=0, padx=10, pady=(0,10),sticky="w")
#     mecheng_zip_code = ttk.Entry(mecheng_frame)
#     mecheng_zip_code.grid(row=4, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mecheng_zip_code, testing, 'Testing', '')

#     mechcon_frame = ttk.Labelframe(add_mod_frame, text = "Mechanical Contractor")
#     mechcon_frame.grid(row=0,column=3,padx=10,pady=10,sticky='nsew')
#     mechcon_frame.grid_columnconfigure((1), weight=1)

#     ttk.Label(mechcon_frame, text="Name").grid(row=0, column=0, padx=10, pady=10,sticky="w")
#     mechcon_name = ttk.Entry(mechcon_frame)
#     mechcon_name.grid(row=0, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_name, testing, 'Testing', '')

#     ttk.Label(mechcon_frame, text="Address").grid(row=1, column=0, padx=10, pady=(0,10),sticky="w")
#     mechcon_address = ttk.Entry(mechcon_frame)
#     mechcon_address.grid(row=1, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_address, testing, 'Testing', '')

#     ttk.Label(mechcon_frame, text="City").grid(row=2, column=0, padx=10, pady=(0,10),sticky="w")
#     mechcon_city = ttk.Entry(mechcon_frame)
#     mechcon_city.grid(row=2, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_city, testing, 'Testing', '')

#     ttk.Label(mechcon_frame, text="State").grid(row=3, column=0, padx=10, pady=(0,10),sticky="w")
#     mechcon_state = ttk.Entry(mechcon_frame)
#     mechcon_state.grid(row=3, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_state, testing, 'Testing', '')

#     ttk.Label(mechcon_frame, text="Zip Code").grid(row=5, column=0, padx=10, pady=(0,10),sticky="w")
#     mechcon_zip_code = ttk.Entry(mechcon_frame)
#     mechcon_zip_code.grid(row=5, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_zip_code, testing, 'Testing', '')

#     ttk.Label(mechcon_frame, text="Telephone").grid(row=6, column=0, padx=10, pady=(0,10),sticky="w")
#     mechcon_phone = ttk.Entry(mechcon_frame)
#     mechcon_phone.grid(row=6, column=1,padx=(0,10),pady=(0,10),sticky='ew')
#     set_entry_text(mechcon_phone, testing, 'Testing', '')
#     #endregion
#     #region Get Entry data
#     # Add Client
#     client_data = {
#         "client_name": client_entry.get(),
#         "scope": client_scope.get(),
#         "address": client_address.get(),
#         "city": client_city.get(),
#         "state": client_state.get(),
#         "zip_code": client_zip_code.get()
#     }
#     # Add Project Manager
#     pm_data = {
#         "first_name": pm_first_name_entry.get(),
#         "last_name": pm_last_name_entry.get()
#     }
#     # Add Mechanical Engineer
#     me_data = {
#         "name": mecheng_name.get(),
#         "address": mecheng_address.get(),
#         "city": mecheng_city.get(),
#         "state": mecheng_state.get(),
#         "zip_code": mecheng_zip_code.get()
#     }
#     # Add Mechanical Contractor
#     mc_data = {
#         "name": mechcon_name.get(),
#         "address": mechcon_address.get(),
#         "city": mechcon_city.get(),
#         "state": mechcon_state.get(),
#         "zip_code": mechcon_zip_code.get(),
#         "telephone": mechcon_phone.get()
#     }
#     # Add Design Engineer
#     de_data = {
#         "first_name": de_first_name_entry.get(),
#         "last_name": de_last_name_entry.get()
#     }
#     # Add Sales Engineer
#     se_data = {
#         "first_name": se_first_name_entry.get(),
#         "last_name": se_last_name_entry.get()
#     }
#     # Add Project
#     project_data = {
#         "project_number": project_number_entry.get(),
#         "em_type": em_type_entry.get(),
#         "job_phase": job_phase_entry.get(),
#         "submit_date": submit_date_entry.get()            
#     }
#     #endregion
#     return add_mod_frame, client_data, pm_data, me_data, mc_data, de_data, se_data, project_data

# def create_add_modify_window(master,title='Add New _________', button_text='Add or Modify?'):
    
#     # Tree created from the parent window, need it so that we can pass it to the buttons to refresh the tree when we add/modify data the table
#         # For modifying option, tree is used to determine if user has selected something    
#     table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree    

#     # # If modifying, this sets the entry data, aka existing record data, as well as the selected record being modified
#     # if button_text == 'Modify':   
#     #     #Run checks to see if only 1 entry is selected
#     #     selected_record = modify_record_properly_selected(table_window_tree,session,model)        
#     #     if selected_record is None:            
#     #         return
#     #     else:            
#     #         selected_record_data = {field: getattr(selected_record, field) for field in selected_record.__table__.columns.keys()}
#     #         entry_data = selected_record_data
#     # else:
#     #     default_entry_data = generate_default_entry_data(metadata)        
#     #     entry_data = default_entry_data            
            
#     # Creates the window
#     add_mod_window = tk.Toplevel()
#     add_mod_window.title(title)    
#     add_mod_window.grid_rowconfigure(0, weight=1)
#     add_mod_window.grid_columnconfigure(0, weight=1)
#     add_mod_window.resizable(height=False,width=True)

#     add_mod_frame, client_data, pm_data, me_data, mc_data, de_data, se_data, project_data = create_add_or_modify_frame(add_mod_window)
#     add_mod_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')    
    
#     # # Adds buttons for adding new mechanical engineers/contractors
#     # if model.__tablename__ == 'tblProject':
#     #     # Adds an "Add Eng" button to the column of engineers
#     #     mech_eng_frame = dividing_frame[3] # [3] represents the column that the mechanical engineer info is in
#     #     butt_row = max_rows_in_dividing_frames[3]+1    
#     #     add_mech_eng_but = create_dynamic_button_frame(mech_eng_frame,[('Add Engineer', None)])
#     #     add_mech_eng_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

#     #     # Adds an "Add Eng" button to the column of engineers
#     #     mech_con_frame = dividing_frame[4]
#     #     butt_row = max_rows_in_dividing_frames[4]+1    
#     #     add_mech_con_but = create_dynamic_button_frame(mech_con_frame,[('Add Contractor', None)])
#     #     add_mech_con_but.grid(row=butt_row,column=0,columnspan = 2, pady=(10,0))

#     #region Add Project Function
#     def add_project_and_related_entities(client_data, pm_data, me_data, mc_data, de_data, se_data, project_data):
#         try:
#             from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
#             from tkinter import messagebox
#             # Add Client   
#             new_client = Client(**client_data)
#             session.add(new_client)
#             session.commit()

#             # Add Project Manager 
#             new_pm = ProjectManager(**pm_data)
#             session.add(new_pm)
#             session.commit()

#             # Add Mechanical Engineer        
#             new_me = MechanicalEngineer(**me_data)
#             session.add(new_me)
#             session.commit()

#             # Add Mechanical Contractor        
#             new_mc = MechanicalContractor(**mc_data)
#             session.add(new_mc)
#             session.commit()

#             # Add Design Engineer        
#             new_de = DesignEngineer(**de_data)
#             session.add(new_de)
#             session.commit()

#             # Add Sales Engineer        
#             new_se = SalesEngineer(**se_data)
#             session.add(new_se)
#             session.commit()

#             # Add Project
#             project_data.update({
#                 "client_id": new_client.id,
#                 "projectmanager_id": new_pm.id,
#                 "mechanicalengineer_id": new_me.id,
#                 "mechanicalcontractor_id": new_mc.id,
#                 "designengineer_id": new_de.id,
#                 "salesengineer_id": new_se.id
#             })
#             new_project = Project(**project_data)
#             session.add(new_project)
#             session.commit()

#             messagebox.showinfo("Success", "Project and related entities added successfully!")
#         except Exception as e:
#             session.rollback()
#             messagebox.showerror("Error", str(e))
#     #endregion

#     # Creates the buttons at the bottom of the screen
#     button_frame = create_dynamic_button_frame(add_mod_window, [(button_text, lambda:add_project_and_related_entities(client_data, pm_data, me_data, mc_data, de_data, se_data, project_data)),
#                                                             ('Cancel', add_mod_window.destroy)])
#     button_frame.grid(row=1,column=0,padx=10,pady=(0,10))
#     # #Function that defines what the button click will do
#     # def add_mod_button_cmd(button_text):     
#     #    pass
#     #     formatted_entries, error_message=prep_data_entry(add_mod_window,project_entries)            
#     #     if error_message:
#     #         return
#     #     if button_text == 'Add':                      
#     #         add_record_to_table(model,session,formatted_entries)
#     #         refresh_table(table_window_tree, model, session,columns_to_display)
#     #         add_mod_window.destroy()
#     #     else:
#     #         update_table(session,formatted_entries,selected_record)
#     #         refresh_table(table_window_tree, model, session,columns_to_display)
#             # add_mod_window.destroy()


#     center_window(add_mod_window) 
#     add_mod_window.grab_set()     
#     add_mod_window.focus_force()  
#     master.wait_window(add_mod_window)
























# import tkinter as tk
# from tkinter import ttk
# from configs import testing
# from utils import center_window, create_dynamic_button_frame
# from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
# from tkinter import messagebox
# from sqlalchemy.exc import IntegrityError


# def set_entry_text(entry_widget, testing, testing_text, production_text):
#     entry_widget.insert(0, testing_text if testing == 1 else production_text)


# def create_label_entry(parent, label_text, row, column, default_text=''):
#     ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
#     entry = ttk.Entry(parent)
#     entry.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
#     set_entry_text(entry, testing, 'Testing', default_text)
#     return entry


# def create_frame(parent, text, row, column):
#     frame = ttk.Labelframe(parent, text=text)
#     frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
#     frame.grid_columnconfigure(1, weight=1)
#     return frame


# def get_entry_data(entries):
#     return {key: entry.get() for key, entry in entries.items()}


# def create_combobox(parent, label_text, values, row, column):
#     ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
#     combobox = ttk.Combobox(parent, values=values, state="readonly")
#     combobox.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
#     return combobox


# def fetch_names(model):
#     return [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).all()]


# def create_add_or_modify_frame(master):
#     add_mod_frame = ttk.Frame(master)
#     add_mod_frame.grid_rowconfigure(0, weight=1)
#     add_mod_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

#     proj_info_frame = create_frame(add_mod_frame, "Project Info", 0, 0)
#     proj_info_entries = {
#         "project_number": create_label_entry(proj_info_frame, "Project Number", 0, 0, ''),
#         "em_type": create_label_entry(proj_info_frame, "EM Type", 1, 0, 'B'),
#         "job_phase": create_label_entry(proj_info_frame, "Job Phase", 2, 0, '1'),
#         "submit_date": create_label_entry(proj_info_frame, "Submit Date", 3, 0, 'XX/XX/XX'),
#     }

#     # Fetch names for comboboxes
#     pm_names = fetch_names(ProjectManager)
#     de_names = fetch_names(DesignEngineer)
#     se_names = fetch_names(SalesEngineer)

#     proj_info_entries.update({
#         "pm_name": create_combobox(proj_info_frame, "Project Manager", pm_names, 4, 0),
#         "de_name": create_combobox(proj_info_frame, "Design Engineer", de_names, 5, 0),
#         "se_name": create_combobox(proj_info_frame, "Sales Engineer", se_names, 6, 0),
#     })

#     client_frame = create_frame(add_mod_frame, "Client", 0, 1)
#     client_entries = {
#         "client_name": create_label_entry(client_frame, "Client", 0, 0, ''),
#         "scope": create_label_entry(client_frame, "Scope", 1, 0, ''),
#         "address": create_label_entry(client_frame, "Address", 2, 0, ''),
#         "city": create_label_entry(client_frame, "City", 3, 0, ''),
#         "state": create_label_entry(client_frame, "State", 4, 0, ''),
#         "zip_code": create_label_entry(client_frame, "Zip Code", 5, 0, '')
#     }

#     me_frame = create_frame(add_mod_frame, "Mechanical Engineer", 0, 2)
#     me_entries = {
#         "name": create_label_entry(me_frame, "Name", 0, 0, ''),
#         "address": create_label_entry(me_frame, "Address", 1, 0, ''),
#         "city": create_label_entry(me_frame, "City", 2, 0, ''),
#         "state": create_label_entry(me_frame, "State", 3, 0, ''),
#         "zip_code": create_label_entry(me_frame, "Zip Code", 4, 0, '')
#     }

#     mc_frame = create_frame(add_mod_frame, "Mechanical Contractor", 0, 3)
#     mc_entries = {
#         "name": create_label_entry(mc_frame, "Name", 0, 0, ''),
#         "address": create_label_entry(mc_frame, "Address", 1, 0, ''),
#         "city": create_label_entry(mc_frame, "City", 2, 0, ''),
#         "state": create_label_entry(mc_frame, "State", 3, 0, ''),
#         "zip_code": create_label_entry(mc_frame, "Zip Code", 4, 0, ''),
#         "telephone": create_label_entry(mc_frame, "Telephone", 5, 0, '')
#     }

#     return add_mod_frame, proj_info_entries, client_entries, me_entries, mc_entries


# def create_add_modify_window(master, title='Add New _________', button_text='Add or Modify?'):
#     add_mod_window = tk.Toplevel()
#     add_mod_window.title(title)
#     add_mod_window.grid_rowconfigure(0, weight=1)
#     add_mod_window.grid_columnconfigure(0, weight=1)
#     add_mod_window.resizable(height=False, width=True)

#     add_mod_frame, proj_info_entries, client_entries, me_entries, mc_entries = create_add_or_modify_frame(add_mod_window)
#     add_mod_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

#     def add_project_and_related_entities():
#         try:
#             new_client = Client(**get_entry_data(client_entries))
#             session.add(new_client)
#             session.commit()

#             pm_first_name, pm_last_name = proj_info_entries["pm_name"].get().split()
#             projectmanager_id = session.query(ProjectManager).filter_by(first_name=pm_first_name, last_name=pm_last_name).first().id

#             de_first_name, de_last_name = proj_info_entries["de_name"].get().split()
#             designengineer_id = session.query(DesignEngineer).filter_by(first_name=de_first_name, last_name=de_last_name).first().id

#             se_first_name, se_last_name = proj_info_entries["se_name"].get().split()
#             salesengineer_id = session.query(SalesEngineer).filter_by(first_name=se_first_name, last_name=se_last_name).first().id

#             new_me = MechanicalEngineer(**get_entry_data(me_entries))
#             session.add(new_me)
#             session.commit()

#             new_mc = MechanicalContractor(**get_entry_data(mc_entries))
#             session.add(new_mc)
#             session.commit()

#             project_data = {
#                 "project_number": proj_info_entries["project_number"].get(),
#                 "em_type": proj_info_entries["em_type"].get(),
#                 "job_phase": proj_info_entries["job_phase"].get(),
#                 "submit_date": proj_info_entries["submit_date"].get(),
#                 "client_id": new_client.id,
#                 "projectmanager_id": projectmanager_id,
#                 "mechanicalengineer_id": new_me.id,
#                 "mechanicalcontractor_id": new_mc.id,
#                 "designengineer_id": designengineer_id,
#                 "salesengineer_id": salesengineer_id
#             }

#             existing_project = session.query(Project).filter_by(project_number=project_data["project_number"]).first()
#             if existing_project:
#                 raise IntegrityError("Project number already exists", None, None)

#             new_project = Project(**project_data)
#             session.add(new_project)
#             session.commit()

#             messagebox.showinfo("Success", "Project and related entities added successfully!")
#         except IntegrityError as e:
#             session.rollback()
#             messagebox.showerror("Error", "Project number already exists. Please use a unique project number.")
#         except Exception as e:
#             session.rollback()
#             messagebox.showerror("Error", str(e))

#     button_frame = create_dynamic_button_frame(add_mod_window, [(button_text, add_project_and_related_entities), ('Cancel', add_mod_window.destroy)])
#     button_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

#     center_window(add_mod_window)
#     add_mod_window.grab_set()
#     add_mod_window.focus_force()
#     master.wait_window(add_mod_window)
























































import tkinter as tk
from tkinter import ttk
from configs import testing
from utils import center_window, create_dynamic_button_frame
from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
from tkinter import messagebox
from sqlalchemy.exc import IntegrityError


def set_entry_text(entry_widget, text):
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, text)


def create_label_entry(parent, label_text, row, column, default_text='', readonly=False, testing=False):
    ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
    entry = ttk.Entry(parent, state='readonly' if readonly else 'normal')
    entry.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
    if testing:
        set_entry_text(entry, 'Testing')
    else:
        set_entry_text(entry, default_text)
    return entry



def create_frame(parent, text, row, column):
    frame = ttk.Labelframe(parent, text=text)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
    frame.grid_columnconfigure(1, weight=1)
    return frame


def get_entry_data(entries):
    return {key: entry.get() for key, entry in entries.items()}


def create_combobox(parent, label_text, values, row, column):
    ttk.Label(parent, text=label_text).grid(row=row, column=column, padx=10, pady=10, sticky="w")
    combobox = ttk.Combobox(parent, values=values, state="readonly")
    combobox.grid(row=row, column=column + 1, padx=(0, 10), pady=10, sticky='ew')
    return combobox


def fetch_names(model):
    return [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).all()]


def fetch_record_data(record_id):
    project = session.query(Project).filter_by(id=record_id).first()
    client = session.query(Client).filter_by(id=project.client_id).first()
    pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
    me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
    mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
    de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
    se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
    return project, client, pm, me, mc, de, se


def create_add_or_modify_frame(master, is_modify=False, selected_record=None):
    add_mod_frame = ttk.Frame(master)
    add_mod_frame.grid_rowconfigure(0, weight=1)
    add_mod_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    proj_info_frame = create_frame(add_mod_frame, "Project Info", 0, 0)
    proj_info_entries = {
        "project_number": create_label_entry(proj_info_frame, "Project Number", 0, 0, '', readonly=is_modify, testing=not is_modify),
        "em_type": create_label_entry(proj_info_frame, "EM Type", 1, 0, 'B', testing=not is_modify),
        "job_phase": create_label_entry(proj_info_frame, "Job Phase", 2, 0, '1', testing=not is_modify),
        "submit_date": create_label_entry(proj_info_frame, "Submit Date", 3, 0, 'XX/XX/XX', testing=not is_modify),
    }

    # Fetch names for comboboxes
    pm_names = fetch_names(ProjectManager)
    de_names = fetch_names(DesignEngineer)
    se_names = fetch_names(SalesEngineer)

    proj_info_entries.update({
        "pm_name": create_combobox(proj_info_frame, "Project Manager", pm_names, 4, 0),
        "de_name": create_combobox(proj_info_frame, "Design Engineer", de_names, 5, 0),
        "se_name": create_combobox(proj_info_frame, "Sales Engineer", se_names, 6, 0),
    })

    client_frame = create_frame(add_mod_frame, "Client", 0, 1)
    client_entries = {
        "client_name": create_label_entry(client_frame, "Client", 0, 0, '', testing=not is_modify),
        "scope": create_label_entry(client_frame, "Scope", 1, 0, '', testing=not is_modify),
        "address": create_label_entry(client_frame, "Address", 2, 0, '', testing=not is_modify),
        "city": create_label_entry(client_frame, "City", 3, 0, '', testing=not is_modify),
        "state": create_label_entry(client_frame, "State", 4, 0, '', testing=not is_modify),
        "zip_code": create_label_entry(client_frame, "Zip Code", 5, 0, '', testing=not is_modify)
    }

    me_frame = create_frame(add_mod_frame, "Mechanical Engineer", 0, 2)
    me_entries = {
        "name": create_label_entry(me_frame, "Name", 0, 0, '', testing=not is_modify),
        "address": create_label_entry(me_frame, "Address", 1, 0, '', testing=not is_modify),
        "city": create_label_entry(me_frame, "City", 2, 0, '', testing=not is_modify),
        "state": create_label_entry(me_frame, "State", 3, 0, '', testing=not is_modify),
        "zip_code": create_label_entry(me_frame, "Zip Code", 4, 0, '', testing=not is_modify)
    }

    mc_frame = create_frame(add_mod_frame, "Mechanical Contractor", 0, 3)
    mc_entries = {
        "name": create_label_entry(mc_frame, "Name", 0, 0, '', testing=not is_modify),
        "address": create_label_entry(mc_frame, "Address", 1, 0, '', testing=not is_modify),
        "city": create_label_entry(mc_frame, "City", 2, 0, '', testing=not is_modify),
        "state": create_label_entry(mc_frame, "State", 3, 0, '', testing=not is_modify),
        "zip_code": create_label_entry(mc_frame, "Zip Code", 4, 0, '', testing=not is_modify),
        "telephone": create_label_entry(mc_frame, "Telephone", 5, 0, '', testing=not is_modify)
    }

    if is_modify and selected_record:
        project, client, pm, me, mc, de, se = fetch_record_data(selected_record)
        set_entry_text(proj_info_entries["project_number"], project.project_number)
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

    return add_mod_frame, proj_info_entries, client_entries, me_entries, mc_entries


def create_add_modify_window(master, title='Add New _________', button_text='Add or Modify?', selected_record=None):
    is_modify = button_text.lower() == 'modify'
    add_mod_window = tk.Toplevel()
    add_mod_window.title(title)
    add_mod_window.grid_rowconfigure(0, weight=1)
    add_mod_window.grid_columnconfigure(0, weight=1)
    add_mod_window.resizable(height=False, width=True)

    add_mod_frame, proj_info_entries, client_entries, me_entries, mc_entries = create_add_or_modify_frame(add_mod_window, is_modify, selected_record)
    add_mod_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def add_project_and_related_entities():
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

            if is_modify:
                existing_project = session.query(Project).filter_by(id=selected_record).first()
                for key, value in project_data.items():
                    setattr(existing_project, key, value)
                session.commit()
                messagebox.showinfo("Success", "Project and related entities modified successfully!")
            else:
                existing_project = session.query(Project).filter_by(project_number=project_data["project_number"]).first()
                if existing_project:
                    raise IntegrityError("Project number already exists", None, None)

                new_project = Project(**project_data)
                session.add(new_project)
                session.commit()
                messagebox.showinfo("Success", "Project and related entities added successfully!")

        except IntegrityError as e:
            session.rollback()
            messagebox.showerror("Error", "Project number already exists. Please use a unique project number.")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))

    button_frame = create_dynamic_button_frame(add_mod_window, [(button_text, add_project_and_related_entities), ('Cancel', add_mod_window.destroy)])
    button_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

    center_window(add_mod_window)
    add_mod_window.grab_set()
    add_mod_window.focus_force()
    master.wait_window(add_mod_window)

