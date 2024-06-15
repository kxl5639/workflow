from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the field metadata
## default - what appears when a new add window is opened
## frame - determines which frame or column the data will show up in on the add/modify window
## display - determines which field will appear on the main mech_eng window ie: don't need to show the specifics of the address in that main mech_eng window.
## entry_method - determines how the user wil enter the data. 'manual', via 'dropdown', or via a 'lookup' that will spawn in new window
## table_ref - references the table in the database where the data comes from
field_metadata = {
    "mechanical_engineer": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "address": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "city": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "state": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "zip_code": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1}
}

# Dynamically create the MechEng class
class MechEng(Base):
    __tablename__ = 'tblMechEng'
    id = Column(Integer, primary_key=True, autoincrement=True)
    for field, meta in field_metadata.items():
        vars()[field] = meta["type"]

DATABASE_URL = 'sqlite:///workflows.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
