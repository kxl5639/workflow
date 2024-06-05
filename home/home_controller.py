from home.home_view import create_home_window
from project.project_view import create_project_window

def projects_button_clicked():
    # This function will be executed when the "Projects" button is clicked
    create_project_window()

def design_engineers_button_clicked():
    # This function will be executed when the "Design Engineers" button is clicked
    messagebox.showinfo("Design Engineers Button", "Design Engineers button clicked!")

def main():
    create_home_window(controller={
        'projects_button_clicked': projects_button_clicked,
        'design_engineers_button_clicked': design_engineers_button_clicked
    })
