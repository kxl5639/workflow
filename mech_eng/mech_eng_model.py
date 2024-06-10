from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the field metadata
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
