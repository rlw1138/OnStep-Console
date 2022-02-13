"""
classes to replace the default Messagebox dialogs

these are styled dark for OnStep


the methods from tkSimpleDialog are used here as well as by
the classes in settings.py
"""

import tkinter as tk
import tkSimpleDialog #edited for OnStep 'style'

_bg='gray19'
_fg='tomato'


class ShowInfo_Dark(tkSimpleDialog.Dialog):
    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text=title).pack()
        tk.Label(parent, bg=_bg, fg=_fg, text=text, anchor='w').pack()
        #return self # initial focus


    def buttonbox(self):
        # this method overrides the one in the Dialog class

        box = tk.Frame(self)
        box.config(bg=self._bg)

        w = tk.Button(box, text="OK", width=10, command=self.ok)
        w.config(bg=self._bg, fg=self._fg, pady=4, activebackground='red')
        w.config(highlightbackground='red')
        w.config(highlightcolor='green2')
        w.config(highlightthickness=1)
        w.pack(side='left')

        self.bind("<Return>", self.ok)
        #self.bind("<Escape>", self.cancel)

        box.pack()


    # this method overrides the one in the Dialog class
    def apply(self):
        return True

    # this method overrides the one in the Dialog class
    def valid_input(self):
        return True # valid inputs



class AskOkCancel_Dark(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text=title).pack()
        tk.Label(parent, bg=_bg, fg=_fg, text=text, anchor='w').pack()
        #return self # initial focus

    # this method overrides the one in the Dialog class
    def apply(self):
        return True

    # this method overrides the one in the Dialog class
    def valid_input(self):
        return True # valid inputs


class AskYesNo_Dark(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text=title).pack()
        tk.Label(parent, bg=_bg, fg=_fg, text=text, anchor='w').pack()
        #return self # initial focus

    def buttonbox(self):
        # this method overrides the one in the Dialog class
        box = tk.Frame(self)
        box.config(bg=self._bg)

        w = tk.Button(box, text="Yes", width=10, command=self.yes)
        w.config(bg=self._bg, fg=self._fg, pady=4, activebackground='red')
        w.config(highlightbackground='red')
        w.config(highlightcolor='green2')
        w.config(highlightthickness=1)
        w.pack(side='left')

        w = tk.Button(box, text="No", width=10, command=self.no)
        w.config(bg=self._bg, fg=self._fg, pady=4, activebackground='goldenrod1')
        w.config(highlightbackground='goldenrod1')
        w.config(highlightcolor='red')
        w.config(highlightthickness=1)
        w.pack(side='left')

        self.bind("<Return>", self.yes)
        self.bind("<Escape>", self.no)

        box.pack()

    def apply(self):
        return True

    # this method overrides the one in the Dialog class
    def valid_input(self):
        return True # valid inputs


#EOF messagebox_dark
