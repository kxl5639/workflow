from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetailchild_view import AddDeviceWindow
from project_detail.projectdetail_model import ProjectDetailModel
from project_detail.projectdetailchild_view import AddSystemWindow
from devicemanager import DeviceListBaseController
from model import session, Project, SystemDevice, System, Device, DwgTitle, DwgTitleDiagram
from class_collection import Controller
from title.title_controller import TitleController
from configs import testing

class ProjectDetailController(Controller):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.max_device_data_char_dict = {}
        self.systems_devices_data_dict = {}
        self.number_of_systems = None
        self.model = ProjectDetailModel(self.project_number, self)
        self.project_id = self.model.get_id_from_model_column_data(Project, 'project_number', self.project_number)
        self.view = ProjectDetailWindow(f'{self.project_number} Project Detail',
                                        self.parent, self, self.project_number)
        
        if testing == 1:
            # ProjectDetailWindow(f'{self.project_number} Project Detail',
            #                             self.parent, self, self.project_number)
            self.add_new_device((2, 'AHU'))
            pass
        
#####################################################################################    
    
    def get_systems_devices_data(self):
        def get_systems_keys():
            '''Generates the key as a tuple [ex: (1, 'AHU')] for self.systems_devices_data_dict.'''
            def get_systems_ids_from_proj_num():
                systems_objs = self.model.get_rec_objs_by_opt_filts(System, {'project_id': self.project_id})
                systems_ids = []
                for system_obj in systems_objs:
                    if system_obj.name != '(None)':
                        systems_ids.append(system_obj.id)
                return systems_ids
            
            systems_ids = get_systems_ids_from_proj_num()
            systems_keys = []
            for idx, system_id in enumerate(systems_ids):
                system_obj = self.model.get_rec_objs_by_opt_filts(System, {'id':system_id})
                system_name = system_obj[0].name
                systems_keys.append((system_id, system_name))
            return systems_keys

        # Gets all systems keys of the project number
        systems_keys = get_systems_keys()

        # Clear self.systems_devices_data_dict and self.number_of_systems
        self.systems_devices_data_dict = {}
        self.number_of_systems = None

        systems_devices_data_dict = {}
        max_device_data_char_dict = {}
        for system_key in systems_keys:
            self.systems_devices_data_dict, self.max_device_data_char_dict, self.number_of_systems = DeviceListBaseController.get_devices_data(self, system_key, systems_devices_data_dict, max_device_data_char_dict)

        return self.systems_devices_data_dict, self.max_device_data_char_dict, self.number_of_systems
    
    #region Add new system window
    def add_new_system(self, entry_widget):
        def data_validation(new_system_name):
            if not new_system_name:
                error_msg = 'Please enter a system name to be added.'
                return error_msg
            return None
            
        def add_new_system_db(new_system_rec_obj) -> bool:
            if new_system_rec_obj:
                self.model.add_record(new_system_rec_obj)
                self.model.commit_changes()
                return True

        def get_new_system_rec_obj(new_system_name:str, proj_id:int):
            new_system_record = System(name=new_system_name, project_id=proj_id)
            return new_system_record

        # Declare necessary objects
        new_system_name: str = entry_widget.get()
        proj_id = self.model.get_id_from_model_column_data(Project,'project_number', self.project_number)
        new_system_rec_obj = get_new_system_rec_obj(new_system_name, proj_id)

        ##### Need to verify that the system name doesn't already exist
        error_msg = data_validation(new_system_name)
        if not error_msg:
            add_new_system_db(new_system_rec_obj)
            return None
        return error_msg
    #endregion

    #region Delete system
    def delete_system(self, system_name):
        def get_system_id(system_name):
            for system_key in self.systems_devices_data_dict.keys():
                if system_key[1] == system_name:
                    system_id = system_key[0]
                    return system_id

        def get_dwgtitle_id_from_dwgno(dwgno):
            dwgtitle_id = self.model.get_rec_objs_by_opt_filts(DwgTitle, 
                                                        {'project_id': self.project_id,
                                                            'dwgno': dwgno})
            return dwgtitle_id[0].id
            
        system_id : int = get_system_id(system_name)

        # Need to get all drawing numbers of the system and reproduce blank entries in the database
        # to prevent index errors when executing calc_col_row_for_pop_title_data_frame in TitleController
        dwgtitle_obj_list = self.model.get_rec_objs_by_opt_filts(DwgTitle, {'system_id': system_id})
        dwgno_list = []
        for dwgtitle_obj in dwgtitle_obj_list:
            dwgno_list.append(dwgtitle_obj.dwgno)

        # Deleting system object
        system_obj: System = self.model.get_rec_objs_by_opt_filts(System, {'id': system_id})[0]
        self.model.delete_record([system_obj])
        self.model.commit_changes()

        # Create dwgtitle objects to be added to DwgTitle after deleting the system
        replacement_dwgtitle_obj_list = []
        system_id = self.model.get_rec_objs_by_opt_filts(System, {'project_id': self.project_id,
                                                                'name': '(None)'})[0].id
        for dwgno in dwgno_list:
            replacement_dwgtitle_obj = DwgTitle(title = f'Filler for deleted [{system_name.upper()}] system',
                                                dwgno = dwgno,
                                                project_id = self.project_id,
                                                system_id = system_id)
            replacement_dwgtitle_obj_list.append(replacement_dwgtitle_obj)

        for replacement_dwgtitle_obj in replacement_dwgtitle_obj_list:
            self.model.add_record(replacement_dwgtitle_obj)

        # Also create diagram objects to be added to Diagram after deleting the system
        replacement_dwgtitlediagram_obj_list = []
        for dwgno in dwgno_list:
            dwgtitle_id = get_dwgtitle_id_from_dwgno(dwgno)
            replacement_dwgtitlediagram_obj = DwgTitleDiagram(dwgtitle_id = dwgtitle_id,
                                                              diagram_id = 1)
            replacement_dwgtitlediagram_obj_list.append(replacement_dwgtitlediagram_obj)

        for replacement_dwgtitlediagram_obj in replacement_dwgtitlediagram_obj_list:
            self.model.add_record(replacement_dwgtitlediagram_obj)

        self.model.commit_changes()
    #endregion

    def system_add_btn_cmd(self):
        self.add_system_window = AddSystemWindow('Add New System', self.parent, controller=self)

    def open_title_manager(self):
        TitleController(self.view, self.project_number)
    
    def add_new_device(self, system_key):
        self.add_device_controller = AddDeviceController(self, system_key, self.parent, self.project_number)

    def delete_device_btn_cmd(self, device_model):
        pass

class AddDeviceController(DeviceListBaseController):
    def __init__(self, controller, system_key, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.controller = controller
        self.system_key = system_key

        systems_devices_data_dict = {}
        max_device_data_char_dict = {}  
        self.systems_devices_data_dict, self.max_device_data_char_dict, _ = self.get_devices_data(self.controller,
                                                                                                  self.system_key,
                                                                                                  systems_devices_data_dict,
                                                                                                  max_device_data_char_dict)

        self.view = AddDeviceWindow('Add Device', self.parent, self)

