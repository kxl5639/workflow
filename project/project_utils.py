from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from utils.msgbox import show_custom_error_message



def validate_date_format(date_str, parent_window):
    if date_str != "XX/XX/XX":
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%y').date()
            return date_obj.strftime('%m/%d/%y'), None  # Return formatted date and no error
        except ValueError:
            show_custom_error_message(parent_window, "Error", "Invalid Date Format. Please enter the date in MM/DD/YY format.")
            return None, "Invalid Date Format"
    return date_str, None  # Return the original placeholder and no error

