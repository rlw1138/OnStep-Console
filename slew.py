'''

SLEWING, with error detect and status output

import slew
type = 'hor' (alt/az) or 'equ' (ra/dec)
axis1 = r/a or alt
axis2 = dec or az
slew.slew(type, axis1, axis2)

#[com dot hotmail @ rlw1138] -- 2020-APR-15
'''
import logging
import time
from datetime import datetime

class Slew:

    def abort(self, parent, controller):
        '''stops movement'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.stop()
        self.controller.scope.tracking_off()
        msg = "Movement Stopped"
        self.controller.DisplayWarning(msg)


    def home(self, parent, controller):
        '''go to the home position

        return codes:
        0 - returning home
        1 - already home
        2 - parked
        '''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        type = self.controller.scope.slew_type
        if self.controller.scope.is_home is True:
            msg=' Mount is already at Home'
            self.controller.DisplayWarning(msg)
            self.controller.app_data["var_GTobject"].set('')
            rc = 1
            return rc, msg
        elif self.controller.scope.is_parked is True:
            msg=' Mount is already Parked'
            self.controller.DisplayWarning(msg)
            self.controller.app_data["var_GTobject"].set('')
            rc = 2
            return rc, msg
        else:
            msg=' Returning to home postion'
            self.controller.DisplayWarning(msg)
            logging.info(f"Returning Home") #to the logfile
            # return-home command does not return a value
            self.controller.scope.return_home()
            self.controller.app_data["var_GTobject"].set('')
            rc = 0
            return rc, msg


    def reset_home(self, parent, controller):
        '''reset the home position'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        #print(' Reset Home will clear the corrective pointing model!')
        # self.controller.scope.reset_home() does not return a value
        self.controller.scope.reset_home()
        msg=' Home position reset -- re-Align recommended'
        self.controller.DisplayWarning(msg)
        logging.info(f"Home position reset") #to the logfile


    def park(self, parent, controller):
        '''go to the park position

        return codes:
        0 - parking
        1 - already parked
        2 - error
        '''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        if self.controller.scope.is_parked is True:
            self.controller.app_data["var_IsTracking"].set(0)
            msg = ' Mount is already parked'
            self.controller.DisplayWarning(msg)
            self.controller.app_data["var_GTobject"].set('')
            rc = 1
            return rc, msg
        else:
            #print(' Returning to Parked postion')
            if self.controller.scope.park(): # SUCCESS == 1
                self.controller.DisplayWarning("Parking")
                logging.info(f"Parking") #to the logfile
                self.controller.app_data["var_GTobject"].set('')
                rc = 0
                return rc, "Parking"
            else:
                msg=' ERROR: Park command failed'
                self.controller.DisplayError(msg)
                logging.error(msg.replace(' ERROR: ','')) #to the logfile
                rc = 2
                return rc, msg


    def un_park(self, parent, controller):
        '''allow leaving the park position'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        if self.controller.scope.is_parked is True:
            if self.controller.scope.un_park(): # SUCCESS == 1
                msg=' UN-Parked -- tracking ON'
                self.controller.DisplayWarning(msg)
                logging.info(f'UN-Parked -- tracking ON')
                self.controller.scope.tracking_on()  #SUCCESS == 1
                self.controller.app_data["var_IsTracking"].set(1)
                self.controller.app_data["var_GTobject"].set('')
            else:
                msg=' ERROR: Un-Park command failed'
                self.controller.DisplayError(msg)
                logging.error(f"Un-Park command failed")


    def set_park(self, parent, controller):
        '''set the park position'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        if self.controller.scope.set_park(): # SUCCESS == 1
            msg=' Park position reset'
            self.controller.DisplayWarning(msg)
            logging.info(f"Park position reset")
        else:
            msg=' ERROR: Reset Park command failed'
            self.controller.DisplayError(msg)
            logging.error(f"Reset-Park command failed")


    def toggle_tracking(self, parent, controller):
        '''tracking on and off

        errors:
        0 - success (on or off)
        1 - parked
        2 - cannot switch OFF
        3 - cannot switch ON
        '''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        if self.controller.scope.is_parked is True:
            msg = "Cannot turn on Tracking -- Mount is parked"
            self.controller.DisplayWarning(msg)
            self.controller.app_data["var_GTobject"].set('')
            rc = 1
            return rc, msg
        if self.controller.scope.is_tracking:
            if self.controller.scope.tracking_off(): #SUCCESS == 1
                self.controller.app_data["var_IsTracking"].set(0)
                msg=" Tracking switched 'off'"
                logging.info(msg)
                rc = 0
                return rc, msg
            else:
                msg=" ERROR: Tracking could not be switched 'off'"
                self.controller.DisplayError(msg)
                logging.error(msg.replace(' ERROR: ',''))
                rc = 2
                return rc, msg
        else:
            if self.controller.scope.tracking_on(): #SUCCESS == 1
                self.controller.app_data["var_IsTracking"].set(1)
                msg=" Tracking switched 'on'"
                logging.info(msg)
                rc = 0
                return rc, msg
            else:
                msg=" ERROR: Tracking could not be switched 'on'"
                self.controller.DisplayError(msg)
                logging.error(msg.replace(' ERROR: ',''))
                rc = 3
                return rc, msg


    def toggle_autoflip(self, parent, controller):
        '''automatic meridian flip on and off'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        if self.controller.scope.auto_flip is True:
            self.controller.scope.set_autoflip_off() # success == 1
            self.controller.app_data["var_AFlip_State"].set(0)
        else:
            self.controller.scope.set_autoflip_on()
            self.controller.app_data["var_AFlip_State"].set(1)


    def toggle_pauseHome(self, parent, controller):
        '''automatic meridian flip pause-at-home on and off'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        self.controller.scope.update_status()
        if self.controller.scope.pause_at_home is True:
            self.controller.scope.set_aflip_pause_off() # success == 1
            self.controller.app_data["var_Pause_State"].set(0)
        else:
            self.controller.scope.set_aflip_pause_on()
            self.controller.app_data["var_Pause_State"].set(1)


    def flip_now(self, parent, controller, type):
        '''do a meridian flip if possible'''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        rc, text = self.controller.scope.flip_now()
        if rc != '0': # SUCCESS == ZERO!
            msg=' ERROR: Meridian-flip failed: rc: {} - {}'.format(rc, text)
            self.controller.DisplayError(msg)
            logging.error(msg.replace(' ERROR: ','')) #to the logfile
            return rc, msg
        else:
            slew_end = False
            msg = ' Starting Meridian flip'
            self.controller.DisplayWarning(msg)
            logging.info(msg) #to the logfile
            # time.sleep(2)
            # msg = ' flip: rc({}) - {}'.format(rc,text)
            # self.controller.DisplayWarning(msg)



    '''
    I thought about having slew() use the mount type that's
    stored in the OnStep controller, or at least compare the
    saved type to the one that's passed-in as a param,
    because that makes sense, right?

    Then I remembered that stress_test() uses Alt/Az params
    even on an EQU mount

    So....
    '''

    def slew(self, parent, controller, type, axis1, axis2):
        '''do the actual slewing motion

        errors:
            0 - success
            1 - Error turning tracking on
            2 - ALT must be signed +/-
            3 - Error setting target ALT or R/A
            4 - AZ must be 3 digits
            5 - Error setting target AZ or DEC
            6 - SLEW FAILED
            7 -

        '''

        def __init__(self, parent, controller, *args, **kwargs):
            self.parent = parent
            self.controller = controller

        rc = self.controller.scope.tracking_on()
        # if rc == '0': # SUCCESS == 1
        #     msg = 'Error turning tracking on'
        #     self.controller.DisplayError(msg)
        #     rc = 1
        #     return rc, msg

        self.type = type.lower()
        self.controller.scope.update_status()
        #saved_type = self.controller.scope.slew_type.lower()
        #if saved_type != type:
        #    print('SLEW: parameter "type" [{}] does not match saved mount type [{}]'.format(type, saved_type))
        #    return False

        if self.type == 'hor' or self.type == 'altaz':
            # check for 'Signed' Altitude
            if axis1[0] != '+' and axis1[0] != '-':
                msg = 'Error: ALT must be signed +/-'
                rc = 2
                return rc, msg

            rc = self.controller.scope.set_target_alt(axis1)
            if rc == '0': # SUCCESS == 1
                msg = 'Error setting target ALT: ' + axis1
                rc = 3
                return rc, msg

            # check Azimuth for 3-digit degrees
            if (len(axis2) > 3 and axis2[3] != ':') or len(axis2) < 3:
                msg = 'Error: AZ must be 3 digits'
                rc = 4
                return rc, msg

            rc = self.controller.scope.set_target_azm(axis2)
            if rc == '0': # SUCCESS == 1
                msg = 'Error setting target AZ: ' + axis2
                rc = 5
                return rc, msg

            rc, msg = self.controller.scope.slew_hor()

            if rc != '0': # SUCCESS == ZERO!
                text = 'ERROR: Slew to Alt: {} Az: {} failed: rc: {}: {}'.format(axis1, axis2, rc, msg)
                logging.error(text.replace('ERROR: ','')) #to the logfile
                rc = 6
                return rc, text
            else:
                self.app_data["var_Slewing"].set( 'YES   <--' )
                text = 'Slewing to Alt: {} Az: {}'.format(axis1, axis2)
                logging.info(text)
                rc = 0
                return rc, text

        else:
            self.type == 'equ' # force equatorial, until we TO-DO: figure out what "fork alternate" means!
            #                         it's probably "alt-az fork on a wedge....."

            rc = self.controller.scope.set_target_ra(axis1)
            if rc == '0': # SUCCESS == 1
                msg = 'Error setting target R/A: ' + axis1
                rc = 3
                return rc, msg

            rc = self.controller.scope.set_target_de(axis2)
            if rc == '0': # SUCCESS == 1
                msg = 'Error setting target DEC: ' + axis2
                rc = 5
                return rc, msg

            rc, msg = self.controller.scope.slew_equ()
            if rc != '0': # SUCCESS == ZERO!
                text = 'ERROR: Slew to R/A: {} DEC: {} failed: rc: {}: {}'.format(axis1, axis2, rc, msg)
                logging.error(text.replace('ERROR: ','')) #to the logfile
                rc = 6
                return rc, text
            else:
                self.app_data["var_Slewing"].set( 'YES   <--' )
                text = 'Slewing to R/A: {} DEC: {}'.format(axis1, axis2)
                logging.info(text)
                return rc, text
