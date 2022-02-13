"""     Menubar and related commands and Help texts
"""
import tkinter as tk #   <--- prefix all tkinter functions with tk.
import logging
import time
import sys
import tooltip
from tkinter import scrolledtext
from functools import partial
from hosts import Hosts
from slew import Slew
from commands import Commands
from object_data import ObjectData
from go_to import GoTo


class Menubar:


    def quit(event=None):
        ''' exit to system '''
        #print("quitting...")
        sys.exit(0)

    def abort_movement(self, parent, controller, event=None):
        '''interface between key-binding and control library for abort()'''
        self.parent=parent
        self.controller=controller
        #print("abort movement")
        from slew import Slew
        Slew.abort(self, self.parent, self.controller)
        self.app_data["var_GTobject"].set('')


    def mb(self, parent, controller):
        '''the main Menubar'''
        #def __init__(self, parent, controller, *args, **kwargs):
        def __init__(self):
            self.parent = parent
            self.controller = controller

        _bg='black'
        _fg='red'

        # MENU BAR at the top of the main window
        menubar = tk.Menu(parent)
        self.parent.config(menu=menubar)

        ## fake a vertical separator
        menu_spacer = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_spacer, label="\u22EE")
        menu_spacer.add_command(label="Don't click that", activebackground=menubar.cget("background"))


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' FILE MENU '''
        ###### uses tk.Menu() instead of tooltip.Menu_ToolTip() ######
        menu_file     = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=menu_file, underline=0, label='File')
        menu_file.add_command(label='New',      command=Menubar.newFile, state='disabled')
        menu_file.add_command(label='Open..',   command=Menubar.openFile, state='disabled')
        menu_file.add_command(label='Close...', command=Menubar.closeFile, state='disabled')

        # menu_file.add_separator()
        # menu_file.add_command(label='Pop-Up (Defaults)', command=partial(Menubar.popup, self, parent) )
        # menu_file.add_command(label='Pop-Up (custom)',   command=partial(Menubar.popup, self, parent, "Error Message", "ERROR: there was some kind of bad error!", "Dismiss", "pink", "modal", "800", "300") )
        # menu_file.add_command(label='Pop-Up (config)',   command=partial(Menubar.config_popup, self) )
        menu_file.add_separator()
        menu_file.add_command(label='Quit', underline=0, command=Menubar.quit, accelerator="Ctrl+Q")

        self.bind_all("<Control-q>", Menubar.quit)


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' EDIT MENU '''
        ###### uses tk.Menu() instead of tooltip.Menu_ToolTip() ######
        menu_edit     = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_edit,     label='Edit')
        '''menu_edit.add_command( Edit menu is empty )'''

        '''
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

        the rest of the menu will start out DISABLED, until we can
        establish a connection to an OnStep

        Only 'Settings -> Connection' will be activated until then

        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        '''

        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' ALIGN MENU '''
        ###### uses tooltip.Menu_ToolTip() instead of tk.Menu() ######
        menu_align    = tooltip.Menu_ToolTip(self)
        menubar.add_cascade(menu=menu_align, label='Align')
        menu_align.add_command(label='Alignment Stars', state='disabled', command=partial(Commands.alignment_stars, self, header=True))
        ## sub-menu
        menu_alignY   = tooltip.Menu_ToolTip(menu_align)
        label_text = "{:<20}{:>8}".format('n-Star Align','-->>')
        menu_align.add_cascade(menu=menu_alignY, label=label_text, state='disabled')
        menu_alignY.add_command(label='Align', command=partial(Commands.n_star, self, self.parent, self.controller))
        menu_alignY.add_command(label='Help',  command=lambda:Menubar.help_popup('n-Star Align Help', Menubar.align_text))
        menu_align.add_command(label='Manual Align', state='disabled', command=partial(Commands.accept_align, self, self.parent, self.controller))
        menu_align.add_command(label='Sync now',     state='disabled', command=lambda:self.controller.scope.sync2target())
        ## sub-menu
        menu_alignZ   = tooltip.Menu_ToolTip(menu_align)
        label_text = "{:<20}{:>8}".format('Refine Polar','-->>')
        menu_align.add_cascade(menu=menu_alignZ, label=label_text, state='disabled')
        menu_alignZ.add_command(label='Polar Align', command=partial(Commands.slew_polar, self, self.parent, self.controller) )
        menu_alignZ.add_command(label='Help', command=lambda:Menubar.help_popup('Polar Alignment Help', Menubar.polar_text))
        ## back to Align menu entries


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' CONTROLS (GO-TO) MENU '''
        menu_control     = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_control,    label='Control')

        label_text = "{:<20}{:>8}".format('Motion Controls','-->>')
        menu_control.add_command(label=label_text, state='disabled', command=partial(Commands.movement, self, self.parent, self.controller) )
        menu_control.add_separator()
        ## sub-menu
        menu_controlX    = tk.Menu(menu_control)
        label_text = "{:<20}{:>8}".format('Go-To Object','-->>')
        menu_control.add_cascade(menu=menu_controlX, label=label_text, state="disabled")
        menu_controlX.add_command(label='Choose UserCatalog', command=partial(ObjectData.choose_DataSource, self, self.parent, self.controller, "USER" ))
        menu_controlX.add_command(label='Choose Datafile',    command=partial(ObjectData.choose_DataSource, self, self.parent, self.controller, "FILE" ))
        menu_control.add_separator()
        ## back to Go-To menu entries
        menu_control.add_command(label='Enter Coords', state="disabled", command=partial(Commands.coordinates, self, self.parent) )
        menu_control.add_command(label='Return to Target', state="disabled",  command=lambda: self.controller.scope.slew_equ())
        menu_control.add_checkbutton(label='Tracking on/off', state="disabled",  variable=self.controller.app_data["var_IsTracking"], onvalue=1, offvalue=0, selectcolor='green2',  command=partial(Slew.toggle_tracking, self, self.parent, self.controller))
        menu_control.add_command(label='ABORT',      state="disabled", underline=0, accelerator="Ctrl+A", command=partial(Slew.abort, self, self.parent, self.controller))
        menu_control.add_command(label='HOME',       state="disabled", command=partial(Slew.home, self, self.parent, self.controller))
        menu_control.add_command(label='Home reset', state="disabled", command=partial(Slew.reset_home, self, self.parent, self.controller))
        menu_control.add_command(label='PARK',       state="disabled", command=partial(Slew.park, self, self.parent, self.controller))
        menu_control.add_command(label='UN-Park',    state="disabled", command=partial(Slew.un_park, self, self.parent, self.controller))
        menu_control.add_command(label='Park set',   state="disabled", command=partial(Slew.set_park, self, self.parent, self.controller))
        menu_control.add_command(label='Meridian Flip now',     state="disabled", command=partial(Slew.flip_now, self, self.parent, self.controller, self.app_data["var_MountType"].get()))
        menu_control.add_command(label='Meridian Flip continue',state="disabled", command=lambda: self.controller.scope.autoflip_pause_continue())
         #command=partial(self.pause_continue, self))

        '''this doesn't work because bind() sends hidden 'event' info, so we create 'abort_movement()' here in Menubar class to accept the extra hidden parameter, and then it calls Slew.abort():
        self.bind_all("<Control-a>", partial(Slew.abort, self, self.parent, self.controller))'''
        self.bind_all("<Control-a>", partial(Menubar.abort_movement, self, self.parent, self.controller))


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' STOP MENU '''
        menu_stop = tk.Menu(menubar)
        menubar.add_cascade(label=' ! STOP ! ',menu=menu_stop)
        menu_stop.add_command(label='!', accelerator='Ctrl-Space  !', state='disabled',  command=partial(Slew.abort, self, self.controller, self.controller))
        self.bind_all("<Control-space>", partial(Menubar.abort_movement, self, self.parent, self.controller))


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' SETTINGS MENU '''
        menu_settings = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Connection',   command=partial(Hosts.choose_hostGUI, self, self.parent, self.controller ))
        menu_settings.add_command(label='Settings Help', command=lambda:Menubar.help_popup('Settings Help', Menubar.settings_text))
        ## sub-menu
        menu_settingsZ    = tk.Menu(menu_settings)
        label_text = "{:<20}{:>8}".format('Guide Rate','-->>')
        menu_settings.add_cascade(menu=menu_settingsZ, label=label_text, state='disabled')
        menu_settingsZ.add_radiobutton(label='0.25x',     variable=self.controller.app_data["var_Guide_Rate"], value='0.25x', selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 0) )
        menu_settingsZ.add_radiobutton(label='0.5x',      variable=self.controller.app_data["var_Guide_Rate"], value='0.5x',  selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 1) )
        menu_settingsZ.add_radiobutton(label='1x Guide',  variable=self.controller.app_data["var_Guide_Rate"], value='1x',    selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 2) )
        menu_settingsZ.add_radiobutton(label='2x',        variable=self.controller.app_data["var_Guide_Rate"], value='2x',    selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 3) )
        menu_settingsZ.add_radiobutton(label='4x',        variable=self.controller.app_data["var_Guide_Rate"], value='4x',    selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 4) )
        menu_settingsZ.add_radiobutton(label='8x Center', variable=self.controller.app_data["var_Guide_Rate"], value='8x',    selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 5) )
        menu_settingsZ.add_radiobutton(label='20x Find',  variable=self.controller.app_data["var_Guide_Rate"], value='20x',   selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 6) )
        menu_settingsZ.add_radiobutton(label='48x Fast',  variable=self.controller.app_data["var_Guide_Rate"], value='48x',   selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 7) )
        menu_settingsZ.add_radiobutton(label='Half-Max',  variable=self.controller.app_data["var_Guide_Rate"], value='half',  selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 8) )
        menu_settingsZ.add_radiobutton(label='Max',       variable=self.controller.app_data["var_Guide_Rate"], value='max',   selectcolor='green2', command=partial(Commands.guide_rate, self, self.parent, self.controller, 9) )
        ## back to Settings menu entries
        ## sub-menu
        menu_settingsW    = tk.Menu(menu_settings)
        label_text = "{:<20}{:>8}".format('Max Slew','-->>')
        menu_settings.add_cascade(menu=menu_settingsW, label=label_text, state='disabled')
        menu_settingsW.add_radiobutton(label='50%',  variable=self.controller.app_data["var_Slew_Max"], value='5', selectcolor='green2', command=partial(Commands.slew_speed_max, self, self.parent, self.controller, '5')  )
        menu_settingsW.add_radiobutton(label='75%',  variable=self.controller.app_data["var_Slew_Max"], value='4', selectcolor='green2', command=partial(Commands.slew_speed_max, self, self.parent, self.controller, '4')    )
        menu_settingsW.add_radiobutton(label='1x',   variable=self.controller.app_data["var_Slew_Max"], value='3', selectcolor='green2', command=partial(Commands.slew_speed_max, self, self.parent, self.controller, '3')    )
        menu_settingsW.add_radiobutton(label='150%', variable=self.controller.app_data["var_Slew_Max"], value='2', selectcolor='green2', command=partial(Commands.slew_speed_max, self, self.parent, self.controller, '2')    )
        menu_settingsW.add_radiobutton(label='2x',   variable=self.controller.app_data["var_Slew_Max"], value='1', selectcolor='green2', command=partial(Commands.slew_speed_max, self, self.parent, self.controller, '1')    )
        ## back to Settings menu entries

        menu_settings.add_command(label='OnStep Time', state="disabled", command=lambda:self.controller.scope.set_time()) # self.time_sync)
        menu_settings.add_command(label='Location',    state="disabled", command=partial(Commands.location, self, self.parent) )
        ## sub-menu
        menu_settingsX    = tk.Menu(menu_settings)
        label_text = "{:<20}{:>8}".format('Limits'+u"\u2001"+u"\u2001",'-->>') ## two EM Quads to push the arrows over
        menu_settings.add_cascade(menu=menu_settingsX, label=label_text, state="disabled")
        menu_settingsX.add_command(label='Overhead',  command=partial(Commands.overhead, self, self.parent) )
        menu_settingsX.add_command(label='Horizon',   command=partial(Commands.horizon, self, self.parent) )
        menu_settingsX.add_command(label='Past East', command=partial(Commands.pastE, self, self.parent) )
        menu_settingsX.add_command(label='Past West', command=partial(Commands.pastW, self, self.parent) )
        ## back to Settings menu entries
        menu_settings.add_command(label='Backlash',      state="disabled", command=partial(Commands.backlash, self, self.parent) )
        ## sub-menu
        menu_settingsY    = tk.Menu(menu_settings)
        label_text = "{:<20}{:>8}".format('Tune Backlash','-->>')
        menu_settings.add_cascade(menu=menu_settingsY, label=label_text, state="disabled")
        menu_settingsY.add_command(label='Tune R/A axis', command=partial(Commands.tune_backlash, self, self.parent, self.controller, "R/A"))
        menu_settingsY.add_command(label='Tune DEC axis', command=partial(Commands.tune_backlash, self, self.parent, self.controller, "DEC"))
        ## back to Settings menu entries
        menu_settings.add_checkbutton(label='Meridian Flip Auto', state="disabled",
        variable=self.controller.app_data["var_AFlip_State"], onvalue=1, offvalue=0,
        selectcolor='green2',  command=partial(Slew.toggle_autoflip, self, self.parent, self.controller))
        menu_settings.add_checkbutton(label='AutoFlip Pause Home', state="disabled",
        variable=self.controller.app_data["var_Pause_State"], onvalue=1, offvalue=0,
        selectcolor='green2',  command=partial(Slew.toggle_pauseHome, self, self.parent, self.controller))


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' TOOLS MENU '''
        menu_tools = tooltip.Menu_ToolTip(menubar)
        menubar.add_cascade(menu=menu_tools,   label='Tools')
        #menu_settings.add_separator()
        menu_tools.add_command(label='Stress test', state="disabled", tooltip=
        ' Exercise the motors with \n'
        ' repeated long slews', command=partial(Commands.stress_test, self, self.parent, self.controller) )
        menu_tools.add_command(label='Drift test',  state="disabled", tooltip=
        ' Check for tracking drift, \n'
        ' (takes ~20 minutes) \n'
        ' OnStepX broke this.', command=partial(Commands.drift_test, self, self.parent, self.controller) )


        # / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
        ''' HELP MENU '''
        menu_help     = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_help,     label='Help')
        menu_help.add_command(label='Help', command=lambda:Menubar.help_popup('General Help', Menubar.help_text))
        menu_help.add_command(label='About Console', command=lambda:Menubar.help_popup('About: OnStep python command console', Menubar.about_text))

        menubar.configure(        relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_file.configure(      relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_edit.configure(      relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_align.configure(     relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_alignY.configure(    relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_alignZ.configure(    relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_control.configure(   relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_controlX.configure(  relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_settings.configure(  relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_settingsZ.configure( relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_settingsW.configure( relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_settingsX.configure( relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_settingsY.configure( relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_tools.configure(     relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')
        menu_help.configure(      relief='groove', borderwidth=6, bg=_bg, fg=_fg, activebackground='brown3')

        menu_stop.config(bg='gray40', fg='OrangeRed2')


        return  menu_file,  menu_edit,  menu_align,  menu_control,  menu_settings,  menu_tools,   menu_help,   menu_stop,   menubar


    def newFile():
        '''dummy stub'''
        pass

    def openFile():
        '''dummy stub'''
        pass

    def closeFile():
        '''dummy stub'''
        pass


    """ Help Screens """

    align_text = '''
     > > > Always Start Alignment At HOME Position! < < <\n
    Once completed, ALIGNMENT is 'saved' if you do a "set-Park".\n
    -- One Star Alignment: Pick a bright star that is:
       East of current location (telescope west of the mount)
       Near the Meridian (R/A close to Local Sidereal Time) and
       Near the Celestial Equator (Dec near zero).
       > Corrects for Right Ascension and Declination offset.\n
    -- Two Star Alignment: First star same as above.  Second
       star should be West (telescope east of the mount), also
       Near the Meridian (R/A close to Local Sidereal Time) and
       Near the Celestial Equator (Dec near zero).
       > Adds correction for polar axis Altitude misalignment
       and cone error.\n
    -- Three Star Alignment: Stars 1 & 2 same as above.  Third
       star should be westerly near 45* Dec (or -45) and 5+ hours
       to the west.
       > Adds correction for polar axis Azimuth misalignment.\n
    The 'sync' equatorial coordinates command refines the model
    for a local area of the sky, this refinement is lost when the
    power is cycled unless another Set Park is called.\n'''


    polar_text='''
    HOW TO IMPROVE THE POLAR ALIGNMENT\n
    1. Do a rough alignment using the polar scope.\n
    2. Do a 3 star Align, starting at Home.\n
    3. Go-To a fourth star (from Home) and Sync on it. Use
       a cross-hair eyepiece if possible. Star should have
       DEC between 50 and 80; and not too close to Zenith,
       Meridian, Celestial Pole or due East or West.\n
    4. In menu 'Align -> Refine Polar', do 'Polar Align'
       The mount will move to where the star would be *IF*
       the mount was perfectly polar-aligned.\n
    5. Using ONLY the mount's manual Altitude and Azimuth
       controls, again center the star perfectly.\n
    6. Return the mount to the home position.\n
    7. Repeat the 3-star align procedure.\n'''


    settings_text='''
    First establish a connection to an OnStep controller. Once connected, all the menu items will be activated.

    Although most operational settings can be adjusted by the console, some must be entered using either the OnStep web pages, the smart-phone android app, the Smart Hand Controller (SHC) or Sky Planetarium.

    Among these are Periodic Error Correction (PEC), Location entries, the Time Offset, and all of the Network options, and Advanced Configuration.

    Note that some entries must be multiple digits, or include punctuation such as a + or - sign, or a 'degree' symbol (an asterisk * ), or colon :
    '''


    help_text=''' HELP TEXT (alphabetic)

--  You will probably want to edit hosts.py to reflect your network setup. There is an entry for the OnStep default network address of 192.168.0.1 to get you started.

  ALIGN              CONTROL                   SETTINGS         TOOLS
  --------------     ----------------          -----------      ------------
  Alignment stars    Motion Controls           Connection       Stress Test
  n-Star Align       Go-To Object              Guide Rate       Drift Test
  Sync manual        Enter Coordinates         Slew Speed Max
  Sync Now           Return to Target          OnStep time
  Refine Polar       Tracking On/Off           Location
                     ABORT                     Limits:
                     HOME                           Overhead
                     Home reset                     Horizon
                     PARK                           Past East
                     UN-park                        Past West
                     Park Set                  Backlash
                     Meridian Flip now         Tune Backlash
                     Meridian Flip Continue    Meridian Flip Auto
                                               AutoFlip Pause-at-Home
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  ABORT
  <Control-A> -- Stops all movement.

  Alignment stars
  Displays a list of bright observable stars, within 75* of your zenith, for when and where you are.

  AutoFlip Pause-at-Home
  If Meridian Flips are set to "auto", this setting will cause the mount to pause at the Home postition until the "continue" command is given.

  Backlash
  Accepts entry of backlash settings.

  Connection
  The network address of OnStep is defined in ./hosts.py -- use your favorite text editor to find out more.

  Drift Test
  Monitors motor position relative to time, to calculate axis 'drift' from ideal.

  ERRORS & Warnings
  Any time a 'limit' is exceeded, during tracking or a go-to, the motors will be stopped. To recover, use a hand control or app to move back within limits. Or issue a Home or Park command.

  Go-To Object
  Sets a celestial object as the 'target' and moves the mount to point at it. You can select objects from datafiles on your host computer, or user catalogs that have been uploaded into the   OnStep controller.

  Guide Rate
  Guiding speeds: .25x, .5x, 1x (guide), 2x, 4x, 8x (center), 20x (find), 48x (fast), Half-Max, (very fast), Max

  HOME
  Moves the mount to the 'home' position. Generally, this is counterweight-down and pointing at the celestial pole for an equatorial mount, or optical tube level and pointed due North or South for a fork-mount or alt-az mount.

  Home Reset
  Sets the current mount position as 'home', and clears the "model" of angular corrections. You should manually move the mount to the actual 'home' position before or after this command.

  Limits
  Settings for Horizon, Overhead, degrees Past East and West of the 'pier'.

  Location
  Stores up to four sites (name, latitude, longitude, and time offset)

  Meridian Flip
  Can be set either 'auto' or manual, with optional pause-at-home.

  Meridian Flip Continue
  If pause-at-home is enabled, this command continues the flip when the mount is waiting at home.

  Motion Controls
  Opens a window with eight directional buttons, the cardinal and ordinal points of the compass. Only one direction can be activated at a time, and motion will continue until halted. Speed settings are same as Guide Rate (default 1x), incremented/decremented with the +/- buttons. North/South and East/West can be swapped separately, swapping will effect a Halt. Tracking must be On.

  n-Star Align
  Choose up to three stars from a list, and align the mount to them.

  OnStep Time
  Synchronizes the OnStep controller's internal clock with the host computer.

  PARK
  Allows the mount to be safely positioned when not in use. May or may not be the same as HOME,

  Park set
  Sets the Park position, and saves any correction information.

  Refine Polar
  Allows for fine-tuning the polar alignment of the mount.

  Return to target
  Once a target has been established, via a "go-to" or by entering coordinates, you can return to it after you've 'visited' other nearby neighbors.

  Slew Speed Max
  Sets maximum speed used during go-to's, 50%, 75%, 1x, 150%, 2x -- '1x' is the "base rate" set in config.h at compile-time.

  STOP
  <Control-Space> -- stops all movement.

  Sync Manual
  Same as the command "accept alignment point", which is issued automatically during an n-Star Align.

  Sync Now
  Tells OnStep that the target coordinates of the most recent "go-to" are now centered in the field of view. Improves tracking accuracy in nearby parts of the sky.

  Tracking On/Off
  Manually turns tracking on or off.

  Tune Backlash
  Determines the correct backlash compensation by slewing the mount along each axis.

  UN-Park
  Leaves the 'parked' position and starts Tracking.

  SEE THE ONSTEP WIKI AT WWW.GROUPS.IO FOR FURTHER INFO.
      '''

    about_text='''
    An extensible control utility for OnStep
    Written in python and Tkinter
    Copyright 2020-2022 Russ Williams (rlw1138 # hotmail-dot-com)

    python LX200 command library and test scripts originally created
    by Khalid Baheyeldin [https://github.com/kbahey/onstep-python]

    GPL license, etc etc


    --  If you know (or can learn) the python programming language, the
        console can easily be extended to include any feature you want.
    '''

    ## put this AFTER all the help texts
    def help_popup(title, text):
        '''popup window for the various help screens'''
        _bg='grey19'
        _fg='brown3'
        pop = tk.Toplevel()
        pop.grab_set() # make pop 'modal' (must click to dismiss)
        pop.title(title)
        pop.minsize(540, 300)
        pop.config(bg=_bg, padx=1, pady=1, width=555)
        _text=text

        # msg = tk.Message(pop, text=_text, bg=_bg, fg=_fg, width=555)
        # msg.config(font=("TkDefaultFont", 12))
        # msg.pack()

        scroll_text = scrolledtext.ScrolledText(pop, undo=True)
        scroll_text.config(bg=_bg, fg=_fg, width=80, height=24)
        scroll_text.config(padx=10, pady=10, wrap='word')
        scroll_text.insert(tk.INSERT, _text)
        scroll_text['font'] = ('consolas', '12')
        scroll_text.pack(expand=True, fill='both')

        button = tk.Button(pop, text="close", command=pop.destroy)
        button.config(bg=_bg, fg=_fg, pady=4, activebackground='goldenrod1')
        button.config(highlightbackground='goldenrod1')
        button.config(highlightcolor='red')
        button.config(highlightthickness=1)
        button.pack()


    """these are included only because"""

    def popup(self, parent, _title='popup-title', _text='some-default-text', _button='btn_lbl', _bg='grey', _type='modal', _width='60', _height='10'):
        '''a generic pop-up'''

        self.parent=parent

        self.pop = tk.Toplevel()
        self.pop.attributes('-topmost',True)
        self.x = parent.winfo_x()
        self.y = parent.winfo_y()
        self.pop.geometry("+%d+%d" % (self.x + 100, self.y + 200))
        if _type and _type.lower()=='modal':
            self.pop.grab_set() # make pop 'modal' (must click to dismiss)
        self.pop.title(_title)
        if (not _width) and (not _height):
            self.pop.minsize(600, 400)
            self.pop.config(bg=_bg, padx=10, pady=10)
            self.pop.geometry('600x400')
        elif _width and _height:
            self.pop.config(bg=_bg, padx=10, pady=10, width=int(_width), height=int(_height) )
            self.pop.geometry('600x400')
        else:
            self.pop.config(bg=_bg, padx=10, pady=10, width=int(_width), height=int(_height) )
            self.pop.geometry('600x400')
        self.msg = tk.Message(self.pop, text=_text, bg=_bg, width=60)
        self.msg.pack()
        self.button = tk.Button(self.pop, text=_button, command=self.pop.destroy)
        self.button.pack()


    def config_popup(self, _title='config options', _text='settings available', _button='Close', _bg='grey', _fg='pink'):
        '''displays config info in a pop-up'''
        pop = tk.Toplevel()
        pop.geometry("100x190")
        pop.grab_set() # make pop 'modal' (must click to dismiss)
        pop.title(_title)
        pop.config(bg=_bg, padx=10, pady=10)
        msg = tk.Message(pop, text=_text, bg=_bg, fg=_fg)
        msg.pack()
        #from tkinter import *
        from pprint import pprint
        pprint('Settings of "pop" window')
        pprint(tk.Radiobutton().config())

        button = tk.Button(pop, text=_button, command=pop.destroy)
        button.pack()
