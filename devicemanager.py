import tkinter as tk
from tkinter import ttk
from class_collection import ListWindow, Controller, Model, ButtonsFrame
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
        # self.controller.column_map = {}
        # self.controller.table_data = {}

########### Frame Structure ###########
#                                     #
#  system_base_frame [ -> tree_frame  #
#                                     #
#######################################

    @classmethod
    def create_device_section(cls, parent, system_key, systems_devices_data_dict, max_device_data_char_dict):

        def create_device_base_frame(parent):
            device_base_frame = ttk.LabelFrame(parent, text='Devices')
            device_base_frame.grid(row=1,column=0,padx=0,pady=(5,0),sticky='nsew')
            device_base_frame.grid_columnconfigure(0, weight=1)
            return device_base_frame
      

        def create_data_frame(parent):
            device_data_frame = ttk.Frame(parent)
            device_data_frame.grid(row=0,column=0,padx=10,pady=(10,10),sticky='nsew')
            return device_data_frame

        def iter_generate_device_frame(parent, system_key, systems_devices_data_dict, max_device_data_char_dict): # parent is device_data_frame
            #region Functions
            def create_device_frame(parent, row_idx, system_key, systems_devices_data_dict):

                def create_device_tag_entry(parent, row_idx, system_key, dev_prop_key, systems_devices_data_dict):
                    device_tag_data = systems_devices_data_dict[system_key]['devices_tags']['data'][row_idx]
                    label_width = systems_devices_data_dict[system_key][dev_prop_key]['max_char']
                    def validate_input_length(P):
                        if len(P) > 7:  # Limit to 10 characters
                            return False
                        return True
                    vcmd = (parent.register(validate_input_length), '%P')
                    device_tag_entry = ttk.Entry(parent,width=label_width, validate='key', validatecommand=vcmd)
                    device_tag_entry.grid(row=row_idx+1,column=0)
                    device_tag_entry.delete(0, tk.END)
                    device_tag_entry.insert(0, device_tag_data)

                def create_device_label(parent, row_idx, system_key, dev_prop_key, col, systems_devices_data_dict):
                    device_data = systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
                    label_width = systems_devices_data_dict[system_key][dev_prop_key]['max_char'] + 2
                    device_label = ttk.Label(parent, text=f' {device_data}', relief='solid', width=label_width)
                    device_label.grid(row=row_idx+1,column=col, stick='nsew')
                
                def create_device_spinbox(parent, row_idx, system_key, dev_prop_key, col, systems_devices_data_dict):
                    device_data = systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
                    label_width = systems_devices_data_dict[system_key][dev_prop_key]['max_char'] 
                    device_spinbox = ttk.Spinbox(parent, from_=0, to=9999, width=label_width)
                    device_spinbox.set(device_data)
                    device_spinbox.grid(row=row_idx+1,column=col, sticky='nsew')
                
                def create_device_combobox(parent, row_idx, system_key, dev_prop_key, col, systems_devices_data_dict):
                    device_data = systems_devices_data_dict[system_key][dev_prop_key]['data'][row_idx]
                    label_width = systems_devices_data_dict[system_key][dev_prop_key]['max_char'] 
                    device_spinbox = ttk.Combobox(parent, width=label_width)
                    device_spinbox.set(device_data)
                    device_spinbox.grid(row=row_idx+1,column=col, sticky='nsew')

                create_device_tag_entry(parent, row_idx, system_key, 'devices_tags', systems_devices_data_dict)
                create_device_label(parent, row_idx, system_key, 'devices_descs', 1, systems_devices_data_dict)
                create_device_label(parent, row_idx, system_key, 'devices_manufs', 2, systems_devices_data_dict)
                create_device_label(parent, row_idx, system_key, 'devices_models', 3, systems_devices_data_dict)
                create_device_spinbox(parent, row_idx, system_key, 'devices_qtys', 4, systems_devices_data_dict)
                create_device_combobox(parent, row_idx, system_key, 'devices_dwgs', 5, systems_devices_data_dict)
                delete_device_button = ButtonsFrame(parent, [('Delete', None)])
                delete_device_button.button_frame.grid(row=row_idx+1, column=6, padx=(5,0))

            def create_device_header(parent, max_device_data_char_dict):
                def extract_model_from_string(input_string):
                    # Split the input string by underscore
                    parts = input_string.split('_')
                    # Check if the split result has at least two parts
                    if len(parts) >= 2:
                        # Get the last part of the split result
                        model = parts[-1]
                        # Remove the last character if it is 's'
                        if model.endswith('s'):
                            model = model[:-1]
                        return model
                header_list = ['Tag', 'Description', 'Manufacturer', 'Model', 'Qty', 'Dwg']
                # header_list = ['Tag', 'Description', 'Manufacturer', 'Model', 'Qty']
                width_dict = max_device_data_char_dict
                width_list = []
                for header in header_list:
                    for idx, key in enumerate(width_dict.keys()):
                        clean_key = extract_model_from_string(key).lower()
                        if clean_key in header.lower():
                            width_list.append(width_dict[key])
                for idx, header in enumerate(header_list):
                    label_tag = ttk.Label(parent, text=header, width=width_list[idx]-1, font=("Helvetica", 10, "bold"))
                    label_tag.grid(row=0,column=idx,sticky='nsew')
            #endregion

            manufs_list = systems_devices_data_dict[system_key]['devices_manufs']['data']
            if manufs_list:
                num_devices = len(manufs_list)
                create_device_header(parent, max_device_data_char_dict)
                for row_idx in range(num_devices):
                    create_device_frame(parent, row_idx, system_key, systems_devices_data_dict)
        #endregion
        
        device_base_frame = create_device_base_frame(parent)
        device_data_frame = create_data_frame(device_base_frame)
        iter_generate_device_frame(device_data_frame, system_key, systems_devices_data_dict, max_device_data_char_dict)
        
        return device_base_frame

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
