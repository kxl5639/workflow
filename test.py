# import tkinter as tk
# from tkinter import ttk

# test_window = tk.Tk()

# dividing_frame = ttk.Frame(test_window)
# dividing_frame.grid()

# label1 = ttk.Entry(dividing_frame, text = 'Label 1')
# label1.grid(row=0,column = 0)

# button1 = ttk.Button(dividing_frame, text = "Button 1")
# button1.grid(row=0,column = 1)

# button1 = ttk.Button(dividing_frame, text = "Button 1")
# button1.grid(row=1,column = 0, columnspan=2)


# test_window.mainloop()





def calculate_sum(a, b):
    """
    Calculate the sum of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

print(calculate_sum(1,4))