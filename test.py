import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import aliased
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    project_number = Column(String, nullable=False, unique=True)
    em_type = Column(String, nullable=False)
    job_phase = Column(Integer, nullable=False)
    submit_date = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    projectmanager_id = Column(Integer, ForeignKey('projectmanagers.id'), nullable=False)
    mechanicalengineer_id = Column(Integer, ForeignKey('mechanicalengineers.id'), nullable=False)
    mechanicalcontractor_id = Column(Integer, ForeignKey('mechanicalcontractors.id'), nullable=False)
    designengineer_id = Column(Integer, ForeignKey('designengineers.id'), nullable=False)
    salesengineer_id = Column(Integer, ForeignKey('salesengineers.id'), nullable=False)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    client_name = Column(String, nullable=False)
    scope = Column(String, nullable=False)
    address = Column(String, nullable=False)

class ProjectManager(Base):
    __tablename__ = 'projectmanagers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class MechanicalEngineer(Base):
    __tablename__ = 'mechanicalengineers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class MechanicalContractor(Base):
    __tablename__ = 'mechanicalcontractors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class DesignEngineer(Base):
    __tablename__ = 'designengineers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class SalesEngineer(Base):
    __tablename__ = 'salesengineers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

# Setup the database connection
DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Aliasing the classes for better query readability
ClientAlias = aliased(Client)
ProjectManagerAlias = aliased(ProjectManager)
MechanicalEngineerAlias = aliased(MechanicalEngineer)
MechanicalContractorAlias = aliased(MechanicalContractor)
DesignEngineerAlias = aliased(DesignEngineer)
SalesEngineerAlias = aliased(SalesEngineer)

# Query to get the required data
projects_data = session.query(
    Project.project_number,
    Project.submit_date,
    ClientAlias.client_name,
    ClientAlias.scope,
    ClientAlias.address,
    ProjectManagerAlias.first_name,
    ProjectManagerAlias.last_name,
    MechanicalEngineerAlias.name,
    MechanicalContractorAlias.name,
    DesignEngineerAlias.first_name,
    DesignEngineerAlias.last_name,
    SalesEngineerAlias.first_name,
    SalesEngineerAlias.last_name
).join(ClientAlias, Project.client_id == ClientAlias.id)\
 .join(ProjectManagerAlias, Project.projectmanager_id == ProjectManagerAlias.id)\
 .join(MechanicalEngineerAlias, Project.mechanicalengineer_id == MechanicalEngineerAlias.id)\
 .join(MechanicalContractorAlias, Project.mechanicalcontractor_id == MechanicalContractorAlias.id)\
 .join(DesignEngineerAlias, Project.designengineer_id == DesignEngineerAlias.id)\
 .join(SalesEngineerAlias, Project.salesengineer_id == SalesEngineerAlias.id)\
 .all()

# Function to create the treeview and populate it
def create_treeview():
    root = tk.Tk()
    root.title("Project TreeView")

    tree = ttk.Treeview(root)
    tree["columns"] = ("project_number", "submit_date", "client", "client_scope", "client_address",
                       "project_manager", "mech_eng", "mech_contractor", "design_eng", "sales_eng")
    
    tree.heading("project_number", text="Project Number")
    tree.heading("submit_date", text="Submit Date")
    tree.heading("client", text="Client")
    tree.heading("client_scope", text="Client Scope")
    tree.heading("client_address", text="Client Address")
    tree.heading("project_manager", text="Project Manager")
    tree.heading("mech_eng", text="Mechanical Engineer")
    tree.heading("mech_contractor", text="Mechanical Contractor")
    tree.heading("design_eng", text="Design Engineer")
    tree.heading("sales_eng", text="Sales Engineer")

    tree.column("project_number", width=100)
    tree.column("submit_date", width=100)
    tree.column("client", width=100)
    tree.column("client_scope", width=100)
    tree.column("client_address", width=150)
    tree.column("project_manager", width=150)
    tree.column("mech_eng", width=150)
    tree.column("mech_contractor", width=150)
    tree.column("design_eng", width=150)
    tree.column("sales_eng", width=150)

    for project in projects_data:
        project_manager = f"{project[5]} {project[6]}"
        design_engineer = f"{project[9]} {project[10]}"
        sales_engineer = f"{project[11]} {project[12]}"
        
        tree.insert("", "end", text=project[0],
                    values=(project[0], project[1], project[2], project[3], project[4],
                            project_manager, project[7], project[8], design_engineer, sales_engineer))

    tree.pack(expand=True, fill='both')
    root.mainloop()

create_treeview()
