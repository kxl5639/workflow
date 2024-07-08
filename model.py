import os
import json
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import ForeignKey, create_engine
from typing import List
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = 'projects'
    id:Mapped[int] = mapped_column(primary_key=True)
    project_number:Mapped[str] = mapped_column(nullable=False, unique=True)
    em_type:Mapped[str] = mapped_column(nullable=False)
    job_phase:Mapped[int] = mapped_column(nullable=False)
    submit_date:Mapped[str] = mapped_column(nullable=False)
    client_id:Mapped[int] = mapped_column(ForeignKey('clients.id'),nullable=False)
    client:Mapped['Client'] = relationship(back_populates='projects')
    projectmanager_id:Mapped[int] = mapped_column(ForeignKey('projectmanagers.id'),nullable=False)
    projectmanager:Mapped['ProjectManager'] = relationship(back_populates='projects')
    mechanicalengineer_id:Mapped[int] = mapped_column(ForeignKey('mechanicalengineers.id'),nullable=False)
    mechanicalengineer:Mapped['MechanicalEngineer'] = relationship(back_populates='projects')
    mechanicalcontractor_id:Mapped[int] = mapped_column(ForeignKey('mechanicalcontractors.id'),nullable=False)
    mechanicalcontractor:Mapped['MechanicalContractor'] = relationship(back_populates='projects')
    designengineer_id:Mapped[int] = mapped_column(ForeignKey('designengineers.id'),nullable=False)
    designengineer:Mapped['DesignEngineer'] = relationship(back_populates='projects')
    salesengineer_id:Mapped[int] = mapped_column(ForeignKey('salesengineers.id'),nullable=False)
    salesengineer:Mapped['SalesEngineer'] = relationship(back_populates='projects')
    dwgtitles:Mapped[List['DwgTitle']] = relationship(back_populates='project', cascade="all, delete-orphan")
    systems:Mapped[List['System']] = relationship(back_populates='project', cascade="all, delete-orphan")

class System(Base):
    __tablename__ = 'systems'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    project: Mapped['Project'] = relationship(back_populates='systems')
    diagrams: Mapped[list['Diagram']] = relationship(back_populates='system', cascade="all, delete-orphan")
    devices: Mapped[list['SystemDevice']] = relationship('SystemDevice', back_populates='system', cascade="all, delete-orphan")

class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    systems: Mapped[list['SystemDevice']] = relationship('SystemDevice', back_populates='device')

class SystemDevice(Base):
    __tablename__ = 'systemdevices'
    id: Mapped[int] = mapped_column(primary_key=True)
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'), primary_key=False)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id'), primary_key=False)
    tag:Mapped[str] = mapped_column(nullable=True)    
    qty:Mapped[int] = mapped_column(nullable=True)  
    system: Mapped['System'] = relationship('System', back_populates='devices')
    device: Mapped['Device'] = relationship('Device', back_populates='systems')

class Diagram(Base):
    __tablename__ = 'diagrams'
    id:Mapped[int] = mapped_column(primary_key=True)
    type:Mapped[str] = mapped_column(nullable=True)    
    system_id:Mapped[int] = mapped_column(ForeignKey('systems.id'),nullable=False)
    system:Mapped['System'] = relationship(back_populates='diagrams')
    dwgtitle_id:Mapped[int] = mapped_column(ForeignKey('dwgtitles.id'),nullable=False)
    dwgtitle:Mapped['DwgTitle'] = relationship(back_populates='diagrams')

class DwgTitle(Base):
    __tablename__ = 'dwgtitles'
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=True)
    dwgno:Mapped[int] = mapped_column(nullable=False)
    project_id:Mapped[int] = mapped_column(ForeignKey('projects.id'),nullable=False)
    project:Mapped['Project'] = relationship(back_populates='dwgtitles')
    diagrams:Mapped[List['Diagram']] = relationship(back_populates='dwgtitle')

