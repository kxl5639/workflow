from model import session, Project, System

class ProjectDetailModel:
    def __init__(self, controller, project_number) -> None:
        self.controller = controller
        self.project_number = project_number
    
    def get_id_from_model_column_data(self, model, col_name, col_val):
        col_attr = getattr(model, col_name)
        return session.query(model).filter(col_attr == col_val).first().id

    def get_objs_from_column_data(self, model, col_name, col_val):
        col_attr = getattr(model, col_name)
        return session.query(model).filter(col_attr == col_val).all()
        