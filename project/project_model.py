from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the field metadata
field_metadata = {
    "project_number": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1, "entry_method":"manual"},
    "em_type": {"type": Column(String(50)), "default": "B", "frame": 1, "display": 0, "entry_method":"manual"},
    "job_phase": {"type": Column(String(50)), "default": "1", "frame": 1, "display": 0, "entry_method":"manual"},
    "submittal_date": {"type": Column(String), "default": "XX/XX/XX", "frame": 1, "display": 1, "entry_method":"manual"},
    "client": {"type": Column(String(100)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "scope": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "address": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "city": {"type": Column(String(100)), "default": "New York", "frame": 2, "display": 0, "entry_method":"manual"},
    "state": {"type": Column(String(50)), "default": "NY", "frame": 2, "display": 0, "entry_method":"manual"},
    "zip_code": {"type": Column(String(20)), "default": "10001", "frame": 2, "display": 0, "entry_method":"manual"},
    "project_manager": {"type": Column(String(100)), "default": "", "frame": 1, "display": 1, "entry_method":"dropdown"},
    "mechanical_engineer": {"type": Column(String(100)), "default": "", "frame": 3, "display": 1, "entry_method":"lookup"},
    "me_address": {"type": Column(String(250)), "default": "", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_city": {"type": Column(String(100)), "default": "New York", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_state": {"type": Column(String(50)), "default": "NY", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_zip_code": {"type": Column(String(20)), "default": "10001", "frame": 3, "display": 0, "entry_method":"manual"},
    "mechanical_contractor": {"type": Column(String(100)), "default": "", "frame": 4, "display": 1, "entry_method":"lookup"},
    "mc_address": {"type": Column(String(250)), "default": "", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_city": {"type": Column(String(100)), "default": "New York", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_state": {"type": Column(String(50)), "default": "NY", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_zip_code": {"type": Column(String(20)), "default": "10000", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_phone_number": {"type": Column(String(20)), "default": "10000", "frame": 4, "display": 0, "entry_method":"manual"},
    "design_engineer": {"type": Column(String(100)), "default": "Kevin Lee", "frame": 1, "display": 1, "entry_method":"dropdown"},
    "sales_engineer": {"type": Column(String(100)), "default": "", "frame": 1, "display": 1, "entry_method":"dropdown"}
    
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
