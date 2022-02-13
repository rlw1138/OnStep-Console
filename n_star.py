'''

ALIGN telescope to 1 or 2 or 3 stars

DEPENDENCY: align_stars.align_stars(text) -- provides a list of good stars to align on


#[com dot hotmail @ rlw1138] -- 2020-APR-15
'''
import tkinter as tk
from functools import partial
from tkinter import messagebox
import logging
import time

from go_to import GoTo
from messagebox_dark import AskOkCancel_Dark
from messagebox_dark import AskYesNo_Dark
from messagebox_dark import ShowInfo_Dark


class NStar_Align:


    """ these three global lists are filled-in from the
        'celestial_objects' Listbox selection(s)
    """
    RA_list = list()
    DE_list = list()
    Object_list = list()


    """star list file into Listbox"""
    def get_stars(self, parent, controller):
        def __init__(self):
            self.parent = parent
            self.controller = controller


        def selected_items(self, listbox):
            # Traverse the tuple returned by curselection method and print
            # corresponding value(s) from the listbox
            x = len(listbox.curselection())
            if x < 1 or x > 3:
                """NO GOOD"""
                window_title='Selection Error'
                msg_info = '\nPlease select at least one and up to three alignment stars.\n\n'
                ShowInfo_Dark(parent, window_title, msg_info)
                return

            #print('{} rows selected'.format(count))
            for i in listbox.curselection():
                tmp   = listbox.get(i)
                num   = tmp[1:4]
                beyer = tmp[6:13]
                name  = tmp[14:28]
                ra    = tmp[29:40]
                dec   = tmp[41:52]
                #junk  = tmp[53:]
                # print("# # # # # # # # # # # # ")
                # print(listbox.get(i))
                # print('- - - - - - - - - - - -')
                # FMT = '|{0:>3}|{1:<7}|{2:<15}|{3:>11}|{4:>11}|\n'
                # object=(FMT.format(num, beyer, name, ra, dec))
                # print( object )
                NStar_Align.RA_list.append(ra)
                NStar_Align.DE_list.append(dec)
                NStar_Align.Object_list.append(beyer+':'+name)
            # for loop

            # print(NStar_Align.RA_list)
            # print(NStar_Align.DE_list)
            # print(NStar_Align.Object_list)
            """activate and color the buttons"""
            self.button2["state"] = "normal"
            self.button3["state"] = "normal"
            self.button3["highlightbackground"] = 'green2'
            self.button3["highlightcolor"] = 'green2'
            self.pop.focus_set()
        # def selected_item


        x = parent.winfo_x()
        y = parent.winfo_y()
        _bg='gray19'
        _fg='tomato'
        self.pop = tk.Toplevel()
        self.saved_pop = self.pop
        self.pop.attributes('-topmost',True)
        self.pop.geometry("+%d+%d" % (x + 100, y + 200))
        self.pop.geometry('700x500')
        self.pop.focus_force()
        self.pop.grab_set() # make pop 'modal' (must click to dismiss)
        self.pop.title("n-Star Alignment")
        self.pop.config(bg=_bg, padx=3, pady=3)
        self.msg = tk.Message(self.pop, text="Choose up to 3 stars", bg=_bg, fg=_fg, width=690)
        self.msg.pack()
        self.msg = tk.Message(self.pop, text="(be sure to start at 'Home')", bg=_bg, fg=_fg, width=690, font=("TkDefaultFont", 10))
        self.msg.pack()


        '''choose One or Two or Three (put them into a List)'''
        self.objectframe = tk.Frame(self.pop)
        self.scroll_Y = tk.Scrollbar(self.objectframe, orient="vertical")
        self.celestial_objects = tk.Listbox(self.objectframe, selectmode='multiple', yscrollcommand=self.scroll_Y.set)

        self.celestial_objects.config(bg=_bg, fg=_fg,highlightcolor='black', selectbackground='brown3')
        self.celestial_objects.config(width=80, height=18, font=("Courier", 12) )
        self.scroll_Y.config(command=self.celestial_objects.yview)

        self.objectframe.pack()
        self.scroll_Y.pack(side='right', fill='y')
        self.celestial_objects.pack(expand=True, fill='both')

        lat = self.app_data["var_Lat"].get()
        lst = self.app_data["var_LST"].get()

        import align_stars
        valid_stars = align_stars.align_stars(lst, lat, heading=False)
        rows = valid_stars.splitlines()

        #insert each new 'row' at the end of celestial_objects
        for row in rows:
            self.celestial_objects.insert('end', row)

        self.celestial_objects.see(0) #go to the top

        self.bottomframe = tk.Frame(self.pop)
        self.bottomframe.pack( side = 'bottom' )

        self.button1 = tk.Button(self.bottomframe, text="Cancel", command=self.pop.destroy)
        self.button1.config(bg=_bg, fg=_fg, pady=4, activebackground='goldenrod1')
        self.button1.config(highlightbackground='goldenrod1')
        self.button1.config(highlightcolor='goldenrod1')
        self.button1.config(highlightthickness=2)
        self.button1.pack(side='left')

        self.button2 = tk.Button(self.bottomframe, text="Choose",  command=partial(selected_items, self, self.celestial_objects) )
        self.button2.config(bg=_bg, fg=_fg, pady=4, activebackground='red')
        self.button2.config(highlightbackground='green2')
        self.button2.config(highlightcolor='green2')
        self.button2.config(highlightthickness=2)
        self.button2.pack(side='left')
        #self.button2.bind("<Return>", selected_item(self, self.celestial_objects))

        self.button3 = tk.Button(self.bottomframe, text="continue", state="disabled", command=partial(NStar_Align.goto_stars, self, self.parent, self.controller) )
        self.button3.config(bg=_bg, fg=_fg, pady=4, activebackground='red')
        self.button3.config(highlightbackground='red')
        self.button3.config(highlightcolor='red')
        self.button3.config(highlightthickness=2)
        self.button3.pack(side='left')

        #self.pop.focus_set()
        self.button2.focus_set()
        self.parent.wait_window(self.pop)

        #self.celestial_objects.focus_set()



    def goto_stars(self, parent, controller):
        def __init__(self):
            self.parent = parent
            self.controller = controller

        # get rid of the previous pop-up
        self.saved_pop.destroy()

        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        # self.pop2 = tk.Toplevel()
        # self.saved_pop = self.pop2
        # #self.pop2.attributes('-topmost',True)
        # self.pop2.geometry("+%d+%d" % (x + 100, y + 200))
        # self.pop2.geometry('700x500')
        # self.pop2.grab_set() # make pop 'modal' (must click to dismiss)
        # self.pop2.title("Go-To")
        # _bg='gray19'
        # _fg='tomato'
        # self.pop2.config(bg=_bg, padx=3, pady=3)
        # self.msg = tk.Message(self.pop2, text="Slewing to Object", bg=_bg, fg=_fg, width=690)
        # self.msg.pack()

        window_title='n-Star Alignment'
        msg_info = '''
\nThe mount will now slew to each star.\n
\nPress "OK" when ready.'''
        answer = AskOkCancel_Dark(parent, window_title, msg_info)
        if answer is False:
            return
        num_stars = len(NStar_Align.Object_list)
        self.controller.scope.align(num_stars)

        num=0
        for item in NStar_Align.Object_list:
            #print('star {}: {} % {}'.format(num,NStar_Align.Object_list[num],object))
            #print('RA: {}  /  DEC: {}'.format(NStar_Align.RA_list[num], NStar_Align.DE_list[num]))
            object = NStar_Align.Object_list[num]
            RA = NStar_Align.RA_list[num]
            DEC = NStar_Align.DE_list[num]
            num+=1
            window_title='Star Alignment -- star {} of {}\ntarget: {} | {} | {}'.format(num,num_stars,object,RA,DEC)

            GoTo.do_goto(self, parent, controller, object, RA, DEC)

            msg_info = '''
When the slew completes, center the star carefully. Use a crosshair eyepiece.\n
Try to end the motions with the East and South buttons.\n
\nPress "OK" when done.'''
            answer = AskOkCancel_Dark(parent, window_title, msg_info)
            if answer is False:
                return

            ret = self.controller.scope.align_accept()

        window_title='n-Star Alignment'
        msg_info = '\nAlignment Completed\n\nPress "OK" to finish.'
        ShowInfo_Dark(parent, window_title, msg_info)
