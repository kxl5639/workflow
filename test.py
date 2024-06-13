# import tkinter as tk
# from tkinter import ttk, Toplevel, Listbox, StringVar, Entry, END
# from sqlalchemy.inspection import inspect
# from utils.controller import populate_treeview
# from utils.button import create_addmodifydelete_buttons
# from project.project_add.project_add_view import open_add_project_window #type:ignore 
# from project.project_modify.project_modify_view import open_modify_project_window #type:ignore 
# from project.project_delete.project_delete_controller import delete_selected_projects #type:ignore 
# from project.project_model import Project, session # type: ignore
# from project.project_controller import columns_to_display # type: ignore
# from utils.view import center_window, create_tree_and_addmoddel_buttons_frame #type:ignore 



# def create_tree_frame_from_db_table(master,columns, session, model):    
#     tree_frame = ttk.Frame(master)    
    
#     tree = ttk.Treeview(tree_frame,columns=columns, show='headings')
#     tree.pack()
    
#     # Define the column headings and set a minimum width
#     for col in columns:
#         tree.heading(col, text=col.replace("_", " ").title())
#         tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

#     populate_treeview(tree, model, session, columns)
#     return tree_frame

# test_window = tk.Tk()
# test_window.title("Test Window")

# tree_frame = create_tree_frame_from_db_table(test_window, columns_to_display, session, Project)
# tree_frame.pack()


# test_window.mainloop()


# import tkinter as tk
# from tkinter import ttk

# def create_sticky_grid():
#     root = tk.Tk()
#     root.title("Sticky Example")
#     root.geometry("400x300")

#     # Configure the grid for the root window
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_rowconfigure(1, weight=1)
#     root.grid_rowconfigure(2, weight=1)
#     root.grid_rowconfigure(3, weight=1)
#     root.grid_rowconfigure(4, weight=1)
#     root.grid_rowconfigure(5, weight=1)
#     root.grid_rowconfigure(6, weight=1)

#     # Create frames with different sticky values, background colors, and add labels
#     frame1 = tk.Frame(root, width=100, height=50, bg="red", borderwidth=2, relief="solid")
#     frame1.grid(row=0, column=0, sticky="n")
#     # label1 = ttk.Label(frame1, text="sticky='n'")
#     # label1.pack(expand=True)

#     frame2 = tk.Frame(root, width=100, height=50, bg="green", borderwidth=2, relief="solid")
#     frame2.grid(row=1, column=0, sticky="e")
#     # label2 = ttk.Label(frame2, text="sticky='e'")
#     # label2.pack(expand=True)

#     frame3 = tk.Frame(root, width=100, height=50, bg="blue", borderwidth=2, relief="solid")
#     frame3.grid(row=2, column=0, sticky="s")
#     # label3 = ttk.Label(frame3, text="sticky='s'")
#     # label3.pack(expand=True)

#     frame4 = tk.Frame(root, width=100, height=50, bg="yellow", borderwidth=2, relief="solid")
#     frame4.grid(row=3, column=0, sticky="w")
#     # label4 = ttk.Label(frame4, text="sticky='w'")
#     # label4.pack(expand=True)

#     frame5 = tk.Frame(root, width=100, height=50, bg="orange", borderwidth=2, relief="solid")
#     frame5.grid(row=4, column=0, sticky="ns")
#     # label5 = ttk.Label(frame5, text="sticky='ns'")
#     # label5.pack(expand=True)

#     frame6 = tk.Frame(root, width=100, height=50, bg="purple", borderwidth=2, relief="solid")
#     frame6.grid(row=5, column=0, sticky="ew")
#     # label6 = ttk.Label(frame6, text="sticky='ew'")
#     # label6.pack(expand=True)

#     frame7 = tk.Frame(root, width=100, height=50, bg="cyan", borderwidth=2, relief="solid")
#     frame7.grid(row=6, column=0, sticky="nsew")
#     # label7 = ttk.Label(frame7, text="sticky='nsew'")
#     # label7.pack(expand=True)

#     root.mainloop()

# if __name__ == "__main__":
#     create_sticky_grid()

import tkinter as tk

def update_grid_configure():
    for i in range(3):
        weight = row_weights[i].get()
        root.grid_rowconfigure(i, weight=weight)
        col_weight = col_weights[i].get()
        root.grid_columnconfigure(i, weight=col_weight)

def create_grid():
    for i in range(3):
        for j in range(3):
            label = tk.Label(root, text=f"Row {i} Col {j}", borderwidth=1, relief="solid")
            sticky_val = sticky_vars[i][j].get()
            label.grid(row=i, column=j, sticky=sticky_val)

root = tk.Tk()
root.title("Grid Attribute Tester")

# Variables for sticky attributes
sticky_vars = [[tk.StringVar(value="") for _ in range(3)] for _ in range(3)]

# Variables for row and column weights
row_weights = [tk.IntVar(value=1) for _ in range(3)]
col_weights = [tk.IntVar(value=1) for _ in range(3)]

# Control panel for adjusting grid attributes
control_panel = tk.Frame(root)
control_panel.grid(row=0, column=3, rowspan=3, sticky="nsew")

tk.Label(control_panel, text="Row Weights:").grid(row=0, column=0, sticky="w")
for i in range(3):
    tk.Entry(control_panel, textvariable=row_weights[i], width=5).grid(row=i+1, column=0, sticky="w")

tk.Label(control_panel, text="Column Weights:").grid(row=0, column=1, sticky="w")
for i in range(3):
    tk.Entry(control_panel, textvariable=col_weights[i], width=5).grid(row=i+1, column=1, sticky="w")

# Sticky control
tk.Label(control_panel, text="Sticky:").grid(row=0, column=2, sticky="w")
sticky_options = ["", "n", "s", "e", "w","ew", "ne", "nw", "ns", "se", "sw", "nsew"]
for i in range(3):
    for j in range(3):
        sticky_menu = tk.OptionMenu(control_panel, sticky_vars[i][j], *sticky_options)
        sticky_menu.grid(row=i+1, column=2+j, sticky="w")

# Update grid configuration button
update_button = tk.Button(control_panel, text="Update Grid", command=lambda: [create_grid(), update_grid_configure()])
update_button.grid(row=4, column=0, columnspan=3)

create_grid()
update_grid_configure()

root.mainloop()