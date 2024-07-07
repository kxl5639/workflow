from title.title_view import TitleView
from title.title_model import TitleModel, DwgTitle
from tkinter import messagebox
from class_collection import Controller

class TitleController(Controller):
    def __init__(self, parent=None, project_number=None) -> None:
        super().__init__(parent, project_number)
        self.view = TitleView('Title Manager', self.parent, self, project_number=None)
        self.model = TitleModel()

#region View
    def add_entry(self, parent):
        """Add a new entry widget to the view."""
        self.view.create_entry_widget(parent)

    def moveup_entry(self):
        """Move the selected entry widget up."""
        self.view.move_entry('up')

    def movedown_entry(self):
        """Move the selected entry widget down."""
        self.view.move_entry('down')
    
    def on_project_combobox_selected(self):
        """Handle project combobox selection."""
        self.view.on_project_selected()
#endregion

#region Model
    def get_project_object(self, project_number):
        """Get project object from the model."""
        return self.model.get_project_object(project_number)
    
    def get_title_object(self, project_object):
        """Get title object list from the model."""
        return self.model.get_title_object(project_object)
    
    def update_new_page_title_dict(self):
        """Update the new page title dictionary and return it along with pages to be deleted."""
        entry_widget_list = self.view.get_all_entry_widgets(self.view.root)
        new_titles, removed_indices = self.model._remove_end_blanks([title.get() for title in entry_widget_list])    
        pages_to_be_deleted_from_screen = [item+1 for item in removed_indices]
        new_page_title_dict = {idx+1: title for idx, title in enumerate(new_titles)} 
        return new_page_title_dict, pages_to_be_deleted_from_screen
    
    def commit_titles(self, project_number): 
        """Commit titles to the model."""
        project_obj = self.get_project_object(project_number)
        existing_title_record_objs = self.get_title_object(project_obj)        
        new_page_title_dict, pages_to_be_deleted_from_screen = self.update_new_page_title_dict()        
        existing_page_titleobj_dict = {idx + 1: title_obj for idx, title_obj in enumerate(existing_title_record_objs)}
        
        # Destroy the end title entry widgets that are blank (view)
        if pages_to_be_deleted_from_screen != []:
            self.view.destroy_frames_if_labels_match(pages_to_be_deleted_from_screen)
            new_page_title_dict, pages_to_be_deleted_from_screen = self.update_new_page_title_dict()                        

        # Get list of title record objects to be deleted as well as entry widgets that need to be popped
        title_record_obj_to_delete = []
        for existing_page_number in list(existing_page_titleobj_dict.keys()):
            if existing_page_number not in new_page_title_dict:
                title_record_obj_to_delete.append(existing_page_titleobj_dict[existing_page_number])
                existing_page_titleobj_dict.pop(existing_page_number)
        
        # Delete records from table (model)
        self.model.delete_record(title_record_obj_to_delete)
        
        # Continue to update/add new title records(model)
        for new_page_number, new_title_name in new_page_title_dict.items():
            if new_page_number in existing_page_titleobj_dict:
                # This page already exist. We are just updating the existing title name only if they are different
                if existing_page_titleobj_dict[new_page_number].title != new_title_name:
                    existing_page_titleobj_dict[new_page_number].title = new_title_name                
            else:
                # This is a new page that we are adding                
                new_title_record = DwgTitle(dwgno=new_page_number,
                                            title = new_title_name,
                                            project_id = project_obj.id)
                self.model.add_record(new_title_record)

        # Commit changes
        self.model.commit_changes()
#endregion

