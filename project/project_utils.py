from project.project_model import session, Project


def project_columns_to_display(): #THIS INDICATES WHAT COLUMNS I WANT TO SHOW IN THE PROJECTS WINDOW
    return (
        "project_number", "client", "scope", "address",
        "project_manager", "design_engineer", "sales_engineer", "submittal_date",
        "mechanical_engineer", "mechanical_contractor"
    )

def fetch_projects():
    return session.query(Project).all()

def populate_treeview_with_projects(tree):
    # Define the columns
    columns = project_columns_to_display()

    # Clear existing items in tree
    for item in tree.get_children():
        tree.delete(item)

    # Fetch projects
    projects = fetch_projects()
    
    # Insert projects into the treeview
    for project in projects:
        values = tuple(getattr(project, col) for col in columns)
        tree.insert('', 'end', values=values)




