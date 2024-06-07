import tkinter as tk
from tkinter import ttk
from utils import center_window
from components.buttons import create_addmodifydelete_buttons
from design_eng.design_eng_utils import populate_treeview_with_design_engs, design_eng_columns_to_display
from design_eng.design_eng_add.design_eng_add_view import open_add_design_eng_window  
#from design_eng.design_eng_modify.design_eng_modify_view import open_modify_design_eng_window
#from design_eng.design_eng_delete.design_eng_delete_controller import delete_selected_design_engs


def create_design_eng_window():
    window = tk.Toplevel()
    window.title("Design Engineers")

    # Create the treeview
    columns = design_eng_columns_to_display()
    tree = ttk.Treeview(window, columns=columns, show='headings')

    # Define the column headings and set a minimum width
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=max(10, len(col.replace("_", " ").title()) * 10), anchor='center')

    # Fetch the design_eng data and insert it into the treeview
    populate_treeview_with_design_engs(tree)

    tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create and add the action buttons    
    button_frame = create_addmodifydelete_buttons(
        window,
        add_command=lambda: open_add_design_eng_window(tree),
        modify_command=lambda: open_modify_design_eng_window(tree),
        delete_command=lambda: delete_selected_design_engs(tree)
    )
    button_frame.pack(pady=10)
  
    # Center the window after adding widgets
    center_window(window)

    # Bring the window to the front and set focus
    window.focus_force()

    window.mainloop()
