"""
classes to change OnStep settings

these write values directly to the controller, rather than saving
into the "app_data["variable"]" first -- the 'update' loops in the
main program update the screen.

the methods from tkSimpleDialog are used here as well as by
the classes in messagebox_dark.py
"""

import tkinter as tk
import tkSimpleDialog #edited for OnStep 'style'
import conversion

_bg='gray19'
_fg='tomato'


class Location(tkSimpleDialog.Dialog):
    # Sites (locations) in the controller are numbered 0,1,2,3
    # Site Names are indexed with M, N, O, & P
    #
    # We retrieve both at start-up...into app_data[] tk.StringVars

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Site [{}] - {}".format(self.parent.app_data["var_SiteNum"].get(), self.parent.app_data["var_SiteName"].get())).grid(row=0, columnspan=2)

        tk.Label(parent, bg=_bg, fg=_fg, text="Site number, 1-4: ").grid(row=1)

        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e1.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        limit = int(self.e1.get())-1 # input 1-4, sites numbered 0-3
        #print(axis1, axis2) # or something
        self.parent.scope.set_site(limit)
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        limit, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        if limit < 1 or limit > 4:
            return False
        return True # valid inputs



class Overhead_Limit(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Overhead limit [{}]".format(self.parent.scope.get_overhead_limit())).grid(row=0, columnspan=2)
        tk.Label(parent, bg=_bg, fg=_fg, text="Degrees, 60-90: ").grid(row=1)
        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e1.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        limit = int(self.e1.get())
        #print(axis1, axis2) # or something
        self.parent.scope.set_overhead_limit(str(limit))
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        limit, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        if limit < 60 or limit > 90:
            return False
        return True # valid inputs



class Horizon_Limit(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Horizon limit [{}]".format( self.parent.scope.get_horizon_limit() ) ).grid(row=0, columnspan=2)
        tk.Label(parent, bg=_bg, fg=_fg, text="Degrees, ±30: ").grid(row=1)
        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e1.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        limit = int(self.e1.get())
        #print(axis1, axis2) # or something
        self.parent.scope.set_horizon_limit(str(limit))
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        limit, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        if limit < -30 or limit > 30:
            return False
        return True # valid inputs


class PastE_Limit(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Past East limit [{}]".format(self.parent.scope.get_degrees_past_E())).grid(row=0, columnspan=2)
        tk.Label(parent, bg=_bg, fg=_fg, text="Degrees, ±180: ").grid(row=1)
        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e1.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        limit = int(self.e1.get())
        #print(axis1, axis2) # or something
        self.parent.scope.set_degrees_past_E(str(limit))
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        limit, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        if limit < -180 or limit > 180:
            return False
        return True # valid inputs


class PastW_Limit(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Past West limit [{}]".format(self.parent.scope.get_degrees_past_W())).grid(row=0, columnspan=2)
        tk.Label(parent, bg=_bg, fg=_fg, text="Degrees, ±180: ").grid(row=1)
        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e1.grid(row=1, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        limit = int(self.e1.get())
        #print(axis1, axis2) # or something
        self.parent.scope.set_degrees_past_W(str(limit))
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        limit, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        if limit < -180 or limit > 180:
            return False
        return True # valid inputs


class Backlash_Settings(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Need BOTH entries, in arc-secs 0-3600").grid(row=0, columnspan=2)
        tk.Label(parent, bg=_bg, fg=_fg, text="R/A Backlash [{}] Axis 1: ".format(self.parent.scope.get_backlash(1))).grid(row=1)
        tk.Label(parent, bg=_bg, fg=_fg, text="DEC Backlash [{}] Axis 2: ".format(self.parent.scope.get_backlash(2))).grid(row=2)

        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')
        self.e2 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e2.config(highlightbackground=self._bg, highlightthickness=0)
        self.e2.config(insertbackground='goldenrod1')

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        axis1 = int(self.e1.get())
        axis2 = int(self.e2.get())
        #print(axis1, axis2) # or something
        self.parent.app_data["var_Backlash1"].set(axis1)
        self.parent.app_data["var_Backlash2"].set(axis2)
        self.parent.scope.set_backlash(1,axis1)
        self.parent.scope.set_backlash(2,axis2)
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        axis1, error_flag = conversion.str_to_int(self.e1.get())
        if error_flag:
            return False
        axis2, error_flag = conversion.str_to_int(self.e2.get())
        if error_flag:
            return False
        if axis1 < 0 or axis1 > 3600 or axis2 < 0 or axis2 > 3600:
            return False
        return True # valid inputs





class Coordinates_Settings(tkSimpleDialog.Dialog):

    # this method overrides the one in the Dialog class
    def body(self, parent, title, text):

        tk.Label(parent, bg=_bg, fg=_fg, text="Need BOTH entries, 00:00:00 / ±00*00:00").grid(row=0, columnspan=2)
        label_1 = tk.Label(parent, bg=_bg, fg=_fg, text="R/A : ")
        label_1.grid(row=1)
        label_2 = tk.Label(parent, bg=_bg, fg=_fg, text="DEC : ")
        label_2.grid(row=2)

        self.e1 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e1.insert(0, "{}".format(self.parent.scope.get_target_ra() ))
        self.e1.config(highlightbackground=self._bg, highlightthickness=0)
        self.e1.config(insertbackground='goldenrod1')

        self.e2 = tk.Entry(parent, bg=self._bg, fg=self._fg)
        self.e2.insert(0, "{}".format(self.parent.scope.get_target_de() ))
        self.e2.config(highlightbackground=self._bg, highlightthickness=0)
        self.e2.config(insertbackground='goldenrod1')

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        return self.e1 # initial focus


    # this method overrides the one in the Dialog class
    def apply(self):
        axis1 = self.e1.get()
        axis2 = self.e2.get()
        print('ax1: {} ax2: {}'.format(axis1, axis2))
        self.parent.app_data["var_TargetRA"].set(axis1)
        self.parent.app_data["var_TargetDEC"].set(axis2)
        self.parent.scope.set_target_ra(axis1)
        self.parent.scope.set_target_de(axis2)
        return None


    # this method overrides the one in the Dialog class
    def valid_input(self):
        box_1 = self.e1.get()
        box_2 = self.e2.get()
        if not box_1 or not box_2: return False
        ret_val = conversion.validate_hms(box_1)
        if isinstance(ret_val, (float, str )):
            ## if we get a float or string, r/a is good
            self.e1.delete(0, 'end')
            self.e1.insert(0, "{}".format( ret_val ))
            ## now chek dec
            ret_val = conversion.validate_dms(box_2)
            if isinstance(ret_val, (float, str )):
                self.e2.delete(0, 'end')
                self.e2.insert(0, "{}".format( ret_val ))
                return True # both are good
            else:
                return False
        else:
            return False
