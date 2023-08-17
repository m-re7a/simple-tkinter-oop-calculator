'''
the idea is to create a button panel that consists of 4 seperated parts,
so we are able to manage each one easily! each part (widget) inherits from
tkinter.Frame (except one):

    1) NumbersPad: contains Numbers, Point and Paranthesis

    2) BasicFuncs: contains main functions in mathematics such as
    Addition, Subtraction, Multiplication, Division and buttons such as
    Equal, Percentage, AC(All Clear) and DEL(Delete)

    3) AdvancedFuncs: contains other functions like Power, Radical, Logarithm and etc.
    in additons to these functions, there's a button named Tri (refers to Trigonometry);
    by clicking this button, a pop-up window appears that include sin, cos and... buttons.
    
    Note: when app runs, basic mode is displayed by default. to use more functions
    it's necessary to change the mode from 'Basic' to 'Advanced' from option menu.

    4) Trigonometry: it's a pop up widget that inhertis from tkinter.TopLevel 
    class. it'll be shown by clicking the Tri Botton. includes buttons such as
    sin, cos, tan, cot and their reverses (arc sin, arc cos and etc.)
'''


# importings
import tkinter as tk
from auth.theme import Colors
from auth.process import calculation, is_number
import string

# ======================================================================


class NumbersPad(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg= Colors['bg'])

        values = list(string.digits)[1:]+['.','0','()']
        self.btns = [self.create_buttons(value) for value in values]
        row = 0
        for i,btn in enumerate(self.btns):
            if i%3 == 0: row += 1
            btn.grid(row=row,column=i%3, padx=5, pady=5)
        
    def create_buttons(self,value):
        return tk.Button(self, text= value, height=1, width=6, bg=Colors['btn1'],
                        relief=tk.SOLID, font= 'latinmodern-math 10',
                        command= lambda: self.click_btn(value))

    def click_btn(self, value):

        current_entry = str(self.master.entry.get())
        position = self.master.entry.index(tk.INSERT) #index of entring text cursor

        if value == '()':
            if not position:
                self.entry_set(position, value, 1)
            else:
                if current_entry[position-1].isnumeric() or current_entry[position-1] == ')': self.entry_set(position, '*'+value, 2)
                else: self.entry_set(position, value, 1)
        else:
            self.entry_set(position, value, 1)
        
    
    def entry_set(self, position, value, set_index):
        self.master.entry.insert(position, value)
        self.master.entry.icursor(position+set_index)

# ======================================================================

class BasicFuncs(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg= Colors['bg'])
        
        values = ['AC' , 'DEL', '-'  , '+'  , '\u00f7'  , 'x'  , '%'  , '='  ]
        
        self.btns = [self.create_buttons(value) for value in values]
        row = 0
        for i,btn in enumerate(self.btns):
            if i%2 == 0: row += 1
            btn.grid(row=row,column=i%2, padx=5, pady=5)
        
        
    def create_buttons(self,value):
        return tk.Button(self, text= value, height=1, width=6,
                         bg=Colors['btn2'], fg= Colors['btn2_text'] , 
                        relief= tk.FLAT, command= lambda: self.click_btn(value))

    def click_btn(self, value):

        current_entry = str(self.master.entry.get())
        position = self.master.entry.index(tk.INSERT)
        

        if value == '=':
            calculation(self.master)
        
        elif value == 'x':
            self.entry_set(position, '*', 1)

        elif value == 'AC':
            self.master.entry.delete(0, tk.END)

        
        elif value == 'DEL':
            if position: self.master.entry.delete(position-1)
        
        # there is two way to caculate the percentage of numbers:
        # 1) add % symbol next to numbers and then calculate them in the end
        # 2) calculate the percentage of any number by click the button and replace the old one with the resault 
        # I prefered to choose the seconde one! here is the process:
        elif value == '%':
            if position:
                first = position-1 #index of character behind text cursor
                if current_entry[first].isnumeric():
                    number = ''
                    while is_number(current_entry[first: position]):
                        number = current_entry[first: position]
                        first -= 1
                        if first == -1: break
                    
                    number_divided_by_100 = str(round(eval(number+'/100'),20))

                    self.master.entry.delete(first+1, position)
                    self.master.entry.insert(first+1, number_divided_by_100)
                    self.master.entry.icursor(first+len(number_divided_by_100)+1)

        else:
            self.entry_set(position, value, 1)
    

    def entry_set(self, position, value, set_index):
        self.master.entry.insert(position,value)
        self.master.entry.icursor(position+set_index)
        
