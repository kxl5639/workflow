from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session

table_data = session.query(
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
).join(Client, Project.client_id == Client.id)
 .join(ProjectManager, Project.projectmanager_id == ProjectManager.id)\
 .join(MechanicalEngineer, Project.mechanicalengineer_id == MechanicalEngineer.id)\
 .join(MechanicalContractor, Project.mechanicalcontractor_id == MechanicalContractor.id)\
 .join(DesignEngineer, Project.designengineer_id == DesignEngineer.id)\
 .join(SalesEngineer, Project.salesengineer_id == SalesEngineer.id)\
 .all()

# Combine first and last names for project manager, design engineer, and sales engineer
formatted_projects_data = [
    (
        project[0], project[1], project[2], project[3], project[4],
        f"{project[5]} {project[6]}", project[7], project[8],
        f"{project[9]} {project[10]}", f"{project[11]} {project[12]}"
    ) for project in table_data
]

# Example usage
column_map = {
    "project_number": 0,
    "submit_date": 1,
    "client": 2,
    "client_scope": 3,
    "client_address": 4,
    "project_manager": 5,
    "mech_eng": 6,
    "mech_contractor": 7,
    "design_eng": 8,
    "sales_eng": 9
}


print(table_data)

