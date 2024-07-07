from model import session, Project, System, SystemDevice

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

    def get_target_col_val_by_known_col_val(self, model, known_col, known_val, target_col):
        known_col_attr = getattr(model, known_col)        
        record_obj = session.query(model).filter(known_col_attr==known_val).first()        
        target_val = getattr(record_obj, target_col)
        return target_val
    
    def add_record(self, record_obj):
        session.add(record_obj)

    def commit_changes(self):
        session.commit()