# ======================================================================

class Trigonometry(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.grab_set()
        self.resizable(width= False, height=False)
        self.title('')

        self.configure(bg= Colors['bg'])

        values = ['sin()','cos()','tan()','cot()',
                  'arcsin()', 'arccos()', 'arctan()','arccot()']
        self.btns = [self.create_buttons(value) for value in values]
        row = 0
        for i,btn in enumerate(self.btns):
            if i%4 == 0: row += 1
            btn.grid(row=row,column=i%4, padx=5, pady=5)

        self.wm_transient(self.master)
    
    def create_buttons(self,value):
        return tk.Button(self, text= value, height=1, width=6,
                        bg= Colors['btn2'], fg= Colors['btn2_text'],
                        relief= tk.FLAT, command= lambda: self.click_btn(value))

    def click_btn(self, value):
        
        current_entry = str(self.master.entry.get())
        position = self.master.entry.index(tk.INSERT)

        if not position: self.entry_set(position, value, len(value)-1 )
        else:
            if current_entry[position-1].isnumeric() or current_entry[position-1] == ')': self.entry_set(position, '*'+value, len(value) )
            else: self.entry_set(position, value, len(value)-1 )


    def entry_set(self, position, value, set_index):
        self.master.entry.insert(position, value)
        self.master.entry.icursor(position+set_index)
        self.destroy()
        
# ======================================================================

class AdvancedFuncs(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg= Colors['bg'])

        values = ['x\u207f','|x|','1/x','Tri','\u03C0',
                  '\u221A', '[x]', 'x!','Log', 'e' ]
        self.btns = [self.create_buttons(value) for value in values]
        row = 0
        for i,btn in enumerate(self.btns):
            if i%5 == 0: row += 1
            btn.grid(row=row,column=i%5, padx=5, pady=5)
        
    def create_buttons(self,value):
        return tk.Button(self, text= value, height=1, width=6,
                                bg= Colors['btn2'], fg= Colors['btn2_text'],
                    relief= tk.FLAT, command= lambda: self.click_btn(value))
    
    def click_btn(self, value):

        current_entry = str(self.master.entry.get())
        position = self.master.entry.index(tk.INSERT)
        check_num = current_entry[position-1].isnumeric() if position else False


        if value == 'Tri': # shows Trigonometry pop-up window
            pop_up = Trigonometry(self.master)
            pop_up.mainloop()

        elif value == 'x\u207f': # Power xⁿ
            if check_num: self.entry_set(position, '^()', 2)
        
        elif value == 'x!': #Factorial
            if check_num: self.entry_set(position, '!', 1)
        
        elif value == '1/x': #Reverse
            if check_num: self.entry_set(position, '^(-1)', 5)
        

        elif value == '|x|': # Absolute value
            self.entry_set_2(current_entry, position, 'abs()', 4)

        elif value == '\u03C0': # pi π
            self.entry_set_2(current_entry, position, value, 1)

        elif value == '\u221A': # Sqrt √
            self.entry_set_2(current_entry, position, value+'()', 2)

        elif value == '[x]': #Correct component
            self.entry_set_2(current_entry, position, 'floor()', 6)


        elif value == 'Log': #Logarithm (default: natural base)
            self.entry_set_2(current_entry, position, 'log(,e)', 4)

        elif value == 'e': #Euler's (Neper's) number e
            self.entry_set_2(current_entry, position, value, 1)
            
    
    def entry_set(self, position, value, set_index):
        self.master.entry.insert(position, value)
        self.master.entry.icursor(position+set_index)
    
    def entry_set_2(self,current_entry, position, value, set_index):
        if not position:
                self.entry_set(position, value, set_index)
        else:
            if current_entry[position-1].isnumeric() or current_entry[position-1] == ')':
                self.entry_set(position, '*'+value, set_index+1)
            else: self.entry_set(position, value, set_index)
