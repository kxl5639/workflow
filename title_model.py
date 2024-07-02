from model import session, Project, DwgTitle

class TitleModel:

    def get_project_object(self, project_number):
        return session.query(Project).filter_by(project_number=project_number).first()
        
    def get_title_object(self, project_object):
        return session.query(DwgTitle).filter_by(project_id=project_object.id).order_by(DwgTitle.dwgno).all()            