class Client(Base):
    __tablename__ = 'clients'
    id:Mapped[int] = mapped_column(primary_key=True)
    client_name:Mapped[str] = mapped_column(nullable=False)
    scope:Mapped[str] = mapped_column(nullable=False)
    address:Mapped[str] = mapped_column(nullable=False)
    city:Mapped[str] = mapped_column(nullable=False)
    state:Mapped[str] = mapped_column(nullable=False)
    zip_code:Mapped[int] = mapped_column(nullable=False)    
    projects:Mapped[List['Project']] = relationship(back_populates='client')

class ProjectManager(Base):
    __tablename__ = 'projectmanagers'
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(nullable=False)
    projects:Mapped[List['Project']] = relationship(back_populates='projectmanager')

class MechanicalEngineer(Base):
    __tablename__ = 'mechanicalengineers'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)    
    address:Mapped[str] = mapped_column(nullable=False)
    city:Mapped[str] = mapped_column(nullable=False)
    state:Mapped[str] = mapped_column(nullable=False)
    zip_code:Mapped[int] = mapped_column(nullable=False)    
    projects:Mapped[List['Project']] = relationship(back_populates='mechanicalengineer')

class MechanicalContractor(Base):
    __tablename__ = 'mechanicalcontractors'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)    
    address:Mapped[str] = mapped_column(nullable=False)
    city:Mapped[str] = mapped_column(nullable=False)
    state:Mapped[str] = mapped_column(nullable=False)
    zip_code:Mapped[int] = mapped_column(nullable=False)    
    telephone:Mapped[str] = mapped_column(nullable=False)    
    projects:Mapped[List['Project']] = relationship(back_populates='mechanicalcontractor')

class DesignEngineer(Base):
    __tablename__ = 'designengineers'
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(nullable=False)
    projects:Mapped[List['Project']] = relationship(back_populates='designengineer')

class SalesEngineer(Base):
    __tablename__ = 'salesengineers'
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(nullable=False)
    projects:Mapped[List['Project']] = relationship(back_populates='salesengineer')

def _db_exist():
    if os.path.exists('workflow.db'):
        return True
    else:
        return False

exist_db = _db_exist()
DATABASE_URL = 'sqlite:///workflow.db'
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session() 

# Check if the database exists
if not exist_db:    
    Base.metadata.create_all(engine)
    # Load data from JSON file
    with open('database_seed.json') as f:
        data = json.load(f)
        
    # Seed the database
    for client_data in data['clients']:
        client = Client(**client_data)
        session.add(client)
    
    for pm_data in data['projectmanagers']:
        project_manager = ProjectManager(**pm_data)
        session.add(project_manager)

    for me_data in data['mechanicalengineers']:
        mechanical_engineer = MechanicalEngineer(**me_data)
        session.add(mechanical_engineer)
        
    for mc_data in data['mechanicalcontractors']:
        mechanical_contractor = MechanicalContractor(**mc_data)
        session.add(mechanical_contractor)
        
    for de_data in data['designengineers']:
        design_engineer = DesignEngineer(**de_data)
        session.add(design_engineer)
        
    for se_data in data['salesengineers']:
        sales_engineer = SalesEngineer(**se_data)
        session.add(sales_engineer)

    for project_data in data['projects']:
        project = Project(**project_data)
        session.add(project)

    for dwgtitle_data in data['dwgtitles']:
        dwgtitle = DwgTitle(**dwgtitle_data)
        session.add(dwgtitle)
    
    for system_data in data['systems']:
        system = System(**system_data)
        session.add(system)

    for systemdevice_data in data['systemdevices']:
        systemdevice = SystemDevice(**systemdevice_data)
        session.add(systemdevice)

    for device_data in data['devices']:
        device = Device(**device_data)
        session.add(device)
    
    for diagram_data in data['diagrams']:
        diagram = Diagram(**diagram_data)
        session.add(diagram)

    session.commit()