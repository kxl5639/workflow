from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
from tkinter import messagebox
from project.project_controller import get_entry_data, validate_data

def add_mod_project(proj_info_entries,
                    client_entries, me_entries,
                    mc_entries, is_modify, selected_record=None):    
    from sqlalchemy.exc import IntegrityError
    
    #Data Validation
    if validate_data():    
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
                existing_project = session.query(Project).filter_by(id=selected_record.id).first()
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
    else:
        return
