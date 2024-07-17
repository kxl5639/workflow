from class_collection import ListWindow, Controller, Model
from model import Device, SystemDevice

class DeviceListBaseController(Controller):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.model = DeviceListBaseModel(self)
        self.column_map = self.model.column_map
        self.table_data = self.model.table_data
        self.button_info = None

    @classmethod
    def get_devices_data(cls, controller, systems_keys):

        def get_devices_data_without_length(system_key, systems_devices_data_dict):
            system_id = system_key[0]
            systemdevices_ids_list_of_dicts = controller.model.get_vals_from_rec_objs(SystemDevice, ['id'], {'system_id':system_id})
            systemdevices_ids = [systemdevices_ids_dict['id'] for systemdevices_ids_dict in systemdevices_ids_list_of_dicts]
            devices_ids, devices_qtys, devices_tags, devices_dwgs, devices_descs, devices_manufs, devices_models, = [], [], [], [], [], [], []
            for systemdevices_id in systemdevices_ids:
                devices_ids.append(controller.model.get_vals_from_rec_objs(SystemDevice, ['device_id'], {'id':systemdevices_id})[0]['device_id'])
                devices_qtys.append(controller.model.get_vals_from_rec_objs(SystemDevice, ['qty'], {'id': systemdevices_id})[0]['qty'])
                devices_tags.append(controller.model.get_vals_from_rec_objs(SystemDevice, ['tag'], {'id': systemdevices_id})[0]['tag'])
                devices_dwgs.append(controller.model.get_vals_from_rec_objs(SystemDevice, ['dwgtitle_id'], {'id': systemdevices_id})[0]['dwgtitle_id'])
            for devices_id in devices_ids:
                devices_descs.append(controller.model.get_vals_from_rec_objs(Device, ['description'], {'id':devices_id})[0]['description'])
                devices_manufs.append(controller.model.get_vals_from_rec_objs(Device, ['manufacturer'], {'id':devices_id})[0]['manufacturer'])
                devices_models.append(controller.model.get_vals_from_rec_objs(Device, ['model'], {'id':devices_id})[0]['model'])
            systems_devices_data_dict[system_key] = {'devices_tags' : {'data':devices_tags, 'max_char':0},
                                                        'devices_qtys' : {'data':devices_qtys, 'max_char':0},
                                                        'devices_dwgs' : {'data':devices_dwgs, 'max_char':0},
                                                        'devices_descs' : {'data':devices_descs, 'max_char':0},
                                                        'devices_manufs' : {'data':devices_manufs, 'max_char':0},
                                                        'devices_models' : {'data':devices_models, 'max_char':0}}
            
            return systems_devices_data_dict

        def get_max_devices_data_char(system_key, systems_devices_data_dict, max_device_data_char_dict):
            for cat in systems_devices_data_dict[system_key].keys():
                if cat not in max_device_data_char_dict:
                    # Establish a minimum character width and CAN  overwritten
                    if cat == 'devices_models':
                        max_device_data_char_dict[cat] = len('model')
                    elif cat == 'devices_descs':
                        max_device_data_char_dict[cat] = len('description')
                    elif cat == 'devices_manufs':
                        max_device_data_char_dict[cat] = len('manufacturer')
                    else:
                        max_device_data_char_dict[cat] = 0
                for next in systems_devices_data_dict[system_key][cat]['data']:
                    # Establishes a minimum character width and CANNOT be overwritten
                    if cat == 'devices_tags':
                        max_device_data_char_dict[cat] = 7
                    elif cat == 'devices_qtys':
                        max_device_data_char_dict[cat] = 5
                    elif cat == 'devices_dwgs':
                        max_device_data_char_dict[cat] = 4
                    else:
                        if len(next) > max_device_data_char_dict[cat]:
                            max_device_data_char_dict[cat] = len(next)

            return max_device_data_char_dict
        
        def update_max_char_in_systems_devices_data_dict(system_key, systems_devices_data_dict, max_device_data_char_dict):
            # Update max char for each systems_devices_data_dict
            for device_prop_key in systems_devices_data_dict[system_key]:
                systems_devices_data_dict[system_key][device_prop_key]['max_char']=max_device_data_char_dict[device_prop_key]

            return systems_devices_data_dict
        
        systems_devices_data_dict = {}
        max_device_data_char_dict = {}
        for system_key in systems_keys:
            systems_devices_data_dict = get_devices_data_without_length(system_key, systems_devices_data_dict)
            max_device_data_char_dict = get_max_devices_data_char(system_key, systems_devices_data_dict, max_device_data_char_dict)
            systems_devices_data_dict = update_max_char_in_systems_devices_data_dict(system_key, systems_devices_data_dict, max_device_data_char_dict)
        number_of_systems = len(systems_devices_data_dict)

        return systems_devices_data_dict, max_device_data_char_dict, number_of_systems

class DeviceListBaseView(ListWindow):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.button_frame = None

########### Frame Structure ###########
#                                     #
#  system_base_frame [ -> tree_frame  #
#                                     #
#######################################


class DeviceListBaseModel(Model):
    def __init__(self, controller=None) -> None:
        super().__init__(controller)
        self.column_map = {"name": 1,
                    "description": 2,
                    "manufacturer": 3,
                    "model": 4
                    }
        self.table_data = self.get_table_data()
        
    def get_table_data(self):
        data_table_list = []
        device_cols_val = self.get_vals_from_rec_objs(Device, ['id','name', 'description', 'manufacturer', 'model'])
        for each_list in device_cols_val:
            invididual_device_tuple = ()
            for val in each_list.values():
                invididual_device_tuple = invididual_device_tuple + (val,)
            data_table_list.append(invididual_device_tuple)
        return data_table_list
