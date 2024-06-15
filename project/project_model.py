from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Define the field metadata
## default - what appears when a new add window is opened
## frame - determines which frame or column the data will show up in on the add/modify window
## display - determines which field will appear on the main project window ie: don't need to show the specifics of the address in that main project window.
## entry_method - determines how the user wil enter the data. Manually, via dropdown, or via a lookup that will spawn in new window
## table_ref - references the table in the database where the data comes from
field_metadata = {
    "project_number": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1, "entry_method":"manual"},
    "em_type": {"type": Column(String(50)), "default": "B", "frame": 1, "display": 0, "entry_method":"manual"},
    "job_phase": {"type": Column(String(50)), "default": "1", "frame": 1, "display": 0, "entry_method":"manual"},
    "submittal_date": {"type": Column(String), "default": "XX/XX/XX", "frame": 1, "display": 1, "entry_method":"manual"},
    "client": {"type": Column(String(100)), "default": "", "frame": 2, "display": 1, "entry_method":"manual",'relationship':['Client','tblProject']},
    "scope": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "address": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "city": {"type": Column(String(100)), "default": "New York", "frame": 2, "display": 0, "entry_method":"manual"},
    "state": {"type": Column(String(50)), "default": "NY", "frame": 2, "display": 0, "entry_method":"manual"},
    "zip_code": {"type": Column(String(20)), "default": "10001", "frame": 2, "display": 0, "entry_method":"manual"},
    "project_manager": {"type": Column(String(100)), "default": "", "frame": 1, "display": 1, "entry_method":"dropdown", "table_ref":"ProjectManager"},
    "mechanical_engineer": {"type": Column(String(100)), "default": "", "frame": 3, "display": 1, "entry_method":"lookup", "table_ref":"MechEng"},
    "me_address": {"type": Column(String(250)), "default": "", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_city": {"type": Column(String(100)), "default": "New York", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_state": {"type": Column(String(50)), "default": "NY", "frame": 3, "display": 0, "entry_method":"manual"},
    "me_zip_code": {"type": Column(String(20)), "default": "10001", "frame": 3, "display": 0, "entry_method":"manual"},
    "mechanical_contractor": {"type": Column(String(100)), "default": "", "frame": 4, "display": 1, "entry_method":"lookup", "table_ref":"MechCon"},
    "mc_address": {"type": Column(String(250)), "default": "", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_city": {"type": Column(String(100)), "default": "New York", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_state": {"type": Column(String(50)), "default": "NY", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_zip_code": {"type": Column(String(20)), "default": "10000", "frame": 4, "display": 0, "entry_method":"manual"},
    "mc_phone_number": {"type": Column(String(20)), "default": "10000", "frame": 4, "display": 0, "entry_method":"manual"},
    "design_engineer": {"type": Column(String(100)), "default": "Kevin Lee", "frame": 1, "display": 1, "entry_method":"dropdown", "table_ref":"DesignEng"},
    "sales_engineer": {"type": Column(String(100)), "default": "", "frame": 1, "display": 1, "entry_method":"dropdown", "table_ref":"SalesEng"}
    
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
