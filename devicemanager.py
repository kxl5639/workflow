from class_collection import ListWindow, Controller, Model
from model import Device

class DeviceListBaseController(Controller):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.model = DeviceListBaseModel(self)
        self.column_map = self.model.column_map
        self.table_data = self.model.table_data
        self.button_info = None

class DeviceListBaseView(ListWindow):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)
        self.button_frame = None

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


        
# [(1, 'TEST', 'XX/XX/XX', 'UBS', '32nd Floor', '123 Main St', 'Rayan Zabib', 'TEST', 'TEST', 'Kevin Lee', 'David Green'), (2, '2265B', 'XX/XX/XX', 'TEST', 'TEST', 'TEST', 'TEST TEST', 'Bob Smith', 'XYZ Contractors', 'Kevin Lee', 'David Green'), (3, '2278B', 'XX/XX/XX', 'UBS', '32nd Floor', '123 Main St', 'Rayan Zabib', 'Bob Smith', 'XYZ Contractors', 'Kevin Lee', 'David Green')]