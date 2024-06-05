from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the field metadata
field_metadata = {
    "project_number": {"type": Column(String(50)), "default": "PN123", "frame": 1, "display": 1},
    "em_type": {"type": Column(String(50)), "default": "Type1", "frame": 1, "display": 0},
    "job_phase": {"type": Column(String(50)), "default": "Phase1", "frame": 1, "display": 0},
    "submittal_date": {"type": Column(String), "default": "XX/XX/XX", "frame": 1, "display": 1},
    "client": {"type": Column(String(100)), "default": "Client1", "frame": 2, "display": 1},
    "scope": {"type": Column(String(250)), "default": "Scope1", "frame": 2, "display": 1},
    "address": {"type": Column(String(250)), "default": "123 Main St", "frame": 2, "display": 1},
    "city": {"type": Column(String(100)), "default": "Anytown", "frame": 2, "display": 0},
    "state": {"type": Column(String(50)), "default": "CA", "frame": 2, "display": 0},
    "zip_code": {"type": Column(String(20)), "default": "90210", "frame": 2, "display": 0},
    "project_manager": {"type": Column(String(100)), "default": "Manager1", "frame": 1, "display": 1},
    "mechanical_engineer": {"type": Column(String(100)), "default": "Engineer1", "frame": 3, "display": 1},
    "me_address": {"type": Column(String(250)), "default": "456 Engineer St", "frame": 3, "display": 0},
    "me_city": {"type": Column(String(100)), "default": "Enginetown", "frame": 3, "display": 0},
    "me_state": {"type": Column(String(50)), "default": "CA", "frame": 3, "display": 0},
    "me_zip_code": {"type": Column(String(20)), "default": "90211", "frame": 3, "display": 0},
    "mechanical_contractor": {"type": Column(String(100)), "default": "Contractor1", "frame": 4, "display": 1},
    "mc_address": {"type": Column(String(250)), "default": "789 Contractor Ave", "frame": 4, "display": 0},
    "mc_city": {"type": Column(String(100)), "default": "Contractortown", "frame": 4, "display": 0},
    "mc_state": {"type": Column(String(50)), "default": "CA", "frame": 4, "display": 0},
    "mc_zip_code": {"type": Column(String(20)), "default": "90212", "frame": 4, "display": 0},
    "design_engineer": {"type": Column(String(100)), "default": "Designer1", "frame": 1, "display": 1},
    "sales_engineer": {"type": Column(String(100)), "default": "Sales1", "frame": 1, "display": 1}
}

# Dynamically create the Project class
class Project(Base):
    __tablename__ = 'tblProject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    for field, meta in field_metadata.items():
        vars()[field] = meta["type"]

DATABASE_URL = 'sqlite:///workflows.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
