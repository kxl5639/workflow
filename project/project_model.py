from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
from tkinter import messagebox
from project.project_controller import get_entry_data, is_valid_addmodd_data, column_map
from utils import refresh_tree


def add_mod_project(master,project_window, entry_dict, is_modify, selected_record=None):    
    from sqlalchemy.exc import IntegrityError

    #Init
    need_refresh = False

    #Data Validation
    if is_valid_addmodd_data(master, entry_dict, is_modify):    
        
        #Unpack entry_dict
        proj_info_entries = entry_dict[Project.__tablename__]
        client_entries = entry_dict[Client.__tablename__]
        me_entries = entry_dict[MechanicalEngineer.__tablename__]
        mc_entries = entry_dict[MechanicalContractor.__tablename__]    

        # Tree grabbed from project window 
        table_window_tree = project_window.nametowidget('tree_addmoddel_frame').tree_frame.tree
        
        # Init project_id to be used so that when add/modify is complete, the project window will have the updated/added record selected
        project_id = None
        try:
            new_client = Client(**get_entry_data(client_entries))
            session.add(new_client)
            session.commit()

            pm_first_name, pm_last_name = proj_info_entries["pm_name"].get().split()            
            project_manager = session.query(ProjectManager).filter_by(first_name=pm_first_name, last_name=pm_last_name).first()
            if project_manager is None:
                raise ValueError(f"Project Manager {pm_first_name} {pm_last_name} not found.")
            projectmanager_id = project_manager.id

            de_first_name, de_last_name = proj_info_entries["de_name"].get().split()
            design_engineer = session.query(DesignEngineer).filter_by(first_name=de_first_name, last_name=de_last_name).first()
            if design_engineer is None:
                raise ValueError(f"Design Engineer {de_first_name} {de_last_name} not found.")
            designengineer_id = design_engineer.id

            se_first_name, se_last_name = proj_info_entries["se_name"].get().split()
            sales_engineer = session.query(SalesEngineer).filter_by(first_name=se_first_name, last_name=se_last_name).first()
            if sales_engineer is None:
                raise ValueError(f"Sales Engineer {se_first_name} {se_last_name} not found.")
            salesengineer_id = sales_engineer.id

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
                existing_project = session.query(Project).filter_by(id=selected_record.id).first()
                for key, value in project_data.items():
                    setattr(existing_project, key, value)
                session.commit()
                project_id = existing_project.id  # Get the ID of the modified project                
                messagebox.showinfo("Success", "Project modified successfully!")
                need_refresh = True                
            else:
                existing_project = session.query(Project).filter_by(project_number=project_data["project_number"]).first()
                if existing_project:
                    raise IntegrityError("Project number already exists", None, None)
                new_project = Project(**project_data)
                session.add(new_project)
                session.commit()
                project_id = new_project.id  # Get the ID of the modified project                
                messagebox.showinfo("Success", "Project added successfully!")
                need_refresh = True

        except IntegrityError as e:
            session.rollback()
            messagebox.showerror("Error", "Project number already exists. Please use a unique project number.")
        except ValueError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
    
    if need_refresh:
        from project.project_controller import update_table_data    
        table_data = update_table_data()
        refresh_tree(table_window_tree, column_map, table_data)
        master.destroy()
        project_window.lift()
        project_window.focus_set()        
        return project_id
    
    return None  # Return None if no refresh was needed

def delete_selected_projects(master, selected_records=None):
    table_window_tree = master.nametowidget('tree_addmoddel_frame').tree_frame.tree
    from utils import delete_record 
    from project.project_controller import update_table_data         
    for selected_record in selected_records:
        record = session.query(Project).get(selected_record)        
        delete_record(record, session)        
        table_data = update_table_data()  
        refresh_tree(table_window_tree, column_map, table_data)
    

 