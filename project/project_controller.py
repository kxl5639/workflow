from datetime import datetime
from project.project_model import session, Project, field_metadata
from project.project_utils import fetch_projects

def add_project(entries):
    submittal_date_str = entries["submittal_date"].get()

    # Try to parse the date if it is not a placeholder
    if submittal_date_str != "XX/XX/XX":
        try:
            submittal_date = datetime.strptime(submittal_date_str, '%m/%d/%y').date()
            submittal_date_str = submittal_date.isoformat()
        except ValueError:
            return "Invalid Date Format. Please enter the date in MM/DD/YY format."

    project_data = {}
    for field, metadata in field_metadata.items():
        if field == "submittal_date":
            project_data[field] = submittal_date_str
        else:
            project_data[field] = entries[field].get()

    new_project = Project(**project_data)
    session.add(new_project)
    session.commit()
    return None  # Indicate success