#region title SCR script generator
    def write_text_style(self, font):
        return ["-style\n", f"{font}\n", '\n', '0\n', '\n', '\n', '\n', '\n','\n',]   

    def create_layout_title_start_coord_arr(self, number_of_titles):
        start_point = {}
        start_point['x'] = 0
        start_point['y'] = -1
        textbox_height = 0.5
        coord_dict = {}    
        for i in range(number_of_titles):
            coord_dict[i] = [start_point['x'], start_point['y'] - (i*textbox_height)]
        return coord_dict

    def create_layout_title_end_coord_arr(self, number_of_titles):
        end_point = {}
        end_point['x'] = 1.75
        end_point['y'] = -1.5
        textbox_height = 0.5
        coord_dict = {}    
        for i in range(number_of_titles):
            coord_dict[i] = [end_point['x'], end_point['y'] - (i*textbox_height)]
        return coord_dict    

    def populate_layout_titles(self, number_of_titles, titles_list):
        txt_height = 0.07
        start_coord_dict = self.create_layout_title_start_coord_arr(number_of_titles)
        end_coord_dict = self.create_layout_title_end_coord_arr(number_of_titles)
        lines = []
        for i in range(number_of_titles):        
            lines.append("-mtext\n")
            lines.append(f'{start_coord_dict[i][0]},{start_coord_dict[i][1]}\n')
            lines.append("justify\n")
            lines.append("mc\n")
            lines.append("style\n")
            lines.append("romand\n")
            lines.append("height\n")
            lines.append(f'{txt_height}\n')
            lines.append("columns\n")
            lines.append("no\n")
            lines.append(f'{end_coord_dict[i][0]},{end_coord_dict[i][1]}\n')
            lines.append(f'{titles_list[i]}\n')
            lines.append("\n")
        return lines

    def populate_cover_page_toc(self, number_of_titles, titles):    
        start_point1 = {}
        start_point1['x'] = 1.1
        start_point1['y'] = 5.68
        start_coord_offset = 9
        cutoff = 30
        lines = []
        lines = ["-mtext\n", f'{start_point1["x"]},{start_point1["y"]}\n', "justify\n",
                "TL\n", "style\n", "romand\n", "height\n", "0.1\n", "columns\n", "no\n",
                f'{start_point1["x"]+start_coord_offset},{start_point1["y"]-start_coord_offset}\n']
        if number_of_titles > cutoff: 
            for i in range(cutoff):
                lines.append(f'{i+1}. {titles[i]}\n')
        else:
            for i in range(number_of_titles):
                lines.append(f'{i+1}. {titles[i]}\n')
        lines.append("\n")
        
        if number_of_titles > cutoff:
            start_point2 = {}
            start_point2['x'] = start_point1['x']+6.4
            start_point2['y'] = start_point1['y']
            lines.extend(["-mtext\n", f'{start_point2["x"]},{start_point2["y"]}\n', "justify\n",
                            "TL\n", "style\n", "romand\n", "height\n", "0.1\n", "columns\n", "no\n",
                            f'{start_point2["x"]+start_coord_offset},{start_point2["y"]-start_coord_offset}\n'])
            for i in range(cutoff, number_of_titles):
                lines.append(f'{i+1}. {titles[i]}\n')
        lines.append("\n")    
        return lines

    def populate_titles_of_dwgs(self, number_of_titles, titles):
        lines = ["-layer\n", "N\n", "ToCSCR\n", "color\n", "40\n", "ToCSCR\n", "M\n", "ToCSCR\n", "\n"]
        start_coord = {}
        start_coord['x'] = 18 + 7.0685 #7.0685 is half the width of the dwg box
        start_coord['y'] = 10
        text_y_offset = 0.0732
        vertical_spacing = 12
        horizontal_spacing = 16
        sheet_width = 14.137
        text_height = 0.12
        j = 0
        for i in range(number_of_titles):
            if i % 10 == 0:
                lines.extend(['-text\n', 'justify\n', 'tc\n'])
                coord10_start = {}
                coord10_start['x'] = start_coord["x"]
                coord10_start['y'] = start_coord["y"] - (j*vertical_spacing) - text_y_offset
                lines.append(f'{coord10_start['x']}, {coord10_start['y']}\n')
                lines.append(f'{text_height}\n')
                lines.extend(['\n'])
                lines.extend([f'%%u{titles[i]}\n'])
                j += 1
            else:
                lines.extend(['-text\n', 'justify\n', 'tc\n'])
                coord_non10_start = {}
                coord_non10_start['x'] = start_coord["x"] + ((i - ((j - 1) * 10)) * horizontal_spacing)
                coord_non10_start['y'] = start_coord["y"] - ((j - 1) * vertical_spacing) - text_y_offset
                lines.extend(f'{coord_non10_start['x']}, {coord_non10_start['y']}\n')
                lines.append(f'{text_height}\n')
                lines.extend(['\n'])
                lines.extend([f'%%u{titles[i]}\n'])
        return lines

    def write_scr(self, project_number):        
        save_titles = messagebox.askyesno('Save Titles', 'Tiltes must be saved before generating SCR script.\nDo you want to save titles now?', parent=self.view.root)
        if save_titles == True:
            self.commit_titles(self.view.project_number)
            project_obj = self.get_project_object(project_number)
            titles_objs = self.get_title_object(project_obj) 
            titles_list = [title_object.title for title_object in titles_objs]
            number_of_titles = len(titles_list)
            scr_dict = {'init_properties' : ["osmode\n", "0\n", "-layer\n", "N\n", "ToCSCR\n", "color\n",
                                                "green\n", "ToCSCR\n", "M\n", "ToCSCR\n", "\n",],
                        'romand_text_style' : self.write_text_style('romand'),
                        'romans_text_style' : self.write_text_style('romans'),
                        'populate_layout_titles' : self.populate_layout_titles(number_of_titles, titles_list),
                        'populate_cover_page_toc' : self.populate_cover_page_toc(number_of_titles, titles_list),
                        'populate_titles_of_dwgs' : self.populate_titles_of_dwgs(number_of_titles, titles_list),
                        'final_properties' : ["osmode\n", "7335\n", "-layer\n", "set\n", "1-1\n", "\n",]
                        }

            scr_script = []
            scr_script = [item for sublist in scr_dict.values() for item in sublist]

            with open('SRC.src', 'w') as file:
                file.writelines(scr_script)
            self.view.root.focus_force()
#endregion