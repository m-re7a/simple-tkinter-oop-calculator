# importings
import tkinter as tk
from math import pi, e, floor, sqrt, factorial, log
from math import sin, cos, tan, asin as arcsin, acos as arccos, atan as arctan
# ======================================================================
cot = lambda x: 1/tan(x)
arccot = lambda x: 1/arctan(x)

def calculation(cls):
    
    current_entry = str(cls.entry.get()).lower()
    current_entry = current_entry.replace(' ','')

    #replacing some symbols to interpretable phrases    
    equivalents = (('x','*'),('^','**'),('\u00f7','/'),
                   ('\u03C0','pi'), ('\u221A','sqrt'))
    for i,j in equivalents:
            current_entry = current_entry.replace(i,j)

    # the process of detecting factorial symbols (!) in text, get the
    # number behind each one then place numbers in factorial function
    if '!' in current_entry:
        full = ''
        splits = current_entry.split('!')
        rest = splits.pop()
        for split in splits:
            if split:
                ind = len(split) -1
                while split[ind].isnumeric():
                    if not ind: break
                    ind -= 1
                if not split[ind].isnumeric(): ind += 1
                full+= split[:ind]+'factorial({})'.format(split[ind:])+rest
        current_entry = full

    if current_entry:
        try:
            answer = str(round(eval(current_entry),10))
            cls.entry.delete(-1, tk.END)
            cls.entry.insert(0, answer)
            cls.lable.config(text= answer[:17])
        except:
            cls.lable.config(text= 'Something Went Wrong')
    else:
        cls.lable.config(text= '')
        
def is_number(value):
        try:
            float(value)
            if value[0] not in ['+','-']:
                return True
        except ValueError:
            return False