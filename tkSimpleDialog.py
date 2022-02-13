'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

##       Creating a simple dialog, revisited

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

https://effbot.org/tkinterbook/tkinter-dialog-windows.htm

## example implementation:

import tkinter as tk
import tkSimpleDialog

class MyDialog(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class (below)
    def body(self, parent):

        tk.Label(parent, text="First:").grid(row=0)
        tk.Label(parent, text="Second:").grid(row=1)

        self.e1 = tk.Entry(parent)
        self.e2 = tk.Entry(parent)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class (below)
    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print(first, second) # or something
'''


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""
        file:  tkSimpleDialog.py

the methods from tkSimpleDialog are used in
    -- messagebox_dark.py
    -- settings.py
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#from Tkinter import *
import tkinter as tk
import os

""" V V V V V V  Styled DARK for OnStep Console  V V V V V V V V """
class Dialog(tk.Toplevel):

    def __init__(self, parent, windowTitle=None, text=None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.attributes('-topmost',True)
        if windowTitle:
            self.title=windowTitle
        else:
            self.title="Settings"
        self.parent = parent
        self.text=text
        self.result = None
        self._bg='gray19'
        self._fg='tomato'
        self.config(bg=self._bg)
        body = tk.Frame(self)
        body.config(bg=self._bg)
        self.initial_focus = self.body(body,self.title,self.text)
        body.pack(padx=20, pady=20)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)


    #
    # construction hooks
    #
    def body(self, parent, title, text):   #   THIS METHOD must BE OVERRIDDEN
        # create dialog body.
        # return widget that should have initial focus.
        pass

    """ V V V V V V  Styled DARK for OnStep Console  V V V V V V V V """
    def buttonbox(self):
        # add standard button box.
        # override if you don't want the standard buttons

        box = tk.Frame(self)
        box.config(bg=self._bg)

        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.config(bg=self._bg, fg=self._fg, pady=4, activebackground='goldenrod1')
        w.config(highlightbackground='goldenrod1')
        w.config(highlightcolor='red')
        w.config(highlightthickness=1)
        w.pack(side='left')
        w = tk.Button(box, text="OK", width=10, command=self.ok)
        w.config(bg=self._bg, fg=self._fg, pady=4, activebackground='red')
        w.config(highlightbackground='red')
        w.config(highlightcolor='green2')
        w.config(highlightthickness=1)
        #w.pack(side='left', padx=5, pady=5)
        w.pack(side='left')

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


    #
    # standard button semantics
    #
    def ok(self, event=None):
        if not self.valid_input():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        result = self.apply()
        self.cancel(result)

    def cancel(self, result=False, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        return result

    def yes(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.parent.focus_set()
        self.destroy()
        return "Yes"

    def no(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.parent.focus_set()
        self.destroy()
        return "No"


    #
    # command hooks
    #
    def valid_input(self):   #   THIS METHOD COULD BE OVERRIDDEN
        return 0 #        OVERRIDE

    def apply(self):   #   THIS METHOD must BE OVERRIDDEN
        pass #         OVERRIDE







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
showinfo, showwarning, showerror,
askquestion, askokcancel, askyesno, or askretrycancel

'''
## #    try:
## #        fp = open(filename)
## #    except:
## #        tkMessageBox.showwarning(
## #            "Open file",
## #            "Cannot open this file\n(%s)" % filename
## #        )
## #        return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
