from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# # Define the base class
# Base = declarative_base()

# # Define the User class (table)

# project_field_metadata = {
#     "project_number": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1, "entry_method":"manual"},
#     "em_type": {"type": Column(String(50)), "default": "B", "frame": 1, "display": 0, "entry_method":"manual"},
#     "job_phase": {"type": Column(String(50)), "default": "1", "frame": 1, "display": 0, "entry_method":"manual"},
#     "submittal_date": {"type": Column(String), "default": "XX/XX/XX", "frame": 1, "display": 1, "entry_method":"manual"},
#     "client": {"type": Column(String(100)), "default": "", "frame": 2, "display": 1, "entry_method":"manual",'relationship':['Client','tblProject']},
#     "scope": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
#     "address": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
#     "city": {"type": Column(String(100)), "default": "New York", "frame": 2, "display": 0, "entry_method":"manual"},
#     "state": {"type": Column(String(50)), "default": "NY", "frame": 2, "display": 0, "entry_method":"manual"},
#     "zip_code": {"type": Column(String(20)), "default": "10001", "frame": 2, "display": 0, "entry_method":"manual"},}



# class Project(Base):
#     __tablename__ = 'tblProject'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     for field, meta in project_field_metadata.items():
#         vars()[field] = meta["type"]


# client_field_metadata = {
#     "client": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
#     "scope": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
#     "address": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
#     "city": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
#     "state": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1},
#     "zip_code": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1}
# }


# # Dynamically create the Client class
# class Client(Base):
#     __tablename__ = 'tblClient'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     for field, meta in client_field_metadata.items():
#         vars()[field] = meta["type"]

# DATABASE_URL = 'sqlite:///test.db'
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()



Base = declarative_base()

project_field_metadata = {
    "project_number": {"type": Column(String(50)), "default": "", "frame": 1, "display": 1, "entry_method":"manual"},
    "em_type": {"type": Column(String(50)), "default": "B", "frame": 1, "display": 0, "entry_method":"manual"},
    "job_phase": {"type": Column(String(50)), "default": "1", "frame": 1, "display": 0, "entry_method":"manual"},
    "submittal_date": {"type": Column(String), "default": "XX/XX/XX", "frame": 1, "display": 1, "entry_method":"manual"},
    "client": {"type": Column(String(100)), "default": "", "frame": 2, "display": 1, "entry_method":"manual",'relationship':['Client','tblProject']},
    "scope": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "address": {"type": Column(String(250)), "default": "", "frame": 2, "display": 1, "entry_method":"manual"},
    "city": {"type": Column(String(100)), "default": "New York", "frame": 2, "display": 0, "entry_method":"manual"},
    "state": {"type": Column(String(50)), "default": "NY", "frame": 2, "display": 0, "entry_method":"manual"},
    "zip_code": {"type": Column(String(20)), "default": "10001", "frame": 2, "display": 0, "entry_method":"manual"},}

# Dynamically create the Client class
class Client(Base):
    __tablename__ = 'tblClient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    for field, meta in project_field_metadata.items():
        vars()[field] = meta["type"]
        print(field)