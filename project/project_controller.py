from model import Client, Project, ProjectManager, DesignEngineer, SalesEngineer, MechanicalContractor, MechanicalEngineer, session
import tkinter as tk

columns_to_display = ['project_number', 'submittal_date', 'client', 'scope', 'address',
               'project_manager', 'mechanical_engineer', 'mechanical_contractor', 'design_engineer', 'sales_engineer']

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

# Example usage
column_map = {
    "project_number": 1,
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

def fetch_record_data(record_id):
    from model import Client, ProjectManager, MechanicalContractor, MechanicalEngineer, DesignEngineer, SalesEngineer, Project, session
    project = session.query(Project).filter_by(id=record_id).first()
    client = session.query(Client).filter_by(id=project.client_id).first()
    pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
    me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
    mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
    de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
    se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
    return project, client, pm, me, mc, de, se

def fetch_names(model):
    return [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).all()]

def get_entry_data(entries):
    return {key: entry.get() for key, entry in entries.items()}

def set_entry_state(entry, state):
    entry.config(state=state)

def set_entry_text(entry_widget, text):
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, text)

def validate_data(): # Validates data to be added or updated to database
    return True