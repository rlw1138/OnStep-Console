""" Go-To Data / datafile selection and import / go-to an object """
import sys
import os
sys.path.append(os.getcwd())
from functools import partial
import glob
import logging
import conversion
import tkinter as tk
from go_to import GoTo

class ObjectData:

    """ these three global lists are built-up as the 'celestial_objects'
        Listboxes are created
    """
    RA_list = list()
    DE_list = list()
    object_list = list()


    def choose_DataSource(self, parent, controller, source):
        '''pick the source of celestial object data, (file or catalog)'''

        def __init__(self):
            self.parent = parent
            self.controller = controller

        def selected_item(self, listbox):
            # Traverse the tuple returned by curselection method and print
            # corresponding value(s) from the listbox
            for i in listbox.curselection():
                # print("# # # # # # # # # # # # ")
                # print(listbox.get(i))
                # print("# # # # # # # # # # # # ")
                self.controller.app_data["var_DataSource"].set(listbox.get(i))
                self.controller.app_data["var_RowNum"].set(i)
            self.button2["state"] = "normal"
            self.button2["highlightbackground"] = 'green2'
            self.button2["highlightcolor"] = 'green2'
            self.button3["state"] = "normal"
            self.button3["highlightbackground"] = 'green2'
            self.button3["highlightcolor"] = 'green2'
            self.pop.focus_set()
        # selected_item

        self.source = source # FILE or USER
        x = parent.winfo_x()
        y = parent.winfo_y()
        _bg='gray19'
        _fg='tomato'
        self.pop = tk.Toplevel()
        self.saved_pop = self.pop
        self.pop.attributes('-topmost',True)
        self.pop.geometry("+%d+%d" % (x + 100, y + 200))
        self.pop.geometry('500x500')
        self.pop.focus_force()
        self.pop.grab_set() # make pop 'modal' (must click to dismiss)
        self.pop.title("Go-To")
        self.pop.config(bg=_bg, padx=3, pady=3)
        """ V V V V V V V  DATASOURCE HEADING  V V V V V V V V V V V """
        if self.source == "FILE":
            self.msg = tk.Message(self.pop, text="Choose Object Datafile", bg=_bg, fg=_fg, width=490)

            '''works on Linux'''
            SOURCE_DIR = "./data"
            SUFFIX = "*.py"
            DATA_SOURCE = SOURCE_DIR + "/" + SUFFIX
            FILES = glob.glob(DATA_SOURCE)
        else:
            self.msg = tk.Message(self.pop, text="Choose User Star Catalog", bg=_bg, fg=_fg, width=490)
            self.msg.pack() # side='top' is default

            text='Use the OnStep webpage to upload object data -- '+self.controller.scope.user_space()+' entries available'
            self.msg = tk.Message(self.pop, text=text, bg=_bg, fg=_fg, width=490)
            self.msg.config( font=("TkDefaultFont", 10) )
        self.msg.pack() # side='top' is default
        """ x x x x x x x DATASOURCE HEADING x x x x x x x x x x x x """

        self.frm_datasource = tk.Frame(self.pop)
        self.scroll_Y = tk.Scrollbar(self.frm_datasource, orient="vertical")
        self.lb_datasource = tk.Listbox(self.frm_datasource, selectmode='single', yscrollcommand=self.scroll_Y.set)

        self.scroll_Y.config(command=self.lb_datasource.yview)
        self.lb_datasource.config(bg=_bg, fg=_fg, highlightcolor='black', selectbackground='brown3')
        self.lb_datasource.config(width=50, height=18, font=("Courier", 12) )

        self.frm_datasource.pack()
        self.scroll_Y.pack(side='right', fill='y')
        self.lb_datasource.pack(expand=True, fill='both')
        """ V V V V V V V  DATASOURCE INSERT  V V V V V V V V V V V """
        if self.source == "FILE":
            x=0
            for full_path in FILES:
                x+=1
                filename=os.path.basename(full_path).replace('.py', '')
                self.lb_datasource.insert(x, filename)
        else:
            prev_name = ''
            cat_num = 0
            self.controller.scope.get_catalog(0)
            for num in range(0,15):
                '''
                    ONLY 0 - 6 ARE USER-DEFINED, 7 - 14 ARE RESERVED
                    should probs do something about that.....
                    To-Do: something about that
                '''
                self.controller.scope.get_catalog(num)
                self.controller.scope.move_catName()
                name, object_type = self.controller.scope.get_itemID()

                if name != '':
                    if name != prev_name:
                        cat_num += 1
                        self.lb_datasource.insert(cat_num, name)
                        prev_name = name
                else:
                    if num == 0:
                        self.lb_datasource.insert(tk.END,'no catalogs to display')
                        break
                    else:
                        # print(SPC + 'no more catalogs to display')
                        break
            #loop
        """ x x x x x x x DATASOURCE INSERT x x x x x x x x x x x x """

        #self.lb_datasource.activate(3)
        self.lb_datasource.see(0)

        self.bottomframe = tk.Frame(self.pop)
        self.bottomframe.pack( side = 'bottom' )

        self.button1 = tk.Button(self.bottomframe, text="Cancel", command=self.pop.destroy)
        self.button1.config(bg=_bg, fg=_fg, pady=4, activebackground='goldenrod1')
        self.button1.config(highlightbackground='goldenrod1')
        self.button1.config(highlightcolor='goldenrod1')
        self.button1.config(highlightthickness=2)
        self.button1.pack(side='left')

        self.button2 = tk.Button(self.bottomframe, text="Load Data", command=partial(selected_item, self, self.lb_datasource) )
        self.button2.config(bg=_bg, fg=_fg, pady=4, activebackground='red')
        self.button2.config(highlightbackground='green2')
        self.button2.config(highlightcolor='green2')
        self.button2.config(highlightthickness=2)
        self.button2.pack(side='left')

        self.button3 = tk.Button(self.bottomframe, text="continue", state="disabled", command=partial(ObjectData.import_data, self, self.parent, self.controller, self.source) )
        self.button3.config(bg=_bg, fg=_fg, pady=4, activebackground='red')
        self.button3.config(highlightbackground='red')
        self.button3.config(highlightcolor='red')
        self.button3.config(highlightthickness=2)
        self.button3.pack(side='left')

        self.pop.focus_set()
        self.button2.focus_set()
        self.parent.wait_window(self.pop)

    #def choose_DataFile()

    """ # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # """
    """ # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # """

    def import_data(self, parent, controller, source):
        '''import the data from the chosen source'''

        def __init__(self, parent, controller):
            self.parent = parent
            self.controller = controller

        def get_col_names(self, x, col, num_cols):
            '''assigns field names based on content type'''
            self.col_type = str(type(col))
            if self.col_type.find('float') > 0 and x < (num_cols-2):
                # float type, but not the last two cols
                exec('col'+str(x)+' = "mag"')
            elif x == num_cols-2 and (self.col_type.find('float') > 0 or self.col_type.find('str') > 0):
                # Next-to-Last Col AND either float or string
                exec('col'+str(x)+' = "ra"')
            elif x == num_cols-1 and (self.col_type.find('float') > 0 or self.col_type.find('str') > 0) :
                # Last Col AND either float or string
                exec('col'+str(x)+' = "dec"')
            else:
                # every other kind gets "name0", "name1", etc
                exec('col'+str(x)+' = "name'+str(x)+'"')
            self.col_name = eval('col'+str(x))
            return self.col_name
        # get_col_names():

        def selected_item(self, listbox):
            # Traverse the tuple returned by curselection method and print
            # corresponding value(s) from the listbox
            for i in listbox.curselection():
                # print("# # # # # # # # # # # # ")
                # print(listbox.get(i))
                # print("# # # # # # # # # # # # ")
                '''store the index number in RowNum'''
                self.controller.app_data["var_RowNum"].set(i)
                self.pop2.focus_set()
                ra = ObjectData.RA_list[i]
                de = ObjectData.DE_list[i]
                object=ObjectData.object_list[i]
                self.controller.app_data["var_GTobject"].set(object)
                self.controller.app_data["var_RA"].set(ra)
                self.controller.app_data["var_DEC"].set(de)
                self.controller.app_data["var_TargetRA"].set(ra)
                self.controller.app_data["var_TargetDEC"].set(de)

                # get rid of the previous pop-up
                self.saved_pop.destroy()

                GoTo.do_goto(self, self.parent, self.controller, object, ra, de)
                # ObjectData.do_goto(self, self.parent, self.controller, object, ra, de)

        # selected_item

        # get rid of the previous pop-up
        self.saved_pop.destroy()

        self.source = source
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.pop2 = tk.Toplevel()
        self.saved_pop = self.pop2
        self.pop2.attributes('-topmost',True)
        self.pop2.geometry("+%d+%d" % (x + 100, y + 200))
        self.pop2.geometry('700x500')
        self.pop2.grab_set() # make pop 'modal' (must click to dismiss)
        self.pop2.title("Go-To")
        _bg='gray19'
        _fg='tomato'
        self.pop2.config(bg=_bg, padx=3, pady=3)
        self.msg = tk.Message(self.pop2, text="Choose Object for go-to", bg=_bg, fg=_fg, width=690)
        self.msg.pack()

        if self.source == "FILE":
            """ V V V V V V V  DATAFILE PROCESSING V V V V V V V V V V V V """
            #print('var_DataSource:'+str(self.controller.app_data["var_DataSource"].get())+':')
            datafile = 'data.'+str(self.controller.app_data["var_DataSource"].get())
            '''print('IMPORTING DATA FROM: '+datafile)'''
            import importlib
            self.OBJECTDATA = importlib.import_module(datafile)
            self.TotalRows = len( self.OBJECTDATA.stars )
            '''print('data has '+str( self.TotalRows )+' rows (objects)')'''

            row = self.OBJECTDATA.stars[0]
            self.NumCols = len(row)

            # self.msg2 = tk.Message(self.pop2, text='example row: {}'.format(str(row)), width=590)
            # self.msg2.config(bg=_bg, fg=_fg, font=("Helvetica", 12))
            # self.msg2.pack()

            col_names = list() #an empty list
            for x in range(0, self.NumCols):
                #col_names will contain a name for each col, based on data type
                col_names.append(get_col_names(self, x, row[x], self.NumCols))

            # self.msg3 = tk.Message(self.pop2, text='columns will be named: {}'.format(col_names), width=590)
            # self.msg3.config(bg=_bg, fg=_fg, font=("Helvetica", 12))
            # self.msg3.pack()

            if self.NumCols == 5 :
                # num, name0, name1, mag, ra, dec
                FMT = "{0:>3}) {1:<8} {2:<18} !{3:7.2f}! {4:>8} {5:>9}"
            elif self.NumCols == 4 and col_names[1] == 'mag':
                # num, name, mag, ra, dec
                FMT = "{0:>3}) {1:<26} ^{2:7.2f}^ {3:>8} {4:>9}"
            elif self.NumCols == 4 and col_names[1] != 'mag':
                # num, name, object_type, ra, dec
                FMT = "{0:>3}) {1:<16} ~{2:<3}~ {3:>8} {4:>9}"
            elif self.NumCols == 3:
                # num, name, ra, dec
                FMT = "{0:>3}) {1:<16} {2:>8} {3:>9}"
            else:
                FMT='\n\nUNANTICIPATED DATAFILE FORMAT\n\n -- cannot proceed --'
                print(FMT)
                return
            """ X X X X X X X  DATAFILE PROCESSING X X X X X X X X X X X X """
        else: # self.source == "USER" # user-defined list stored in OnStep
            """ X X X X X X NO DATAFILE PROCESSING NEEDED  X X X X X X X X """
            pass

        self.objectframe = tk.Frame(self.pop2)
        self.scroll_Y = tk.Scrollbar(self.objectframe, orient="vertical")
        self.celestial_objects = tk.Listbox(self.objectframe, selectmode='single', yscrollcommand=self.scroll_Y.set)

        self.celestial_objects.config(bg=_bg, fg=_fg,highlightcolor='black', selectbackground='brown3')
        self.celestial_objects.config(width=80, height=18, font=("Courier", 12) )
        self.scroll_Y.config(command=self.celestial_objects.yview)

        self.objectframe.pack()
        self.scroll_Y.pack(side='right', fill='y')
        self.celestial_objects.pack(expand=True, fill='both')
        """ V V V V V V V  CELESTIAL OBJECTS INSERT  V V V V V V V V V V """
        if self.source == "FILE":
            num = 0
            for row in self.OBJECTDATA.stars:
                num += 1 #                        row number will be 'num minus one'
                if num <= self.TotalRows:
                    if self.NumCols == 5:
                        object=(FMT.format(num, row[0], row[1], float(row[2]), row[3], row[4]))
                    elif self.NumCols == 4 and col_names[1] == 'mag':
                        object=(FMT.format(num, row[0], float(row[1]), row[2], row[3]))
                    elif self.NumCols == 4 and col_names[1] != 'mag':
                        object=(FMT.format(num, str(row[0]), row[1], row[2], row[3]))
                    elif self.NumCols == 3:
                        object=(FMT.format(num, row[0], row[1], row[2]))
                self.celestial_objects.insert(num, object)
                ''' convert floating-point R/A DEC to hh:mm:ss if needed '''
                ra = row[self.NumCols - 2]
                if isinstance(ra, float):
                    ra = str(conversion.float_To_hms(ra, 'PRECISION_HIGH')).replace('+', '').replace('-', '')
                de = row[self.NumCols - 1]
                if isinstance(de, float):
                    de = str(conversion.float_To_hms(de, 'PRECISION_HIGH'))
                object = str(row[0])
                if self.NumCols == 5:
                    object += " "
                    object += str(row[1])
                ObjectData.RA_list.append(ra)
                ObjectData.DE_list.append(de)
                ObjectData.object_list.append(object)
            # loop
        else: # self.source == "USER" # user-defined list stored in OnStep
            self.cat_num = self.controller.app_data["var_RowNum"].get()
            if self.controller.scope.get_catalog(self.cat_num):
                self.controller.scope.move_catName()
                catalog, object_type = self.controller.scope.get_itemID()
                for num in range(1,200):
                    self.controller.scope.move_objectNum(num)
                    name, object_type, ra, de = self.controller.scope.get_itemInfo()
                    if name != '':
                        object="{0:>3}) {1:<14}{2:^3} {3:>8} {4:>9}".format(num, name, object_type, ra, de)
                        self.celestial_objects.insert(num, object)
                        ObjectData.RA_list.append(ra)
                        ObjectData.DE_list.append(de)
                        ObjectData.object_list.append(name)
                        ## print(object)
                    else:
                        break
                #loop
            else:
                object='no objects in catalog ( '+str(self.cat_num)+' )'
                self.celestial_objects.insert(0, object)
                return
        """ X X X X X X X  CELESTIAL OBJECTS INSERT  X X X X X X X X X X """
        self.celestial_objects.see(0)

        self.bottomframe = tk.Frame(self.pop2)
        self.bottomframe.pack( side = 'bottom' )

        self.button4 = tk.Button(self.bottomframe, text="Cancel", command=self.pop2.destroy)
        self.button4.config(bg=_bg, fg=_fg, pady=4, activebackground='goldenrod1')
        self.button4.config(highlightbackground='goldenrod1')
        self.button4.config(highlightcolor='goldenrod1')
        self.button4.config(highlightthickness=2)
        self.button4.pack(side='left')

        self.button5 = tk.Button(self.bottomframe, text="Go-To Object",  command=partial(selected_item, self, self.celestial_objects) )
        self.button5.config(bg=_bg, fg=_fg, pady=4, activebackground='red')
        self.button5.config(highlightbackground='green2')
        self.button5.config(highlightcolor='green2')
        self.button5.config(highlightthickness=2)
        self.button5.pack(side='left')
        #self.button5.bind("<Return>", selected_item(self, self.celestial_objects))
        self.celestial_objects.focus_set()

    #import_UserList()

#class ObjectData:
