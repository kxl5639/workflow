from view import BaseWindow
from utils import center_window
import tkinter as tk
from tkinter import ttk

def open_title_manager_window():
    root = TitleMangerView('Title Manager').root

    center_window(root)

class TitleMangerView(BaseWindow):
    ROW = 0
    def __init__(self, title, is_root=False):
        super().__init__(title, is_root)
        self.root.resizable(width=True,height=True)
        
        self.entries_frame = ttk.Frame(self.root)
        self.entries_frame.grid(row=0,column=0, padx=10,pady=10, sticky='nsew')        
        self.entries_frame.columnconfigure(1, weight=1)

        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.grid(row=0,column=1, padx = (0,10), pady = 10, sticky='nsew')                

        self.first_label = ttk.Label(self.entries_frame, text='1')
        self.first_label.grid(row=TitleMangerView.ROW,column=0, padx=(0,5),pady=10,sticky='w')

        self.first_entry = ttk.Entry(self.entries_frame)
        self.first_entry.grid(row=TitleMangerView.ROW,column=1, padx=(0),pady=10,sticky='ew')

        def add_entry(self):    
            TitleMangerView.ROW += 1             
            self.label = ttk.Label(self.entries_frame, text=TitleMangerView.ROW+1)
            self.label.grid(row=TitleMangerView.ROW,column=0, padx=(0,5),pady=10,sticky='w')

            self.entry = ttk.Entry(self.entries_frame)
            self.entry.grid(row=TitleMangerView.ROW,column=1, padx=(0),pady=10,sticky='ew')    


        self.add_button = ttk.Button(self.menu_frame, text='Add Title',command = lambda:add_entry(self))
        self.add_button.grid(row=0,column=0, padx = 0, pady = 10, sticky='nw')

    
    def add_entry(self):    
        TitleMangerView.ROW += 1    
        self.label = ttk.Label(self.entries_frame, text='1')
        self.label.grid(row=TitleMangerView.ROW,column=0, padx=(10,5),pady=10,sticky='w')

        self.entry = ttk.Entry(self.entries_frame)
        self.entry.grid(row=TitleMangerView.ROW,column=1, padx=(0,10),pady=10,sticky='ew')

        

    
