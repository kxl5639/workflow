from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
import sqlalchemy

class ProjectListWindowModel:
    def __init__(self) -> None:
        self.colump_map = {"project_number": 1,
                           "submit_date": 2,
                           "client": 3,
                           "client_scope": 4,
                           "client_address": 5,
                           "project_manager": 6,
                           "mech_eng": 7,
                           "mech_contractor": 8,
                           "design_eng": 9,
                           "sales_eng": 10
                           }
        self.table_data = self.update_table_data()
        
    def update_table_data(self):
        unformatted_table_data = session.query(
            Project.id,  # Include the primary key
            Project.project_number,
            Project.submit_date,
            Client.client_name,
            Client.scope,
            Client.address,
            ProjectManager.first_name,
            ProjectManager.last_name,
            MechanicalEngineer.name,
            MechanicalContractor.name,
            DesignEngineer.first_name,
            DesignEngineer.last_name,
            SalesEngineer.first_name,
            SalesEngineer.last_name
        ).join(Client, Project.client_id == Client.id)\
        .join(ProjectManager, Project.projectmanager_id == ProjectManager.id)\
        .join(MechanicalEngineer, Project.mechanicalengineer_id == MechanicalEngineer.id)\
        .join(MechanicalContractor, Project.mechanicalcontractor_id == MechanicalContractor.id)\
        .join(DesignEngineer, Project.designengineer_id == DesignEngineer.id)\
        .join(SalesEngineer, Project.salesengineer_id == SalesEngineer.id)\
        .all()

        # Combine first and last names for project manager, design engineer, and sales engineer
        table_data = [
            (
                project[0],  # Primary key
                project[1], project[2], project[3], project[4], project[5],
                f"{project[6]} {project[7]}", project[8], project[9],
                f"{project[10]} {project[11]}", f"{project[12]} {project[13]}"
            ) for project in unformatted_table_data
        ]
        return table_data
    
    def delete_record(self, object_list):
        for obj in object_list:
            session.delete(obj)

    def add_record(self, record_obj):
        session.add(record_obj)

    def commit_changes(self):
        session.commit()

    def query_proj_nums(self):
        return session.query(Project.project_number).all()
 