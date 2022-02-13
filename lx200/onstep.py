
''' interface to the OnStep LX200 command-set for controlling motorized
    telescope mounts
'''
'''
For testing / operating an OnStep telescope mount controller

python test scripts originally authored by Khalid Baheyeldin
[https://github.com/kbahey/onstep-python]

modified / tweaked / enhanced by me for my own use. USE AT YOUR OWN RISK
#[com dot hotmail @ rlw1138] -- 2020-APR-15


Functions that return 3 or more possible answers use
  Zero to indicate SUCCESS

Functions that return 2 possible use Zero (False) for failure and
  ONE (True) to indicate SUCCESS

'''

#     misc
#     ALIGNMENT
#     TRACKING
#     GO-TO / MOVEMENT
#     LIMITS / CORRECTIONS
#     DATE AND TIME
#     SITE (location) commands
#     LIBRARY FUNCTIONS -- see text at end-of-file



import lx200.tty
import lx200.sock
from datetime import datetime, timedelta as TimeDelta
import time

class onstep:
    '''
    interface to the OnStep LX200 command-set for controlling motorized
    telescope mounts
    '''

    def __init__(self, port = '', host = ''):
        # Check what mode we are in, serial USB or over TCP/IP
        if host == '' and port != '':
            self.scope = lx200.tty.tty(port=port)
            self.scope.open()
        else:
            if port.isnumeric():
                self.scope = lx200.sock.sock()
                self.scope.connect(host, int(port))
            else:
                raise NonNumericPort

        self.is_slewing = False
        self.is_tracking = False
        self.is_parked = None
        self.type = None
        self.slew_type = None
        self.position = None
        self.is_home = None
        self.pier_side = None
        self.auto_flip = None
        self.pause_at_home = None
        self.pec_recorded = False
        self.pec = None
        self.pps = False
        self.guide_rate = None

        self.max_backlash = 3600

        self.valid_dirs = ("n", "s", "e", "w") # must be lower

        self.valid_site = ("M", "N", "O", "P") # must be upper

        self.valid_types = 'UNK,OC,GC,PN,DN,SG,EG,IG,KNT,SNR,GAL,CN,STR,PLA,CMT,AST'

        self.slew_error = (
        'Goto is possible', # SUCCESS == 0
        'below horizon limit',
        'above overhead limit',
        'controller in standby',
        'mount is parked',
        'Goto in progress',
        'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)',
        'hardware fault',
        'already in motion',
        'unspecified error', )
    # end __init__


    '''
    Command length is limited to 40 chars,
    2 for the command frame ":#"
    + 2 for the code "CC"
    + max 36 for the parameter "P":
    ":CCPPP...#".
    Cr/Lf chars can be sent along with your command, but are ignored.

    '''
    def send_str(self, string):
        '''
        Send an arbitrary string
        '''
        self.scope.send(string)
        return self.scope.recv()



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     STATUS items

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    def dump_status(self):
        self.update_status()
        print('   Mount type: {}'.format(self.type))
        print('      Slewing: {}'.format(self.is_slewing))
        print('     Tracking: {}'.format(self.is_tracking))
        print('      Parking: {}'.format(self.is_parked))
        print('     Position: {}'.format(self.position))
        print('    Pier-side: {}'.format(self.pier_side))
        print('PEC Recorded?: {}'.format(self.pec_recorded))
        print('          PEC: {}'.format(self.pec))
        print('          PPS: {}'.format(self.pps))

    def update_status(self):
        '''
        refreshes all the status values
        '''
        #call this every time a status value is to be checked

        s = ""
        self.scope.send(':GU#')
        s = self.scope.recv()

        ''' [n]ot Tracking  [N]o Go-To '''
        if 'n' in s and 'N' in s:
            self.is_tracking = False # [n]ot Tracking
            self.is_slewing = False  # [N]o go-to

        if 'n' in s and not 'N' in s:
            self.is_tracking = False # [n]ot Tracking
            self.is_slewing = True

        if 'N' in s and not 'n' in s:
            self.is_slewing = False # [N]o go-to
            self.is_tracking = True

        if 'p' in s:
            self.is_parked = False
        if 'P' in s:
            self.is_parked = True
        if 'I' in s:
            self.is_parked = 'Parking...'
        if 'F' in s:
            self.is_parked = 'Park fail'

        if 'H' in s:
            self.is_home = True
        else:
            self.is_home = False

        if 'w' in s:
            self.position = 'Waiting at home' #during Flip
        else:
            self.position = ""

        if 'G' in s:
            self.guide = 'Guide pulse active'

        if 'S' in s:
            self.pps = True
        else:
            self.pps = False

        if 'R' in s:
            self.pec_recorded = True
        else:
            self.pec_recorded = False

        if '/' in s:
            self.pec = 'Ignore'
        if ',' in s:
            self.pec = 'Ready2Play'
        if '~' in s:
            self.pec = 'Playing'
        if ';' in s:
            self.pec = 'Ready2Record'
        if '^' in s:
            self.pec = 'Recording'

        if 'E' in s:
            self.type = 'Equatorial'
            self.slew_type = 'equ'    # GEM
        if 'K' in s:
            self.type = 'Fork (equ)'
            self.slew_type = 'equ'    # wedge-mounted
        if 'k' in s:
            self.type = 'Fork (Alt)'
            self.slew_type = 'hor'    # no wedge, alt/az style
        if 'A' in s:
            self.type = 'AltAz'
            self.slew_type = 'hor'    # up/down, left/right

        if 'a' in s:
            self.auto_flip = True
        else:
            self.auto_flip = False

        if 'u' in s:
            self.pause_at_home = True #during auto-flip
        else:
            self.pause_at_home = False

        if 'o' in s:
            self.pier_side = 'None'
        if 'T' in s:
            self.pier_side = 'East'
        if 'W' in s:
            self.pier_side = 'West'

        if '0' in s:
            #the rate number is always last, ends with zero, followed by '#'
            f = s[-4:-1]
            self.guide_rate = f
            ## 110(1/2xVSlow) 220(1xSlow) 230(2x) 240(4x) 250(8xCenter) 260(20xFind) 270(48xFast) 280(1/2Max)

    def status_bitpacked(self):
        '''
        receives a number of byte objects, assumed to
        represent bit-packed data
        '''
        self.scope.send(':Gu#')
        s = self.scope.recv_raw()
        return s # returns 9 hex bytes
    ##  b'\x82\x84\xb8\xa1\x80\x80\x82\x86\x80#'
    #   EXAMPLE:
    ##    t_rate = config.scope.status_bitpacked()
    ##    tmp = bytearray(t_rate)
    ##    s = tmp[1] & 127
    #   yields an int 's' == 0 | 1 | 2 | 3

    #see Command.ino in the OnStep Arduino source code



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     miscellaneous

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

        # TODO provide last error message
        # :GE#
    def get_last_error(self):
        '''
        returns the last error number code
        '''
        self.scope.send(':GE#')
        return self.scope.recv().replace('#', '')

    ''' // ------------------------- MountStatus -------------------------
        // general (background) errors
        #define L_GE_NONE "None"
        #define L_GE_MOTOR_FAULT "Motor/driver fault"
        #define L_GE_ALT_MIN "Below horizon limit"
        #define L_GE_LIMIT_SENSE "Limit sense"
        #define L_GE_DEC "Dec limit exceeded"
        #define L_GE_AZM "Azm limit exceeded"
        #define L_GE_UNDER_POLE "Under pole limit exceeded"
        #define L_GE_MERIDIAN "Meridian limit exceeded"
        #define L_GE_SYNC "Sync safety limit exceeded"
        #define L_GE_PARK "Park failed"
        #define L_GE_GOTO_SYNC "Goto sync failed"
        #define L_GE_UNSPECIFIED "Unknown error"
        #define L_GE_ALT_MAX "Above overhead limit"
        #define L_GE_WEATHER_INIT "Weather sensor init failed"
        #define L_GE_SITE_INIT "Time or Location not updated"
        #define L_GE_OTHER "Unknown Error, code"
        // command errors
        #define L_CE_NONE "No Errors"
        #define L_CE_0 "Reply 0"
        #define L_CE_CMD_UNKNOWN "command unknown"
        #define L_CE_REPLY_UNKNOWN "invalid reply"
        #define L_CE_PARAM_RANGE "parameter out of range"
        #define L_CE_PARAM_FORM "bad parameter format"
        #define L_CE_ALIGN_FAIL "align failed"
        #define L_CE_ALIGN_NOT_ACTIVE "align not active"
        #define L_CE_NOT_PARKED_OR_AT_HOME "not parked or at home"
        #define L_CE_PARKED "already parked"
        #define L_CE_PARK_FAILED "park failed"
        #define L_CE_NOT_PARKED "not parked"
        #define L_CE_NO_PARK_POSITION_SET "no park position set"
        #define L_CE_GOTO_FAIL "goto failed"
        #define L_CE_LIBRARY_FULL "library full"
        #define L_CE_GOTO_ERR_BELOW_HORIZON "goto below horizon"
        #define L_CE_GOTO_ERR_ABOVE_OVERHEAD "goto above overhead"
        #define L_CE_SLEW_ERR_IN_STANDBY "slew in standby"
        #define L_CE_SLEW_ERR_IN_PARK "slew in park"
        #define L_CE_GOTO_ERR_GOTO "already in goto"
        #define L_CE_GOTO_ERR_OUTSIDE_LIMITS "goto outside limits"
        #define L_CE_SLEW_ERR_HARDWARE_FAULT "hardware fault"
        #define L_CE_MOUNT_IN_MOTION "mount in motion"
        #define L_CE_GOTO_ERR_UNSPECIFIED "other"
        #define L_CE_UNK "unknown"
    '''

    def get_version(self):
        '''
        Get OnStep version
        '''
        self.scope.send(':GVN#')
        return self.scope.recv().replace('#', '')



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     ALIGNMENT

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    def align(self, num_stars = 1):
        '''
        // :A[n]#     Start Telescope Manual Alignment Sequence
        //            This is to initiate a n-star alignment for 1..MAX_NUM_ALIGN_STARS:
        //            1) Before calling this function, the telescope should be in the polar-home position
        //            2) Call this function with the # of align stars you'd like to use
        //            3) Set the target location (RA/Dec) to a bright star, etc. (not too near the NCP/SCP)
        //            4) Issue a goto command
        //            5) Center the star/object using the guide commands (as needed)
        //            6) Call :A+# command to accept the correction
        //            ( for two+ star alignment )
        //            7) Back to #3 above until done, except where possible choose at least one star on both meridian sides
        //            Return: 0 on failure
        //                    1 on success
        // set current time and date before calling this routine

        // telescope should be set in the polar home (CWD) for a starting point
        // this command sets indexAxis1, indexAxis2, azmCor, altCor = 0 ;
        '''
        self.scope.send(':A' + str(num_stars) + '#')
        return self.scope.recv()

    def align_accept(self):
        '''
        // :A+#       Align accept target location
        '''
        self.scope.send(':A+#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def align_write(self):
        '''
        // :AW#       Align Write to EEPROM
        '''
        self.scope.send(':AW#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1


    def get_align_status(self):
        '''
        // :A?#       Align status
        '''
        # see also: 'get_mount_status' -- :GW# command
        self.scope.send(':A?#')
        return self.scope.recv().replace('#', '')
        # Returns: mno
        # where m is the maximum number of alignment stars
        #       n is the current alignment star (0 otherwise)
        #       o is the last required alignment star when an alignment is in progress (0 otherwise)



    def get_mount_status(self):
        '''
        mount's alignment status
        '''
        # see also: 'get_align_status' -- :A?# command
        self.scope.send(':GW#')
        return self.scope.recv().replace('#', '')
        # Returns: [mount][tracking][alignment]
        # Where mount: A-AltAzm, P-Fork, G-GEM
        #       tracking: T-tracking, N-not tracking
        #       alignment: 0-needs alignment, 1-one star aligned, 2-two star aligned, >= 3-three star aligned

    def sync2target(self):
        '''
        sync current scope position with current target r/a and dec
        '''
        self.update_status()
        # Sync only if the scope is tracking
        if self.is_tracking == True:
            self.scope.send(':CS#')
        # no return

    def sync2object(self):
        '''
        sync current scope position with the current database object
        '''
        self.update_status()
        # Sync only if the scope is tracking
        if self.is_tracking == True:
            self.scope.send(':CM#')
        # no return



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     TRACKING

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# tracking is also activated by 'un-park' as well as 'slew_***'

    def tracking_on(self):
        '''
        Turn on tracking
        '''
        self.scope.send(':Te#')
        return self.scope.recv() # SUCCESS == 1

    def tracking_off(self):
        '''
        Turn off tracking
        '''
        self.scope.send(':Td#')
        return self.scope.recv() # SUCCESS == 1

    def tracking_sidereal(self):
        '''
        DEFAULT (power-up) RATE
        '''
        self.scope.send(':TQ#')
        # no return

    def tracking_solar(self):
        self.scope.send(':TS#')
        # no return

    def tracking_lunar(self):
        self.scope.send(':TL#')
        # no return

    def tracking_king(self):
        '''
        King Rate, compensates for refraction near the horizon
        '''
        self.scope.send(':TK#')
        # no return



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     GO-TO / MOVEMENT

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    ##def get_target_alt(self):
    #    #there isn't one!
    # it *would have* been :Ga#, but that conflicts with
    # "Get Local Time in 12 hour format"

    def set_target_alt(self, alt):
        self.scope.send(':Sa' + alt + '#')
        return self.scope.recv() # SUCCESS == 1

    def get_alt(self):
        '''
        get altitude of telescope
        '''
        self.update_status()
        self.scope.send(':GA#')
        return self.scope.recv().replace('#', '')

    ##def get_target_azm(self):
    #    #there isn't one!

    def set_target_azm(self, azm):
        self.scope.send(':Sz' + azm + '#')
        return self.scope.recv() # SUCCESS == 1

    def get_azm(self):
        '''
        get azimuth of telescope
        '''
        self.update_status()
        self.scope.send(':GZ#')
        return self.scope.recv().replace('#', '')

    def get_target_ra(self):
        self.update_status()
        self.scope.send(':Gr#')
        return self.scope.recv().replace('#', '')

    def set_target_ra(self, ra):
        self.scope.send(':Sr' + ra + '#')
        return self.scope.recv() # SUCCESS == 1

    def get_ra(self):
        '''
        Get Telescope Right Ascension
        '''
        self.update_status()
        self.scope.send(':GR#')
        return self.scope.recv().replace('#', '')

    def get_target_de(self):
        self.update_status()
        self.scope.send(':Gd#')
        return self.scope.recv().replace('#', '')

    def set_target_de(self, de):
        self.scope.send(':Sd' + de + '#')
        return self.scope.recv() # SUCCESS == 1

    def get_de(self):
        '''
        Get Telescope Declination
        '''
        self.update_status()
        self.scope.send(':GD#')
        return self.scope.recv().replace('#', '')


## :RG#       Set slew rate to Guiding Rate   1X
## :RC#       Set slew rate to Centering rate 8X
## :RM#       Set slew rate to Find Rate     20X
## :RF#       Set slew rate to Fast Rate     48X
## :RS#       Set slew rate to Half Max (VF)  ?X (1/2 of maxRate)
## :Rn#       Set slew rate to n, where n = 0..9
##            Returns: Nothing
    def set_speed(self, speed = '20x'):
        if     speed == '0.25x':
            s = '0'
        elif speed == '0.5x':
            s = '1'
        elif speed == '1x':
            s = 'G'
        elif speed == '2x':
            s = '3'
        elif speed == '4x':
            s = '4'
        elif speed == '8x':
            s = 'C'
        elif speed == '20x':
            s = 'M'
        elif speed == '48x':
            s = '7'
        elif speed == 'half':
            s = 'S'
        elif speed == 'max':
            s = '9'
        else:
            return False
        self.scope.send(':R' + s + '#')
        return True


    def get_max_slew(self):
        '''
        get MaxRate (current)
        '''
        self.scope.send(':GX92#')
        return self.scope.recv().replace('#', '')

    def get_max_base(self):
        '''
        get maxRateBaseActual (default)
        '''
        self.scope.send(':GX93#')
        return self.scope.recv().replace('#', '')


    def get_slew_speed_max(self):
        '''
        get slew speed

        ## degrees-per-second
        ## SLEW_RATE_BASE_DESIRED
        '''
        self.scope.send(':GX97#')
        return self.scope.recv().replace('#', '')


    def set_slew_rate(self, speed):
        '''
        set slew speed

        ??? what are the speeds ???

        '''
        self.scope.send(':SX92,'+speed+'#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1


    def set_slew_speed_max(self, speed):
        '''
        set slew speed

        ## SLEW_RATE_BASE_DESIRED
        '''
        if speed < '1': speed='1'
        if speed > '5': speed='5'
        self.scope.send(':SX93,'+speed+'#')
        #no return
# //:SX93,5-1# Set slew rate Max / 1=200% 150%, 100%, 75%, 5=50%





    def stop(self):
        '''
        Stop all motor movement
        '''
        self.scope.send(':Q#')
        #no return



## :Me# :Mw#  Move Telescope East or West at current slew rate
## :Mn# :Ms#  Move Telescope North or South at current slew rate
##            Controller Returns: Nothing
    def move(self, direction = ''):
        direction = direction.lower()
        if direction in self.valid_dirs :
            self.scope.send(':M' + direction + '#')
            return True
        else:
            return False

#    def move(self, direction = ''):
#        # Move in a certain direction
#        if direction.Lower() == 'n' or direction.Lower() == 's' or direction.Lower() == 'w' or direction.Lower() == 'e':
#            self.scope.send(':M' + direction + '#')
#            return True
#        else:
#            return False

## :Qn# Qs#   Halt north/south Slews
## :Qe# Qw#   Halt east/westward Slews
##            Controller Returns: Nothing
    def halt(self, direction = ''):
        direction = direction.lower()
        if direction in self.valid_dirs :
            self.scope.send(':Q' + direction + '#')
            return True
        else:
            return False


# SLEWING

        # if rc == '0':
        #     return rc, 'Goto is possible' # SUCCESS
        # elif rc == '1':
        #     return rc, 'below the horizon limit'
        # elif rc == '2':
        #     return rc, 'above overhead limit'
        # elif rc == '3':
        #     return rc, 'controller in standby'
        # elif rc == '4':
        #     return rc, 'mount is parked'
        # elif rc == '5':
        #     return rc, 'Goto in progress'
        # elif rc == '6':
        #     return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
        # elif rc == '7':
        #     return rc, 'hardware fault'
        # elif rc == '8':
        #     return rc, 'already in motion'
        # else:
        #     return rc, 'unspecified error'

    def slew_equ(self):
        '''
        Slew to pre-set target RA and DEC
        '''
        self.scope.send(':MS#')
        rc = int(self.scope.recv())
        if rc < 0 or rc > 8 : rc = 9
        return str(rc), self.slew_error[rc]

    def slew_hor(self):
        '''
        Slew to pre-set target Alt and Azm
        '''
        self.scope.send(':MA#')
        rc = int(self.scope.recv())
        if rc < 0 or rc > 8 : rc = 9
        return str(rc), self.slew_error[rc]

    def slew_polar(self):
        '''
        Slew to OnStep's assumed position (target RA
        and DEC) -- for polar alignment refinement
        '''
        self.scope.send(':MP#')
        rc = int(self.scope.recv())
        if rc < 0 or rc > 8 : rc = 9
        return str(rc), self.slew_error[rc]


# MERIDIAN STUFF
    def flip_now(self):
        '''
        Slew to current target RA and DEC, but scope EAST of
        # pier, (subject to meridian overlap for GEM mounts)
        '''
        self.scope.send(':MN#')
        rc = int(self.scope.recv())
        if rc < 0 or rc > 8 : rc = 9
        return str(rc), self.slew_error[rc]

    def set_autoflip_off(self):
        '''
        auto meridian flip OFF
        '''
        self.scope.send(':SX95,0#')
        return self.scope.recv() # SUCCESS == 1

    def set_autoflip_on(self):
        '''
        auto meridian flip ON
        '''
        self.scope.send(':SX95,1#')
        return self.scope.recv() # SUCCESS == 1

    def get_pier_side(self):
        '''
        Returns: E#, W#, N# (none/parked), ?# (Meridian flip in progress)
        '''
        self.scope.send(':Gm#')
        return self.scope.recv().replace('#', '')

    def set_aflip_pause_off(self):
        '''
        auto meridian flip pause-at-home OFF
        '''
        self.scope.send(':SX98,0#')
        return self.scope.recv() # SUCCESS == 1

    def set_aflip_pause_on(self):
        '''
        auto meridian flip pause-at-home ON
        '''
        self.scope.send(':SX98,1#')
        return self.scope.recv() # SUCCESS == 1

    def autoflip_pause_continue(self):
        '''
        auto meridian flip Continue when paused-at-home
        '''
        self.scope.send(':SX99,1#')
        #no return ?  self.scope.recv() # SUCCESS == 1 ?


# Home commands
    def return_home(self):
        '''
        Move back to home position
        '''
        self.update_status()
        self.scope.send(':hC#')
        # no return

    def reset_home(self):
        '''
        Reset, clears the "model" adjustments

        The actual 'home' position of a gem mount is always "c/w
        down, pointed at the celestial pole"

        The actual 'home' position for fork or alt-az mounts depends,
        but is usually "tube level, pointed due North or South"
        '''
        self.update_status()
        self.scope.send(':hF#')
        # no return

# Park commands
    def set_park(self):
        '''
        sets the parking position, could be different from 'home'
        '''
        self.update_status()
        self.scope.send(':hQ#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def park(self):
        '''
        move to the park position
        '''
        self.update_status()
        self.scope.send(':hP#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def un_park(self):
        '''
        allow leaving the park position, starts tracking
        '''
        self.update_status()
        self.scope.send(':hR#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1




## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     LIMITS / CORRECTIONS

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

# LIMITS

    def get_horizon_limit(self):
        '''
        GET horizon limit
        '''
        self.scope.send(':Gh#')
        return self.scope.recv().replace('#', '')

    def set_horizon_limit(self, limit):
        '''
        SET horizon limit (-30 / +30 degrees)
        '''
        self.scope.send(':Sh' + limit + '#')
        return self.scope.recv() # SUCCESS == 1

    def get_overhead_limit(self):
        '''
        GET overhead limit
        '''
        self.scope.send(':Go#')
        return self.scope.recv().replace('#', '')

    def set_overhead_limit(self, limit):
        '''
        SET overhead limit (<90 degrees, 90 degrees = 'off')
        '''
        self.scope.send(':So' + limit + '#')
        return self.scope.recv() # SUCCESS == 1

    '''
    another weird thing (maybe I'm missing something?)
    OnStep seems to store these 'pier limit' settings in degrees,
    but returns them in terms of 'arc-minutes'.
    Also, when setting the limits, you have to send an arc-
    minutes value which is then converted to degrees in the controller.
    Anywho....there's get/set functions for both representations...
    '''

    def get_minutes_past_E(self):
        '''
        Get Minutes Past Meridian EAST
        '''
        self.scope.send(':GXE9#')
        return self.scope.recv().replace('#', '')

    def set_minutes_past_E(self, limit):
        '''
        SET Minutes Past Meridian EAST
        '''
        self.scope.send(':SXE9,'+limit+'#')
        return self.scope.recv() # SUCCESS == 1

    def get_degrees_past_E(self):
        '''
        Get DEGREES Past Meridian EAST
        '''
        return int(int(self.get_minutes_past_E()) / 4.0)

    def set_degrees_past_E(self, limit):
        '''
        SET Degrees Past Meridian EAST
        '''
        cmd = ':SXE9,{}#'.format( int(limit) * 4.0 )
        self.scope.send(cmd)
        return self.scope.recv() # SUCCESS == 1


    def get_minutes_past_W(self):
        '''
        Get Minutes Past Meridian WEST
        '''
        self.scope.send(':GXEA#')
        return self.scope.recv().replace('#', '')

    def set_minutes_past_W(self, limit):
        '''
        SET Minutes Past Meridian WEST
        '''
        self.scope.send(':SXEA,'+limit+'#')
        return self.scope.recv() # SUCCESS == 1

    def get_degrees_past_W(self):
        '''
        Get DEGREES Past Meridian WEST
        '''
        return int(int(self.get_minutes_past_W()) / 4.0)

    def set_degrees_past_W(self, limit):
        '''
        SET Degrees Past Meridian WEST
        '''
        cmd = ':SXEA,{}#'.format( int(limit) * 4.0 )
        self.scope.send(cmd)
        return self.scope.recv() # SUCCESS == 1



# CORRECTIONS

    def get_backlash(self, axis = 1):
        '''
        Get backlash for axis
        '''
        if axis == 1:
            ax = 'R'
        elif axis == 2:
            ax = 'D'
        else:
            return '0' # SUCCESS == 1
        self.scope.send(':%B' + str(ax) + '#')
        return self.scope.recv().replace('#', '')

    def set_backlash(self, axis = 1, value = 0):
        '''
        Set backlash for axis
        '''
        if axis == 1:
            ax = 'R'
        elif axis == 2:
            ax = 'D'
        else:
            return '0' # SUCCESS == 1
        self.scope.send(':$B' + ax + str(value) + '#')
        return self.scope.recv().replace('#', '')

    def get_debug_equ(self):
        '''
        Get Equatorial values in decimal
        '''
        self.scope.send(':GXFE#')
        return self.scope.recv().replace('#', '')

    def get_ax_motor_pos(self, axis = 1):
        '''
        Get Axis motor position
        '''
        if axis == 1:
            ax = '8'
        elif axis == 2:
            ax = '9'
        else:
            return '0' # SUCCESS == 1
        self.scope.send(':GXF' + str(ax) + '#')
        return self.scope.recv().replace('#', '')

    def get_spd(self, axis = 1):
        '''
        Get Axis motor steps-per-degree
        '''
        if axis == 1:
            ax = '4'
        elif axis == 2:
            ax = '5'
        else:
            return '0' # SUCCESS == 1
        self.scope.send(':GXE' + str(ax) + '#')
        return self.scope.recv().replace('#', '')

    def get_cor_alt(self):
        '''
        Get Altitude Correction
        '''
        self.scope.send(':GX02#')
        return self.scope.recv().replace('#', '')

    def get_cor_azm(self):
        '''
        Get Azimuth Correction
        '''
        self.scope.send(':GX03#')
        return self.scope.recv().replace('#', '')

    def get_cor_do(self):
        '''
        Get Cone Error Correction
        '''
        self.scope.send(':GX04#')
        return self.scope.recv().replace('#', '')


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     DATE AND TIME
#         also see next section for utc
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    def get_TZoffset(self):
        '''
        Returns TimeZone hours (West negative), and
        code for Daylight Savings or Standard Time
        '''
        if (time.localtime().tm_isdst == 0):
            tz_offset = time.timezone
            tz_code = 'ST'
        else:
            tz_offset = time.altzone
            tz_code = 'DST'
        tz_offset = tz_offset / 60 / 60 * -1
        return tz_offset, tz_code

    def get_date(self):
        '''
        Get controller date
        '''
        self.scope.send(':GC#')
        return self.scope.recv().replace('#', '')

    def set_date(self):
        t = datetime.now()
        date = t.strftime("%m/%d/%y")
        self.scope.send(':SC' + date + '#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def get_time(self):
        '''
        Get controller time
        '''
        self.scope.send(':GL#')
        return self.scope.recv().replace('#', '')

    def get_time_2(self):
        '''
        ##this version corrects for the bizarre 2400 time
        ## returned by OnStep for one second at midnight
        #python only tolerates time values 0 to 23:59:59
        '''
        self.scope.send(':GL#')
        the_time = self.scope.recv().replace('#', '')
        return     the_time if the_time!='24:00:00' else '00:00:00'

    def set_time(self):
        '''
        Sets OnStep Local Time based on UTC offset AND TimeZone,
        to account for Daylight Savings Time (if used), since
        System Time can vary because of it
        '''
        t = datetime.now()
        tzo, tzcode = self.get_TZoffset()
        UTC_offset = self.get_utc().split(':')
        time = datetime.now() - TimeDelta(hours=int(UTC_offset[0])+(int(UTC_offset[1])/60)+tzo)
        time = time.strftime('%H:%M:%S')
        self.scope.send(':SL' + time + '#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def get_sidereal(self):
        '''
        Get controller local sidereal time
        '''
        #[com dot hotmail @ rlw1138] -- 2020-APR-15
        self.scope.send(':GS#')
        return self.scope.recv().replace('#', '')

    def set_sidereal(self, time):
        ## debugging only? , do not set LST (usually)
        ## it's calculated within onstep from main clock
        return 0




## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     SITE (location) commands

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
#Return values generally indicate failure (0) or success (1).

    def get_utc(self):
        '''
        UTC Offset (West positive)

        Get UTC offset time (hours and minutes) to add to local time to convert to UTC
        Returns: [s]HH:MM#
        '''
        self.scope.send(':GG#')
        return self.scope.recv().replace('#', '')

    def set_utc(self, utc_offset):
        '''
        UTC Offset (West positive)
        '''
        self.scope.send(':SG' + utc_offset + '#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def get_site(self):
        '''
        GET number of CURRENT SITE (0-3)
        '''
        self.scope.send(':W?#')
        return self.scope.recv().replace('#', '')

    def set_site(self, site_num):
        '''
        set the current site: 0=M, 1=N, 2=O, 3=P
        '''
        if site_num >=0 and site_num < 4 :
            self.scope.send(':W' + str(site_num) + '#')
            return False # no errors assumed
        else:
            return 'invalid site number'

    def get_site_name(self, site):
        if site.upper() in self.valid_site :
            self.scope.send(':G' + site + '#')
            return self.scope.recv().replace('#', '')
            return ret #might be empty-string
        else:
            return 'invalid site'

    def set_site_name(self, site, name):
        if site.upper() in self.valid_site :
            if name != '' and len(name) <=15 :
                self.scope.send(':S' + site + name + '#')
                return self.scope.recv().replace('#', '')
                if ret == 0:
                    return True # there was an error
                else:
                    return False # no errors
            else:
                return 'invalid name'
        else:
            return 'invalid site'

    def get_longitude(self):
        '''
        get lon of CURRENT SITE
        '''
        self.scope.send(':Gg#')
        return self.scope.recv().replace('#', '')

    def set_longitude(self, longitude):
        '''
        set lon of CURRENT SITE
        '''
        self.scope.send(':Sg' + longitude + '#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1

    def get_latitude(self):
        '''
        get lat of CURRENT SITE
        '''
        self.scope.send(':Gt#')
        return self.scope.recv().replace('#', '')

    def set_latitude(self, latitude):
        '''
        set lat of CURRENT SITE
        '''
        self.scope.send(':St' + latitude + '#')
        return self.scope.recv().replace('#', '') # SUCCESS == 1



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     LIBRARY FUNCTIONS -- see text at end-of-file

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
#[com dot hotmail @ rlw1138] -- 2020-APR-15


    def user_space(self):
        '''
        number of open user-catalog entries remaining
        '''
        self.scope.send(':L?#')
        return self.scope.recv().replace('#', '')

    def get_catalog(self, num):
        '''
        SELECT USER CATALOG by Number
        '''
        self.scope.send(':Lo' + str(num) + '#')
        return self.scope.recv().replace('#', '')

    def move_back(self):
        '''
        move BACKWARD one record in user catalog
        '''
        self.scope.send(':LB#')

    def move_next(self):
        '''
        move FORWARD one record in user catalog
        '''
        self.scope.send(':LN#')

    def move_objectNum(self, num):
        '''
        GO TO catalog object by Number
        '''
        self.scope.send(':LC' + str(num) + '#')

    def move_catName(self):
        '''
        MOVE to the Next CATALOG NAME Record
        '''
        self.scope.send(':L$#')

    def get_itemID(self):
        '''
        gets "$name,type#" from controller
        '''
        self.scope.send(':LI#')
        ret = self.scope.recv()
        if ret != '':
            values = ret.split(',')
            name = values[0].replace('$', '')
            type = values[1].replace('#', '')
        else:
            name, type = ''
        return name, type

    def get_itemInfo(self):
        '''
        return name, type, ra, dec for current item in user catalog
        '''
        self.scope.send(':LR#')
        ret = self.scope.recv().replace('#', '')
        values = ret.split(',')
        name = values[0]
        type = values[1]
        if name != '' and type != 'UNK':
            ra     = values[2]
            dec     = values[3]
        else:
            name, type, ra, dec = '','','',''
        return name, type, ra, dec

    def set_itemInfo(self, name, type):
        '''
        sets Name, Type, RA, DEC for current user catalog item

        ra & de must be the "current target"
        '''
        if name != '' and self.valid_types.find(type) :
            self.scope.send(':LW' + name + ',' + type + '#')
            # :LW command returns 1:success or 0:fail
            ret = self.scope.recv().replace('#', '')
            # this function returns (for consistency when more than 2 return values)
            # 0:success or 1:fail or 2:name missing or invalid type
            if ret == '1':
                return 0   # SUCCESS == 0
            else:
                return 1
        else:
            return 2

    def clear_record(self):
        '''
        clears the current user catalog record
        '''
        self.scope.send(':LD#')

    def clear_catalog(self):
        '''
        clears the current user catalog
        '''
        self.scope.send(':LL#')

    def clear_ALL_CaTaLoGs(self):
        '''
        H.U.D. (Handy Universal Destruction)

        clears all records in all user catalogs
        '''
        self.scope.send(':L!#')

#    def x(self):
#    def x(self):

'''
Library functions for OnStep

[use the OnStep web page to upload object data to the controller's eeprom]

Library query ............. :L?#

Select catalog number       :Lonn#          Reply: 0 or 1
Move Back in catalog        :LB#            Reply: [none]
Move to Next in catalog     :LN#            Reply: [none]
Move to catalog item no     :LCnnnn#        Reply: [none]
Move to catalog name rec    :L$#            Reply: 1
Get catalog item id         :LI#            Reply: name,type#
Read catalog item info      :LR#            Reply: name,type,RA,Dec#
(also moves forward)

Write catalog item info     :LWssss,ttt#    Reply: 0 or 1
ssss=name, ttt=type code:
UNK,OC,GC,PN,DN,SG,EG,IG,KNT,SNR,GAL,CN,STR,PLA,CMT,AST

Clear current record        :LD#            Reply: [none]
Clear current cataLog       :LL#            Reply: [none]
Clear all catalogs          :L!#            Reply: [none]

The LI# and LW# commands also set/get target coordinates (as with :Gr#, :Sr#, :Gd#, :Sd#)
Library record storage is in EEPROM.
A catalog name record is like any other except the name must start with a '$'. A special search can then be done with the :L$# command to move to that record.
It's up to the user to not waste EEPROM with more than one name record per catalog. When the default PEC table size of 824 bytes is used, the first 1024 bytes are devoted to settings. The remaining EEPROM is used for catalog records. Each record is 16 bytes.
It's often best to divide up large Libraries into several smaller catalogs due to serial interface speed limitations.
'''
