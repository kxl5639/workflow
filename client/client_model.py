from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Define the field metadata
## default - what appears when a new add window is opened
## frame - determines which frame or column the data will show up in on the add/modify window
## display - determines which field will appear on the main client window ie: don't need to show the specifics of the address in that main client window.
## entry_method - determines how the user wil enter the data. 'manual', via 'dropdown', or via a 'lookup' that will spawn in new window
## table_ref - references the table in the database where the data comes from
field_metadata = {
    "client": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "scope": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "address": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "city": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "state": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
    "zip_code": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1}
}

# Dynamically create the Client class
class Client(Base):
    __tablename__ = 'tblClient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    for field, meta in field_metadata.items():
        vars()[field] = meta["type"]

DATABASE_URL = 'sqlite:///workflows.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
