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
    
DATABASE_URL = 'sqlite:///workflow.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session() 