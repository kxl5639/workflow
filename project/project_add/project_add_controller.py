from project.project_model import field_metadata
from configs import testing

#This function determines the default data when "Add New Project" window is opened.
def default_entry_data():
    default_entry_data = {}
    if testing:
        for field in field_metadata.keys():
            if field == "submittal_date":
                default_entry_data[field] = "XX/XX/XX"
            elif field == "design_engineer":
                default_entry_data[field] = "Kevin Lee"
            else:
                default_entry_data[field] = "TESTING"
    else:
        for field in field_metadata.keys():
            default_entry_data[field] = field_metadata[field]["default"]
    return default_entry_data