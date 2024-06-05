from project.project_model import session, Project, field_metadata

def project_columns_to_display():
    # Extract columns with display value set to 1
    return [field for field, meta in field_metadata.items() if meta['display'] == 1]

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
