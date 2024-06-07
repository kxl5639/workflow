from home.home_view import create_home_window
from project.project_view import create_project_window
from project.design_eng_view import create_design_eng_window

def projects_button_clicked():    
    create_project_window()

def design_engineers_button_clicked():
    create_design_eng_window()

def main():
    create_home_window(controller={
        'projects_button_clicked': projects_button_clicked,
        'design_engineers_button_clicked': design_engineers_button_clicked
    })
