# importings
import tkinter as tk
from auth import buttons, widgets
from auth.process import calculation
from auth.theme import Colors
# ======================================================================

# creating root window (master class) and adding all other widgets to it
class Calc(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Calculator')
        self.configure(bg= Colors['bg'])
        self.resizable(width= False, height=False) # prevent from resizing

        # setting Entry widget
        self.entry = tk.Entry(self, font='arial 12')
        self.entry.focus_force()

        # setting Label to show the resault of calculation
        self.lable = tk.Label( height=1,bg=Colors['bg'],font='arial 12',fg='white', anchor='w')

        # setting widgets
        widgets.RightClick(self)
        self.NumbersPad = buttons.NumbersPad(self)
        self.BasicFuncs= buttons.BasicFuncs(self)
        self.AdvancedFuncs = buttons.AdvancedFuncs(self)

        self.bind('<Return>', lambda *args: calculation(self))

        # griding widgets (Except Advanced functoins)
        self.config(menu= widgets.Menu(self))
        self.entry.grid(column=0,row=1,padx=5,pady=5, sticky='WE')
        self.lable.grid(column=1, row=1,padx=5,pady=5, sticky='WE')
        self.NumbersPad.grid(column=0,row=2)
        self.BasicFuncs.grid(column=1, row=2)

        # centering the main window
        self.eval('tk::PlaceWindow . center')