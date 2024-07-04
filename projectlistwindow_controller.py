from projectlistwindow_model import ProjectListWindowModel
from projectlistwindow_view import ProjectAddModifyWindow
from model import session, ProjectManager, DesignEngineer, SalesEngineer, Client, MechanicalContractor, MechanicalEngineer, Project
from view import ListWindow

class ProjectListWindowController:
    def __init__(self, parent=None) -> None:
        self.parent = parent        
        self.model = ProjectListWindowModel()
        self.column_map = self.model.colump_map
        self.table_data = self.model.table_data
        self.button_info = [("Add", lambda: self.add_button_command()),
                    ("Modify", lambda: self.modify_button_command()),
                    ("Delete", None)]        
        # self.button_info = [("Add", lambda: open_add_project_window(self.parent)),
        #                     ("Modify", lambda: open_modify_project_window(self.parent)),
        #                     ("Delete", lambda: open_delete_project_window(self.parent))]        
        self.view = ListWindow(title = 'Projects List', parent=self.parent, controller=self)

    def add_button_command(self):
        self.add_window = ProjectAddModifyWindow(title='Add New Project', parent=self.view, controller=self)

    def modify_button_command(self):
        self.modify_window = ProjectAddModifyWindow(title='Modify Project', parent=self.view, controller=self,is_modify=True)

    def get_combobox_options(self):        
        model_list = [ProjectManager, DesignEngineer, SalesEngineer]
        results = {model.__tablename__: [f"{instance.first_name} {instance.last_name}" for instance in session.query(model).order_by(model.first_name).all()] for model in model_list}        
        return results
    
    def fetch_record_data(self):
        tree_selection = self.view.tree_frame.tree.selection()        
        selected_record_iid = tree_selection[0] # The item identifier (iid) is the project ID        
        # selected_record_obj = session.query(Project).get(selected_record_iid)
        project = session.query(Project).filter_by(id=selected_record_iid).first()
        client = session.query(Client).filter_by(id=project.client_id).first()
        pm = session.query(ProjectManager).filter_by(id=project.projectmanager_id).first()
        me = session.query(MechanicalEngineer).filter_by(id=project.mechanicalengineer_id).first()
        mc = session.query(MechanicalContractor).filter_by(id=project.mechanicalcontractor_id).first()
        de = session.query(DesignEngineer).filter_by(id=project.designengineer_id).first()
        se = session.query(SalesEngineer).filter_by(id=project.salesengineer_id).first()
        return {'project':project, 'client':client, 'pm':pm, 'me':me, 'mc':mc, 'de':de, 'se':se}
        
        


        
        
        