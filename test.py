from project.project_model import field_metadata
import tkinter as tk

def fields_from_dbtable():
    fields = field_metadata.keys()
    frame_ass = {field: field_metadata[field]["frame"] for field in fields}
    max_frames = max([value["frame"] for value in field_metadata.values()])
    return fields, frame_ass, max_frames
    
fields , frame_ass, max_frames = fields_from_dbtable()
#print(fields)
#print(max_frames)


window = tk.Tk()
for i in range(max_frames):
        [print(i)]

frames = {i: tk.Frame(window) for i in range(1, max_frames+1)}
for i, frame in frames.items():
    frame.grid(row=0, column=(i-1)*2, padx=10, pady=10, sticky="n")

# print(i)
# print(range(max_frames))