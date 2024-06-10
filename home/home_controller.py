from home.home_view import create_home_window #type:ignore
from project.project_view import create_project_window #type:ignore
from design_eng.design_eng_view import create_design_eng_window #type:ignore
from sales_eng.sales_eng_view import create_sales_eng_window #type:ignore
from project_manager.project_manager_view import create_project_manager_window #type:ignore

def projects_button_clicked():    
    create_project_window()

def design_engineers_button_clicked():
    create_design_eng_window()

def sales_engineers_button_clicked():
    create_sales_eng_window()

def project_managers_button_clicked():
    create_project_manager_window()

def main():
    create_home_window(controller={
        'projects_button_clicked': projects_button_clicked,
        'design_engineers_button_clicked': design_engineers_button_clicked,
        'sales_engineers_button_clicked': sales_engineers_button_clicked,
        'project_managers_button_clicked': project_managers_button_clicked
    })
