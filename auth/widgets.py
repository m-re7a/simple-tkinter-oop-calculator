# importings
import tkinter as tk
import _tkinter
import webbrowser
from auth.theme import Colors
# ======================================================================

selection_check = lambda cls: tk.ACTIVE if cls.entry.select_present() else tk.DISABLED

def clipboard_check(cls):
    try:
        cls.clipboard_get()
        return tk.ACTIVE
    except _tkinter.TclError: return tk.DISABLED

class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.mode = tk.BooleanVar()
        self.mode.set(0)
        self.mode.trace('w', self.mode_changer)

        options_menu = tk.Menu(self, tearoff=0)
        options_menu.add_radiobutton(label='Basic',    value=0, variable=self.mode)
        options_menu.add_radiobutton(label='Advanced', value=1, variable=self.mode)

        self.add_cascade(label="Options", menu= options_menu)
        self.add_command(label="About", command=self.about)
        self.add_command(label="Quit", command=self.master.destroy)
        
    def about(self):
        pop_up_window = tk.Toplevel(self.master,bg='white',)
        pop_up_window.grab_set()
        pop_up_window.resizable(width= False, height=False)
        pop_up_window.title('About')
        
        text1 = 'a simple and cool calculator!'
        text2 = 'Built-in:\n\nPython 3.x\ntkinter 8.6\n\n credits:\n\nMohammad Reza Ahamadi Foroud'
        text3 = 'check for more projects:'
        tk.Label(pop_up_window, text=text1,bg='white', fg=Colors['btn2'], font= 'arial 20 bold').grid(padx=10,pady=10)
        tk.Label(pop_up_window, text=text2,bg='white', fg=Colors['bg'], font='arial 15 italic ' ).grid(padx=10,pady=10)
        
        link = tk.Label(pop_up_window, text='github.com/froudx', bg='white', font='arial 17', cursor='hand2')
        tk.Label(pop_up_window, text=text3,bg='white', font='arial 12' ).grid(padx=10,pady=10)
        link.grid()
        link.bind('<Button-1>', lambda *args: webbrowser.open_new_tab('https://github.com/froudx'))
        
        tk.Button(pop_up_window, text='OK',bg= Colors['btn2'], fg ='white',relief=tk.FLAT, command= lambda: pop_up_window.destroy()).grid(padx=10,pady=10,sticky='WE')
        pop_up_window.wm_transient(self.master)
        pop_up_window.mainloop()
    
    def mode_changer(self, *args):
        if self.mode.get():
            self.master.AdvancedFuncs.grid(row=3, column=0, columnspan=2)
        else: self.master.AdvancedFuncs.grid_forget()
    

class RightClick(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.config(tearoff= 0, postcommand= self.enable_selection)
        self.add_command(label="Cut", command=self.cut_text)
        self.add_command(label="Copy", command=self.copy_text)
        self.add_command(label="Paste", command=self.paste_text)
        self.add_command(label="Delete", command=self.delete_text)

        self.master.entry.bind("<Button-3>", self.show_popup)

    
    def enable_selection(self):
         state_selection = selection_check(self.master)
         state_clipboard = clipboard_check(self.master)
			 
         self.entryconfig(0, state=state_selection) # Cut
         self.entryconfig(1, state=state_selection) # Copy
         self.entryconfig(2, state=state_clipboard) # Paste
         self.entryconfig(3, state=state_selection) # Delete


    def show_popup(self, event):
        self.tk_popup(event.x_root, event.y_root)

    def cut_text(self):
        self.copy_text()
        self.delete_text()

    def copy_text(self):
        selection = self.master.entry.selection_get()
        self.master.clipboard_clear()
        self.master.clipboard_append(selection)

    def paste_text(self):
        if selection_check(self.master) == tk.ACTIVE:
            inds = [self.master.entry.index('sel.{}'.format(mode)) for mode in ('first' , 'last')]
            current_entry = str(self.master.entry.get())
            self.master.entry.delete(inds[0], tk.END)
            self.master.entry.insert(inds[0], self.master.clipboard_get()+current_entry[inds[1]:])
        else: self.master.entry.insert(tk.INSERT, self.master.clipboard_get())



    def delete_text(self):
        inds = [self.master.entry.index('sel.{}'.format(mode)) for mode in ('first' , 'last')]
        self.master.entry.delete(inds[0], inds[1])