
import tkinter as tk
from tkinter import *
import time

"""combines ToolTip() and MenuTooltip(), to become Menu_ToolTip() """

"""
        menu = Menu_ToolTip(self)
        menu.add_command(label='Help 1', tooltip='\tToolTip.Help 1')
        menu.add_command(label='Help 2', tooltip='\tToolTip.Help 2')
        self.menubar.add_cascade(label="Help", menu=menu)
"""

class Menu_ToolTip(tk.Menu):
    def __init__(self, parent):
        """
        :param parent: The parent of this Menu, either 'root' or 'Menubar'
         .tooltip == List of tuple (yposition, text)
         .tooltip_active == Index (0-based) of the active shown Tooltip
         Bind events <Leave>, <Motion>
        """
        super().__init__(parent, tearoff=0)
        self.tooltip = []
        self.tooltip_active = None
        self.widget = parent
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

        self.bind('<Leave>', self.on_leave)
        self.bind('<Motion>', self.on_motion)

    def add_command(self, *cnf, **kwargs):
        tooltip = kwargs.get('tooltip')
        if tooltip:
            del kwargs['tooltip']
        super().add_command(*cnf, **kwargs)
        self.add_tooltip(len(self.tooltip), tooltip)

    def add_tooltip(self, index, tooltip):
        """
        :param index: Index (0-based) of the Menu Item
        :param tooltip: Text to show as Tooltip
        :return: None
        """
        self.tooltip.append((self.yposition(index) + 2, tooltip))

    def on_motion(self, event):
        """
        Loop .tooltip to find matching Menu Item
        """
        for idx in range(len(self.tooltip) - 1, -1, -1):
            if event.y >= self.tooltip[idx][0]:
                self.show_tooltip(idx)
                break

    def on_leave(self, event):
        """
        On leave, destroy the Tooltip and reset .tooltip_active to None
        """
        if not self.tooltip_active is None:
            self.tooltip_active = None
            tw = self.tipwindow
            if tw:   tw.destroy()
            self.tipwindow = None


    def show_tooltip(self, idx):
        """
        Show the Tooltip if not already shown, destroy the active Tooltip
        :param idx: Index of the Tooltip to show
        :return: None
        """
        if self.tooltip_active != idx:
            self.tooltip_active = idx
        "Display text in tooltip window"
        self.text = self.tooltip[idx][1]
        if self.tipwindow or not self.text:
            return
        ## print('{}'.format(self.tooltip[idx][1]))
        self.update_idletasks()
        x, y, w, h = self.widget.bbox("insert")
        ## print("x{}xy{}yw{}wh{}h".format(x,y,w,h))
        ### wrx = self.winfo_rootx()
        ### wry = self.winfo_rooty()
        wpx = self.winfo_pointerx()
        wpy = self.winfo_pointery()
        wxp = self.xposition(idx)
        wyp = int(self.yposition(idx) / 11 )

        x =  wpx + wxp + 50
        y =  wpy + wyp + 17

        ## print("wrx{}x wry{}y wpx{}x wpy{}y wxp{}x wyp{}y".format(wrx,wry,wpx,wpy,wxp,wyp))
        ## print("X{}X Y{}Y".format(x,y))

        # x = x + cx + self.widget.winfo_rootx() + 157
        # y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="NavajoWhite2", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        self.update_idletasks()
        time.sleep(2.2)
        tw.destroy()

#background="#ffffe0",
#background="#f8f8e0",




# ''' THIS ONE CAN ONLY DO A TOP-LEVEL MENU ITEM (File, Edit, View, Search, Help, etc)
# but it draws a pretty good tiny pop-up window for the text
#
# x = menu_file.entrycget(0,'label') # 'New'
# y = menu_file.entrycget(1,'label') # 'Open..'
# z = menu_file.entrycget(2,'label') # 'Close...'
#
# print("{} - {} - {}".format(x, y, z ))
# '''
#
# """
# button = Button(root, text = 'click me')
# button.pack()
# CreateToolTip(button, text = 'Hello World\n'
#                  'This is how tip looks like.'
#                  'Best part is, it\'s not a menu.\n'
#                  'Purely tipbox.')
# """

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + cx + self.widget.winfo_rootx() + 157
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
