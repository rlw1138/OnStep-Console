
from functools import partial
import logging
import tkinter as tk
from tkinter import messagebox

class GoTo:

    def do_goto(self, parent, controller, object, RA, DEC):
        '''
        moves the mount to a specific target in the sky

        '''
        def __init__(self, parent, controller):
            self.parent = parent
            self.controller = controller

        self.object=object
        self.ra=RA
        self.de=DEC
        # print(' Target: {} - {} {}'.format(self.object, str(self.ra), str(self.de)))

        from slew import Slew
        self.controller.scope.update_status()
        if self.controller.scope.is_parked:   Slew.un_park()
        self.parent.after(500, None) # give un_park half-a-sec to finish
        self.controller.scope.tracking_on() #SUCCESS == 1
        self.controller.app_data["var_IsTracking"].set(1)
        msg = "Started GO-TO: {} - {}  {}".format(self.object,self.ra,self.de)
        logging.info(msg) #to the logfile
        self.mount_type = self.controller.scope.slew_type
        self.controller.app_data["var_Slewing"].set("YES **")
        Slew.slew(self, parent, controller, self.mount_type, self.ra, self.de)
        #if not Slew.slew(self, parent, controller, type, ra, de):
            # oooops!
        #    return 1
        self.controller.app_data["var_GTobject"].set(self.object)
        self.controller.app_data["var_RA"].set(self.ra)
        self.controller.app_data["var_DEC"].set(self.de)

    #do_goto()
