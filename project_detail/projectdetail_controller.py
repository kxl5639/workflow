from project_detail.projectdetail_view import ProjectDetailWindow
from project_detail.projectdetailchild_view import AddDeviceWinow
from project_detail.projectdetail_model import ProjectDetailModel
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
            # AddDeviceController(self.parent, self.project_number)
            pass
        
#####################################################################################    
    
    def add_new_device(self):
        self.add_device_controller = AddDeviceController(self.parent, self.project_number)
    
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
        
        def get_max_devices_data_char(systems_devices_data_dict, system_key):        
            for cat in systems_devices_data_dict[system_key].keys():
                if cat not in self.max_device_data_char_dict:
                    # This is here to establish a minimum character width and CAN  overwritten
                    if cat == 'devices_models':
                        self.max_device_data_char_dict[cat] = len('model')
                    elif cat == 'devices_descs':
                        self.max_device_data_char_dict[cat] = len('description')
                    elif cat == 'devices_manufs':
                        self.max_device_data_char_dict[cat] = len('manufacturer')
                    else:
                        self.max_device_data_char_dict[cat] = 0
                for next in systems_devices_data_dict[system_key][cat]['data']:
                    # This is here to establish a minimum character width and CANNOT be overwritten
                    if cat == 'devices_tags':
                        self.max_device_data_char_dict[cat] = 7
                    elif cat == 'devices_qtys':
                        self.max_device_data_char_dict[cat] = 5
                    elif cat == 'devices_dwgs':
                        self.max_device_data_char_dict[cat] = 4
                    else:
                        if len(next) > self.max_device_data_char_dict[cat]:
                            self.max_device_data_char_dict[cat] = len(next)

        def get_devices_data(system_key):
                system_id = system_key[0]
                systemdevices_ids = self.get_child_ids_list(SystemDevice, system_id, 'system_id')
                devices_ids = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'device_id')
                devices_tags = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'tag')
                devices_qtys = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'qty')
                devices_dwgs = self.get_target_col_vals_list_by_known_col_val(SystemDevice,'id', systemdevices_ids, 'dwgtitle_id')
                devices_descs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'description')
                devices_manufs = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'manufacturer')
                devices_models = self.get_target_col_vals_list_by_known_col_val(Device,'id',devices_ids,'model')
                self.systems_devices_data_dict[system_key] = {'devices_tags' : {'data':devices_tags, 'max_char':0},
                                                            'devices_qtys' : {'data':devices_qtys, 'max_char':0},
                                                            'devices_dwgs' : {'data':devices_dwgs, 'max_char':0},
                                                            'devices_descs' : {'data':devices_descs, 'max_char':0},
                                                            'devices_manufs' : {'data':devices_manufs, 'max_char':0},
                                                            'devices_models' : {'data':devices_models, 'max_char':0}}
        
        # Clear self.systems_devices_data_dict and self.number_of_systems
        self.systems_devices_data_dict = {}
        self.number_of_systems = None
        # Gets all systems keys of the project number
        systems_keys = get_systems_keys()
        # Gets all the device data (tag, desc, manf, etc...) for each system_key
            # Also gets the max character length for each device data
        for system_key in systems_keys:
            get_devices_data(system_key)
            get_max_devices_data_char(self.systems_devices_data_dict, system_key)
        # Update max char for each systems_devices_data_dict
        for system_key in systems_keys:
            # system_id = system_key[0]
            for device_prop_key in self.systems_devices_data_dict[system_key]:
                self.systems_devices_data_dict[system_key][device_prop_key]['max_char']=self.max_device_data_char_dict[device_prop_key]
        # Update number of systems as well
        self.number_of_systems = len(self.systems_devices_data_dict)
        return self.systems_devices_data_dict, self.number_of_systems

    def get_target_col_vals_list_by_known_col_val(self, model, known_col, known_vals, target_col):
        '''
        Gets target attribute value from the same table if a attribute value in that record is known
        '''
        target_attributes = []
        for known_val in known_vals:
            target_attr = self.model.get_target_col_val_by_known_col_val(model,known_col, known_val, target_col)
            target_attributes.append(target_attr)
        return target_attributes
    
    def get_child_names_list(self, child_model, parent_id, child_col_of_parent_id):
        '''
        Gets names list of child objects, given that parent_id column exists in child table.

        For example, we can retrieve a list of all system names of associated project_id.

        child_col_of_parent_id is column name in child table that refers to parent_id.
        '''
        child_objs = self.model.get_rec_objs_by_opt_filts(child_model, {child_col_of_parent_id: parent_id})
        childs_names = []        
        for child_obj in child_objs:
            childs_names.append(child_obj.name)            
        return childs_names

    def get_child_ids_list(self, child_model, parent_id, child_col_of_parent_id):
        '''
        Gets ids list of child objects, given that parent_id column exists in child table.

        For example, we can retrieve a list of all system ids of associated project_id.

        child_col_of_parent_id is column name in child table that refers to parent_id.
        '''
        child_objs = self.model.get_rec_objs_by_opt_filts(child_model, {child_col_of_parent_id: parent_id})
        childs_ids = []
        for child_obj in child_objs:
            childs_ids.append(child_obj.id)
        return childs_ids
    
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

    def open_title_manager(self):
        TitleController(self.view, self.project_number)

class AddDeviceController(DeviceListBaseController):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.view = AddDeviceWinow('Add Device', self.parent, self)