#!/usr/bin/python3



""" Main Window for OnStep GUI version """

## Line  41 -- __init__() Graphical User Interface
## Line 524 -- code for update loops
## Line 695 -- Entry Point
## Line 914 -- some miscellaneous functions

CONSOLE_VERSION=".988"
ONSTEP="---"
import sys
import os
sys.path.append(os.getcwd())
import conversion
# import libraries -- note Class DateTime is distinct from Module datetime
# CLASSES
from datetime import datetime as DateTime, timedelta as TimeDelta, date as Date
# MODULES
import datetime
import time
import logging
''' "logging" message levels
 lowest / logging.DEBUG / INFO / WARNING / ERROR / CRITICAL / highest '''
TIMESTAMP = "{}".format( int( DateTime.timestamp( DateTime.now() ) ) )
FILE_PATH = "./logs/console_errors_"+TIMESTAMP+".log"

logging.basicConfig(filename=FILE_PATH, format='\n{asctime} {levelname:8s} {message}', style='{', level=logging.INFO)

logging.info(f'OnStep console v{CONSOLE_VERSION} started')
logging.info(f'logging to {FILE_PATH}')


import tkinter as tk #   <--- prefix all tkinter functions with tk.
#from tkinter import *   <--- dont do this
#from tkinter import ttk
from tkinter.font import Font

class MainWindow(tk.Frame):
    ''' "Five Hundred Lines of GUI" '''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = self

        """
        frame_    frames
        lbl_      data element text labels
        val_      label widget to hold values
        var_      the variables themselves
        lb_       Listbox
        """


        '''
        Define ALL variables for Screen Items here, so the 'controller'
        can make them available to all other modules and functions.

        Based on MVC (Model-View-Controller) concept

        See: "choose_hostGUI()" in hosts.py
        '''
        ## python_variable=self.controller.app_data["name"].get(), ..
        ## self.controller.app_data["name"].set(SomeValue), ..
        self.app_data = {
            "var_LastError"   : tk.StringVar(),
            "var_MountStatus" : tk.StringVar(),
            "var_IsTracking"  : tk.IntVar(),
            "var_Tracking"    : tk.StringVar(),
            "var_GTobject"    : tk.StringVar(),
            "var_RA"          : tk.StringVar(),
            "var_DEC"         : tk.StringVar(),
            "var_TargetRA"    : tk.StringVar(),
            "var_TargetDEC"   : tk.StringVar(),
            "var_ALT"         : tk.StringVar(),
            "var_AZ"          : tk.StringVar(),
            "var_Slew_Max"    : tk.StringVar(),
            "var_Guide_Rate"  : tk.StringVar(),
            "var_LST"         : tk.StringVar(),
            "var_OnStepTime"  : tk.StringVar(),
            "var_UTCoffset"   : tk.StringVar(),
            "var_UTC"         : tk.StringVar(),
            "var_TZoffset"    : tk.StringVar(),
            "var_TZcode"      : tk.StringVar(),
            "var_SysClock"    : tk.StringVar(),
            "var_MountType"   : tk.StringVar(),
            "var_Parked"      : tk.StringVar(),
            "var_AtHome"      : tk.StringVar(),
            "var_Slewing"     : tk.StringVar(),
            "var_AutoFlip"    : tk.StringVar(),
            "var_AFlip_State" : tk.IntVar(),
            "var_PauseHome"   : tk.StringVar(),
            "var_Pause_State" : tk.IntVar(),
            "var_AFlip_Pos"   : tk.StringVar(),
            "var_PierSide"    : tk.StringVar(),
            "var_PEC"         : tk.StringVar(),
            "var_PECrecorded" : tk.StringVar(),
            "var_PPS"         : tk.StringVar(),
            "var_ConeCorr"    : tk.StringVar(),
            "var_AltCorr"     : tk.StringVar(),
            "var_AzCorr"      : tk.StringVar(),
            "var_Backlash1"   : tk.StringVar(),
            "var_Backlash2"   : tk.StringVar(),
            "var_Overhead"    : tk.StringVar(),
            "var_Horizon"     : tk.StringVar(),
            "var_WARNING"     : tk.StringVar(),
            "var_ERROR"       : tk.StringVar(),
            "var_PastE"       : tk.StringVar(),
            "var_PastW"       : tk.StringVar(),
            "var_SiteNum"     : tk.StringVar(),
            "var_SiteName"    : tk.StringVar(),
            "var_Lat"         : tk.StringVar(),
            "var_Lon"         : tk.StringVar(),
            "var_lbl_Connection" : tk.StringVar(),
            "var_OnStep"      : tk.StringVar(),
            "var_Host"        : tk.StringVar(),
            "var_Port"        : tk.StringVar(),
            "var_DisplayDate" : tk.StringVar(),
            "var_Pulse"       : tk.StringVar(),
            "var_DataSource"  : tk.StringVar(),
            "var_RowNum"      : tk.IntVar(),
        }


        self.app_data["var_WARNING"].set("Connect to an OnStep Controller, in 'Settings'")
        self.app_data["var_ERROR"].set("errors")
        self.app_data["var_OnStep"].set("not connected")
        self.app_data["var_Host"].set("none") # do not change these two defaults,
        self.app_data["var_Port"].set("none") # unless you want to break things


        ''' These defaults were useful when laying out the widgets,
            they are not really needed anymore but they might be
            handy when debugging.....
        self.app_data["var_LastError"].set("n/a")
        self.app_data["var_MountStatus"].set("n/a")
        self.app_data["var_Tracking"].set("no")
        self.app_data["var_GTobject"].set("n/a")
        self.app_data["var_RA"].set("00:00:00")
        self.app_data["var_DEC"].set("00:00:00")
        self.app_data["var_ALT"].set("00:00:00")
        self.app_data["var_AZ"].set("00:00:00")
        self.app_data["var_LST"].set("00:00:00")
        self.app_data["var_OnStepTime"].set("00:00:00")
        self.app_data["var_UTCoffset"].set("00")
        self.app_data["var_UTC"].set("00:00:00")
        self.app_data["var_TZoffset"].set("00")
        self.app_data["var_TZcode"].set("xxx")
        self.app_data["var_SysClock"].set("99:99:99")
        self.app_data["var_MountType"].set("n/a")
        self.app_data["var_Parked"].set("no")
        self.app_data["var_AtHome"].set("no")
        self.app_data["var_Slewing"].set("no")
        self.app_data["var_AutoFlip"].set("no")
        self.app_data["var_AFlip_Pos"].set("")
        self.app_data["var_PierSide"].set("n/a")
        self.app_data["var_PEC"].set("Ready to record")
        self.app_data["var_PECrecorded"].set("no")
        self.app_data["var_PPS"].set("Off")
        self.app_data["var_ConeCorr"].set("00")
        self.app_data["var_AltCorr"].set("00")
        self.app_data["var_AzCorr"].set("00")
        self.app_data["var_Backlash1"].set("00")
        self.app_data["var_Backlash2"].set("00")
        self.app_data["var_Overhead"].set("00")
        self.app_data["var_Horizon"].set("00")
        self.app_data["var_PastE"].set("00")
        self.app_data["var_PastW"].set("00")
        self.app_data["var_SiteNum"].set("0")
        self.app_data["var_SiteName"].set("none--------")
        self.app_data["var_Lat"].set("00:00:00")
        self.app_data["var_Lon"].set("00:00:00")
        self.app_data["var_DisplayDate"].set("DoW, YYYY-mon-DD")
        self.app_data["var_Pulse"].set("*")
        '''


        # CREATE the Main Container widgets

        ##  grid(), pack(), & place() always return 'None', so NEVER call
        ##  grid(), pack() or place() as part of the constructor!
        ##  ie: frame = tk.Frame(parent, stuff).pack() <---- "frame" will
        ##  end up as a 'None' and you won't be able to do anything else
        ##  with it!
        ##  INSTEAD do "frame = tk.Frame(parent, stuff)"
        ##        then "frame.pack()"

        frame_bd_outer=2
        frame_bd_inner=0
        _bg='black'
        _fg='red'


        row_Warning  = 0
        row_ERROR    = 1
        row_Coord    = 2
        row_Time     = 3
        row_Status   = 4
        row_GROUP1   = 4
        row_Loc      = 5
        row_Comms    = 6

        root.rowconfigure( row_Warning, weight = 1  )
        root.rowconfigure( row_ERROR,   weight = 1  )
        root.rowconfigure( row_Coord,   weight = 4  )
        root.rowconfigure( row_Time,    weight = 4  )
        root.rowconfigure( row_Status,  weight = 10 )
        root.rowconfigure( row_GROUP1,  weight = 10 )
        root.rowconfigure( row_Loc,     weight = 2  )
        root.rowconfigure( row_Comms,   weight = 1  )

        tk.Frame.configure(self, padx=8, pady=8)

        self.frame_WARNING  = tk.Frame(root, bg="goldenrod1", relief="groove" )
        self.WARNING = tk.Label(self.frame_WARNING, textvariable = self.app_data["var_WARNING"],bg='goldenrod1')

        self.frame_ERROR    = tk.Frame(root, bg="light pink", relief="groove" )
        self.ERROR = tk.Label(self.frame_ERROR, textvariable = self.app_data["var_ERROR"],bg='pink')


        self.frame_COORD    = tk.Frame(root, bg=_bg,          relief="groove", borderwidth=0)
        self.frame_COORD.rowconfigure( 0, weight = 50) #frame_Coord_a
        self.frame_COORD.rowconfigure( 1, weight = 50) #frame_Coord_b

        self.frame_Coord_a   = tk.Frame(self.frame_COORD, bg=_bg, relief="groove", borderwidth=frame_bd_inner)
        self.frame_Coord_a.rowconfigure( 0, weight = 50)
        self.lbl_LastError   = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="e", width=12, text="Last error:")
        self.lbl_MountStatus = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="e", width=12, text="Mount status:")
        self.val_LastError   = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="w", width=8,  textvariable = self.app_data["var_LastError"] )
        self.val_MountStatus = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="w", width=20, textvariable = self.app_data["var_MountStatus"])
        self.frame_Coord_a.rowconfigure( 1, weight = 50)
        self.lbl_Tracking    = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="e", width=12, text="Tracking:")
        self.lbl_GTobject    = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="e", width=12, text="Object:")
        self.val_Tracking    = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="w", width=8,  textvariable = self.app_data["var_Tracking"]  )
        self.val_GTobject    = tk.Label(self.frame_Coord_a, bg=_bg, fg=_fg, anchor="w", width=20, textvariable = self.app_data["var_GTobject"]  )

        self.frame_Coord_b   = tk.Frame(self.frame_COORD, bg=_bg, relief="groove", borderwidth=frame_bd_inner)
        self.frame_Coord_b.rowconfigure( 0, weight = 50)
        self.lbl_RA          = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=14, text="Right Ascension: ", padx=4)
        self.lbl_ALT         = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=10, text="Altitude: ", padx=4)
        self.lbl_ra_symbol   = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=7,  text="α")
        self.val_RA          = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=8, textvariable = self.app_data["var_RA"],  padx=4)
        self.val_ALT         = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=8, textvariable = self.app_data["var_ALT"], padx=4)
        self.val_TargetDEC   = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="w", width=10, textvariable = self.app_data["var_TargetDEC"], padx=4)
        self.frame_Coord_b.rowconfigure( 1, weight = 50)
        self.lbl_DEC         = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=14, text="Declination: ",     padx=4)
        self.lbl_AZ          = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=10, text="Azimuth: ",  padx=4)
        self.lbl_dec_symbol  = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=7,  text="δ")
        self.val_DEC         = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=8, textvariable = self.app_data["var_DEC"], padx=4)
        self.val_AZ          = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="e", width=8, textvariable = self.app_data["var_AZ"],  padx=4)
        self.val_TargetRA    = tk.Label(self.frame_Coord_b, bg=_bg, fg=_fg, anchor="w", width=10, textvariable = self.app_data["var_TargetRA"], padx=4)



        self.frame_Time     = tk.Frame(root, bg=_bg,          relief="groove", borderwidth=2)
        self.frame_Time.rowconfigure( 0, weight = 50)
        self.lbl_LST        = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="LST")
        self.lbl_OnStepTime = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="OnStep")
        self.lbl_UTCoffset  = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="UTC offset")
        self.lbl_UTC        = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="UTC")
        self.lbl_TZoffset   = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="TZ offset")
        self.lbl_SysClock   = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, text="System")
        self.lbl_TZcode     = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=6, text="")
        self.frame_Time.rowconfigure( 1, weight = 50)
        self.val_LST        = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_LST"])
        self.val_OnStepTime = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_OnStepTime"])
        self.val_UTCoffset  = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_UTCoffset"] )
        self.val_UTC        = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_UTC"]       )
        self.val_TZoffset   = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_TZoffset"] )
        self.val_SysClock   = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=8, textvariable = self.app_data["var_SysClock"] )
        self.val_TZcode     = tk.Label(self.frame_Time, bg=_bg, fg=_fg, width=6, textvariable = self.app_data["var_TZcode"] )


        self.frame_Status   = tk.Frame(root, bg=_bg,        relief="groove", borderwidth=0)
        self.frame_Status.rowconfigure( 0, weight = 166 )
        self.frame_Status.rowconfigure( 1, weight = 166 )
        self.frame_Status.rowconfigure( 2, weight = 166 )
        self.frame_Status.rowconfigure( 3, weight = 166 )
        self.frame_Status.rowconfigure( 4, weight = 166 )
        self.frame_Status.rowconfigure( 5, weight = 170 )
        self.lbl_MountType = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="Mount type:")
        self.val_MountType = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_MountType"] )
        self.lbl_Parked    = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="Parked:")
        self.val_Parked    = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_Parked"]    )
        self.lbl_AtHome    = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="At Home:")
        self.val_AtHome    = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_AtHome"]    )
        self.lbl_Slewing   = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="Slewing:")
        self.val_Slewing   = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_Slewing"]   )
        self.lbl_PierSide  = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="Pier side:")
        self.val_PierSide  = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_PierSide"]  )
        self.lbl_AutoFlip  = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 10, text="Auto-Flip:")
        self.val_AutoFlip  = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_AutoFlip"]  )
        self.val_AFlip_pos = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 18, textvariable = self.app_data["var_AFlip_Pos"]  )
        self.lbl_AFlip_Pos = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="e", width= 14, text="Pause-at-Home:")
        self.val_PauseHome = tk.Label(self.frame_Status, bg=_bg, fg=_fg, anchor="w", width= 8, textvariable = self.app_data["var_PauseHome"]  )



        self.frame_GROUP1   = tk.Frame(root, bg=_bg,          relief="groove", borderwidth=0)
        self.frame_GROUP1.rowconfigure( 0, weight = 25)
        self.frame_GROUP1.rowconfigure( 1, weight = 25)
        self.frame_GROUP1.rowconfigure( 2, weight = 25)
        self.frame_GROUP1.rowconfigure( 3, weight = 25)

        self.frame_PEC       = tk.Frame(self.frame_GROUP1, bg=_bg, width=100, height=50, relief="groove", borderwidth=frame_bd_inner)
        self.lbl_PPS         = tk.Label(self.frame_PEC, bg=_bg, fg=_fg, anchor="e", width= 6,  text="PPS: ")
        self.lbl_PECrecorded = tk.Label(self.frame_PEC, bg=_bg, fg=_fg, anchor="e", width= 12, text="PEC recorded: ")
        self.lbl_PEC         = tk.Label(self.frame_PEC, bg=_bg, fg=_fg,                        text=" - ")
        self.val_PPS         = tk.Label(self.frame_PEC, bg=_bg, fg=_fg, anchor="w", width= 3, textvariable = self.app_data["var_PPS"]       )
        self.val_PECrecorded = tk.Label(self.frame_PEC, bg=_bg, fg=_fg, anchor="w",           textvariable = self.app_data["var_PECrecorded"] )
        self.val_PEC         = tk.Label(self.frame_PEC, bg=_bg, fg=_fg, anchor="w",           textvariable = self.app_data["var_PEC"] )

        self.frame_Corr     = tk.Frame(self.frame_GROUP1, bg=_bg, width=100, height=50, relief="groove", borderwidth=frame_bd_inner)
        self.lbl_ConeCorr    = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="e", width= 10, text="ConeCorr: ")
        self.lbl_AltCorr     = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="e", width=  7, text="AltCorr: ")
        self.lbl_AzCorr      = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="e", width=  6, text="AzCorr: ")
        self.val_ConeCorr    = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_ConeCorr"]  )
        self.val_AltCorr     = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_AltCorr"]   )
        self.val_AzCorr      = tk.Label(self.frame_Corr, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_AzCorr"]    )

        self.frame_Backlash  = tk.Frame(self.frame_GROUP1, bg=_bg, width=100, height=50, relief="groove", borderwidth=frame_bd_inner)
        self.lbl_Backlash1   = tk.Label(self.frame_Backlash, bg=_bg, fg=_fg, anchor="e", width= 10, text="Backlash1: ")
        self.lbl_Backlash2   = tk.Label(self.frame_Backlash, bg=_bg, fg=_fg, anchor="e", width= 10, text="Backlash2: ")
        self.val_Backlash1   = tk.Label(self.frame_Backlash, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_Backlash1"] )
        self.val_Backlash2   = tk.Label(self.frame_Backlash, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_Backlash2"] )

        self.frame_Limits1   = tk.Frame(self.frame_GROUP1, bg=_bg, width=100, height=50, relief="groove", borderwidth=frame_bd_inner)
        self.lbl_Overhead    = tk.Label(self.frame_Limits1, bg=_bg, fg=_fg, anchor="e", width= 10, text="Overhead: ")
        self.lbl_Horizon     = tk.Label(self.frame_Limits1, bg=_bg, fg=_fg, anchor="e", width= 10, text="Horizon: ")
        self.val_Overhead    = tk.Label(self.frame_Limits1, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_Overhead"]  )
        self.val_Horizon     = tk.Label(self.frame_Limits1, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_Horizon"]   )

        self.frame_Limits2   = tk.Frame(self.frame_GROUP1, bg=_bg, width=100, height=50, relief="groove", borderwidth=frame_bd_inner)
        self.lbl_PastE       = tk.Label(self.frame_Limits2, bg=_bg, fg=_fg, anchor="e", width=  10, text="PastE: ")
        self.lbl_PastW       = tk.Label(self.frame_Limits2, bg=_bg, fg=_fg, anchor="e", width=  10, text="PastW: ")
        self.val_PastE       = tk.Label(self.frame_Limits2, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_PastE"]     )
        self.val_PastW       = tk.Label(self.frame_Limits2, bg=_bg, fg=_fg, anchor="w", width=  4, textvariable = self.app_data["var_PastW"]     )


        self.frame_Location = tk.Frame(root, bg=_bg,          relief="groove", borderwidth=0)

        self.lbl_SiteNum     = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="e",           text="Site")
        self.lbl_SiteSep     = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w",           text=": ")
        self.lbl_Lat         = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="e", width=5,  text="Lat:")
        self.lbl_Lon         = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="e", width=5,  text="Lon:")
        self.lbl_UTCoffset2  = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="e", width=10, text="UTC offset:")
        self.val_SiteNum     = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_SiteNum"]  )
        self.val_SiteName    = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_SiteName"] )
        self.val_Lat         = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_Lat"]      )
        self.val_Lon         = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_Lon"]      )
        self.val_UTCoffset2  = tk.Label(self.frame_Location, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_UTCoffset"])


        self.frame_Comms    = tk.Frame(root, bg=_bg, height=20 )

        _pad=2;    _size=9;     _font="sans"
        self.lbl_Connection = tk.Label(self.frame_Comms, bg=_bg, fg=_fg, anchor="e", textvariable=self.app_data["var_lbl_Connection"], font=(_font, _size))
        self.val_OnStep     = tk.Label(self.frame_Comms, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_OnStep"], font=(_font, _size), padx=_pad)
        self.val_Date       = tk.Label(self.frame_Comms, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_DisplayDate"], font=(_font, _size), padx=_pad)
        self.val_Pulse      = tk.Label(self.frame_Comms, bg=_bg, fg=_fg, anchor="w", textvariable = self.app_data["var_Pulse"], font=(_font, _size), padx=_pad)
        #val_OnStep = "Connected to OnStep at {}".format(comms.COMM)


        self.frame_WARNING.grid( row=row_Warning , sticky="nsew", padx=4, pady=4)
        self.frame_ERROR.grid(   row=row_ERROR   , sticky="nsew", padx=4, pady=4)
        self.frame_COORD.grid(   row=row_Coord   , sticky="nsew",  padx=4, pady=4)
        self.frame_Time.grid(    row=row_Time    , sticky="nsew",  padx=4, pady=4)
        self.frame_Status.grid(  row=row_Status  , sticky="nsw",  padx=4, pady=4)
        self.frame_GROUP1.grid(  row=row_GROUP1  , sticky="ne", padx=4, pady=4)
        self.frame_Location.grid(row=row_Loc     , sticky="nsew", padx=4, pady=4)
        self.frame_Comms.grid(   row=row_Comms   , sticky="nsew")

        self.WARNING.grid()
        self.ERROR.grid()

        #layout widgets for COORDS frame
        self.frame_Coord_a.grid(row=0, sticky="w")

        this_row = 0
        self.lbl_LastError.grid(  row=this_row, sticky="nsew", column=0)
        self.val_LastError.grid(  row=this_row, sticky="nsew", column=1)
        self.lbl_MountStatus.grid(row=this_row, sticky="nsew", column=2)
        self.val_MountStatus.grid(row=this_row, sticky="nsew", column=3)
        this_row+=1
        self.lbl_Tracking.grid(  row=this_row, sticky="nsew", column=0)
        self.val_Tracking.grid(  row=this_row, sticky="nsew", column=1)
        self.lbl_GTobject.grid(  row=this_row, sticky="nsew", column=2)
        self.val_GTobject.grid(  row=this_row, sticky="nsew", column=3)

        self.frame_Coord_b.grid(row=1, sticky="w")

        this_row+=1
        self.lbl_RA.grid(        sticky = "nsew", row=this_row, column=0)
        self.val_RA.grid(        sticky = "nsew", row=this_row, column=1)
        self.lbl_ALT.grid(       sticky = "nsew", row=this_row, column=2)
        self.val_ALT.grid(       sticky = "nsew", row=this_row, column=3)
        self.lbl_ra_symbol.grid( sticky = "nsew", row=this_row, column=4)
        self.val_TargetRA.grid(  sticky = "nsew", row=this_row, column=5)

        this_row+=1
        self.lbl_DEC.grid(        sticky = "nsew", row=this_row, column=0)
        self.val_DEC.grid(        sticky = "nsew", row=this_row, column=1)
        self.lbl_AZ.grid(         sticky = "nsew", row=this_row, column=2)
        self.val_AZ.grid(         sticky = "nsew", row=this_row, column=3)
        self.lbl_dec_symbol.grid( sticky = "nsew", row=this_row, column=4)
        self.val_TargetDEC.grid(  sticky = "nsew", row=this_row, column=5)


        #layout widgets for TIMES frame
        this_row = 0
        self.lbl_LST.grid(       sticky = "nsew", row=this_row, column=0)
        self.lbl_OnStepTime.grid(sticky = "nsew", row=this_row, column=1)
        self.lbl_UTCoffset.grid( sticky = "nsew", row=this_row, column=2)
        self.lbl_UTC.grid(       sticky = "nsew", row=this_row, column=3)
        self.lbl_TZoffset.grid(  sticky = "nsew", row=this_row, column=4)
        self.lbl_SysClock.grid(  sticky = "nsew", row=this_row, column=5)
        self.lbl_TZcode.grid(    sticky = "nsew", row=this_row, column=6)
        this_row += 1
        self.val_LST.grid(       sticky = "nsew", row=this_row, column=0)
        self.val_OnStepTime.grid(sticky = "nsew", row=this_row, column=1)
        self.val_UTCoffset.grid( sticky = "nsew", row=this_row, column=2)
        self.val_UTC.grid(       sticky = "nsew", row=this_row, column=3)
        self.val_TZoffset.grid(  sticky = "nsew", row=this_row, column=4)
        self.val_SysClock.grid(  sticky = "nsew", row=this_row, column=5)
        self.val_TZcode.grid(    sticky = "nsew", row=this_row, column=6)


        #layout widgets for STATUS frame
        this_row = 0
        self.lbl_MountType.grid(row=this_row, column=0)
        self.val_MountType.grid(row=this_row, column=1)
        this_row += 1
        self.lbl_Parked.grid(   row=this_row, column=0)
        self.val_Parked.grid(   row=this_row, column=1)
        this_row += 1
        self.lbl_AtHome.grid(   row=this_row, column=0)
        self.val_AtHome.grid(   row=this_row, column=1)
        this_row += 1
        self.lbl_Slewing.grid(  row=this_row, column=0)
        self.val_Slewing.grid(  row=this_row, column=1)
        this_row += 1
        self.lbl_PierSide.grid( row=this_row, column=0)
        self.val_PierSide.grid( row=this_row, column=1)
        this_row += 1
        self.lbl_AutoFlip.grid( row=this_row, column=0)
        self.val_AutoFlip.grid( row=this_row, column=1)
        self.lbl_AFlip_Pos.grid(row=this_row, column=2)
        self.val_PauseHome.grid(row=this_row, column=3)
        self.val_AFlip_pos.grid(row=this_row, column=4)


        self.frame_PEC.grid(row=0, sticky="w")
        #layout widgets for PEC frame
        this_row = 0
        self.lbl_PPS.grid(row=this_row,column=0)
        self.val_PPS.grid(row=this_row,column=1)

        self.lbl_PECrecorded.grid(row=this_row,column=2)
        self.val_PECrecorded.grid(row=this_row,column=3)

        self.lbl_PEC.grid(row=this_row,column=4)
        self.val_PEC.grid(row=this_row,column=5)


        self.frame_Corr.grid(row=1, sticky="w")
        #layout widgets for CORRECTIONS frame
        this_row =0
        self.lbl_ConeCorr.grid(row=this_row, column=0)
        self.val_ConeCorr.grid(row=this_row, column=1)
        self.lbl_AltCorr.grid( row=this_row, column=2)
        self.val_AltCorr.grid( row=this_row, column=3)
        self.lbl_AzCorr.grid(  row=this_row, column=4)
        self.val_AzCorr.grid(  row=this_row, column=5)


        self.frame_Backlash.grid(row=2, sticky="w")
        #layout widgets for BACKLASH frame
        this_row =0
        self.lbl_Backlash1.grid(row=this_row, column=0)
        self.val_Backlash1.grid(row=this_row, column=1)
        self.lbl_Backlash2.grid(row=this_row, column=2)
        self.val_Backlash2.grid(row=this_row, column=3)


        self.frame_Limits1.grid(row=3, sticky="w")
        #layout widgets for LIMITS frame
        this_row = 0
        self.lbl_Overhead.grid(row=this_row, column=0)
        self.val_Overhead.grid(row=this_row, column=1)
        self.lbl_Horizon.grid( row=this_row, column=2)
        self.val_Horizon.grid( row=this_row, column=3)

        self.frame_Limits2.grid(row=4, sticky="w")

        self.lbl_PastE.grid(   row=this_row, column=0)
        self.val_PastE.grid(   row=this_row, column=1)
        self.lbl_PastW.grid(   row=this_row, column=2)
        self.val_PastW.grid(   row=this_row, column=3)


        #layout widgets for LOCATION frame
        self.lbl_SiteNum.grid(   row=this_row, column=0)
        self.val_SiteNum.grid(   row=this_row, column=1)
        self.lbl_SiteSep.grid(   row=this_row, column=2)
        self.val_SiteName.grid(  row=this_row, column=3)
        self.lbl_Lat.grid(       row=this_row, column=4)
        self.val_Lat.grid(       row=this_row, column=5)
        self.lbl_Lon.grid(       row=this_row, column=6)
        self.val_Lon.grid(       row=this_row, column=7)
        self.lbl_UTCoffset2.grid(row=this_row, column=8)
        self.val_UTCoffset2.grid(row=this_row, column=9)


        #layout widgets for COMMS frame
        self.lbl_Connection.grid(row=row_Comms, column=0)
        self.val_OnStep.grid(    row=row_Comms, column=1)
        self.val_Date.grid(      row=row_Comms, column=2)
        self.val_Pulse.grid(     row=row_Comms, column=3)


        '''
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

        #     finally, the actual programming!

             - get the Menubar (mostly disabled)
             - update the clock
             - establish connection to an OnStep
             - verify OnStep and Host times in sync
             - enable all menu items
             - define, init, and start the update 'loops'

        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

        these functions are all defined within and called (once only!) from inside "__init__"

        those that end with .after() loop independently, with various delays
        those that don't have an .after() are called as needed

        '''

        from menubar import Menubar
        # Main Window Menu Bar
        self.mb_fl,  self.mb_ed,  self.mb_al,  self.mb_ct,  self.mb_st, self.mb_tl,\
        self.mb_hp, self.mb_stop, self.mb_mb = Menubar.mb(self, self.parent, self.controller)
        # the mb_xx objects help when activating/de-activating menu items

        def update_clock():
            ''' update the on-screen clock '''
            self.now = time.strftime("%H:%M:%S")
            self.app_data["var_SysClock"].set(self.now)
            self.after(1000, update_clock) # x1-ish second

        #start updating the system time display
        update_clock()

        def initial_connection():
            """establish the initial connection to OnStep """
            HOST = self.app_data["var_Host"].get()
            PORT = self.app_data["var_Port"].get()

            """ Wait for the User to select a Host, re-try every 3 seconds """
            if HOST == 'none' or PORT == 'none':
                self.connection_cancel = root.after(3000, initial_connection)
            else:
                """ A HOST HAS BEEN CHOSEN! """
                # stop re-trying 'initial_connection'
                root.after_cancel(self.connection_cancel)

                # onstep.py in the LX200 folder is full of cool functions
                import lx200.onstep as onstep

                # creates a Python object named "scope" that allows us to talk to OnStep
                self.scope = onstep.onstep(host = HOST, port = PORT)

                self.scope.update_status() # freshen the status variables of OnStep

                ONSTEP = self.scope.get_version()
                app_title="OnStep Control Console v{} -- {} -- OnStep v{}".format(CONSOLE_VERSION,PLATFORM,ONSTEP)
                root.wm_title(app_title)

                self.controller.app_data["var_lbl_Connection"].set("Connected to OnStep at: ")

                self.app_data["var_MountType"].set(self.scope.type)

                info='Connected to OnStep at {}'.format(self.app_data["var_OnStep"].get())
                logging.info(info)

                # Set some initial values -- these are not updated in a loop
                update_location()
                update_displayDate()
                update_time_offsets()
                self.app_data["var_GTobject"].set(" - - ")
                ra = self.scope.get_target_ra()
                de = self.scope.get_target_de()
                if ra.startswith('00:00:00'): ra = ''
                if de.startswith('+00*00:00'):de = ''
                self.app_data["var_TargetRA"].set(ra)
                self.app_data["var_TargetDEC"].set(de)

                # re-Enable the rest of the (disabled) Menu choices in
                # the Align, Control, Tools, and Settings menus
                self.mb_al.entryconfig("Alignment Stars", state="normal")
                label_text = "{:<20}{:>8}".format('n-Star Align','-->>')
                self.mb_al.entryconfig(label_text,    state="normal")
                self.mb_al.entryconfig("Manual Align",    state="normal")
                label_text = "{:<20}{:>8}".format('Refine Polar','-->>')
                self.mb_al.entryconfig(label_text,    state="normal")
                self.mb_al.entryconfig("Sync now",        state="normal")

                label_text = "{:<20}{:>8}".format('Motion Controls','-->>')
                self.mb_ct.entryconfig(label_text, state="normal")
                label_text = "{:<20}{:>8}".format('Go-To Object','-->>')
                self.mb_ct.entryconfig(label_text, state="normal")
                self.mb_ct.entryconfig("Enter Coords", state="normal")
                self.mb_ct.entryconfig("Return to Target", state="normal")
                if self.scope.is_tracking:
                    self.app_data["var_IsTracking"].set(1)
                else:
                    self.app_data["var_IsTracking"].set(0)
                self.mb_ct.entryconfig("Tracking on/off", state="normal")
                self.mb_ct.entryconfig("ABORT", state="normal")
                self.mb_ct.entryconfig("HOME", state="normal")
                self.mb_ct.entryconfig("Home reset", state="normal")
                self.mb_ct.entryconfig("PARK", state="normal")
                self.mb_ct.entryconfig("UN-Park", state="normal")
                self.mb_ct.entryconfig("Park set", state="normal")
                self.mb_ct.entryconfig("Meridian Flip now",    state="normal")
                self.mb_ct.entryconfig("Meridian Flip continue", state="normal")

                #self.mb_mb.entryconfig(' ! STOP ! ', state="normal")
                self.mb_stop.entryconfig('!', state="normal")

                self.mb_st.entryconfig("Connection", state="normal")
                label_text = "{:<20}{:>8}".format('Guide Rate','-->>')
                self.mb_st.entryconfig(label_text, state="normal")
                self.app_data['var_Guide_Rate'].set('1x')

                label_text = "{:<20}{:>8}".format('Max Slew','-->>')
                self.mb_st.entryconfig(label_text, state="normal")
                self.app_data['var_Slew_Max'].set('1')

                self.mb_st.entryconfig("OnStep Time", state="normal")
                self.mb_st.entryconfig("Location", state="normal")
                label_text = "{:<20}{:>8}".format('Limits'+u"\u2001"+u"\u2001",'-->>') ## two EM Quads to push the arrows over
                self.mb_st.entryconfig(label_text, state="normal")
                self.mb_st.entryconfig("Backlash", state="normal")
                label_text = "{:<20}{:>8}".format('Tune Backlash','-->>')
                self.mb_st.entryconfig(label_text, state="normal")
                if self.scope.auto_flip:
                    self.app_data["var_AutoFlip"].set('On')
                    self.app_data["var_AFlip_State"].set(1)
                else:
                    self.app_data["var_AutoFlip"].set('off')
                    self.app_data["var_AFlip_State"].set(0)
                self.mb_st.entryconfig("Meridian Flip Auto", state="normal")
                if self.scope.pause_at_home:
                    self.app_data["var_PauseHome"].set('On')
                    self.app_data["var_Pause_State"].set(1)
                else:
                    self.app_data["var_PauseHome"].set('off')
                    self.app_data["var_Pause_State"].set(0)
                self.mb_st.entryconfig("AutoFlip Pause Home", state="normal")

                self.mb_tl.entryconfig("Stress test", state="normal")
                ## borked with OnStepX
                #self.mb_tl.entryconfig("Drift test", state="normal")

                # start up the time update # ~ every second-ish
                update_times()
                '''root.after_cancel(self.times_cancel) # to kill it'''

                # start up the stats update # every 3 seconds
                update_stats()
                '''root.after_cancel(self.stats_cancel) # to kill it'''

                # start up the coordinates update # every half-second
                update_coords()
                '''root.after_cancel(self.coords_cancel) # to kill it'''

                # start up the LST update # x almost each second
                update_lst()
                '''root.after_cancel(self.lst_cancel) # to kill it'''

                self.reset_Warning()
                '''root.after_cancel(self.warning_reset_cancel) # to kill it'''

                self.reset_Error()
                '''root.after_cancel(self.error_reset_cancel) # to kill it'''
        # END OF initial_connection()

        """ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ """
        """ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ """

        """   THIS IS THE ENTRY-POINT OF THE PROGRAM    """

        """ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ """
        """ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ """
        # watch for HOST selection, then attempt a connection
        self.connection_cancel = root.after(3000, initial_connection)


        def update_coords():
            """keep coordinates and time updated """
            self.app_data["var_RA"].set(  self.scope.get_ra()  )
            self.app_data["var_DEC"].set( self.scope.get_de()  )
            self.app_data["var_ALT"].set( self.scope.get_alt() )
            self.app_data["var_AZ"].set(  self.scope.get_azm() )

            self.coords_cancel = root.after(500, update_coords) # every half second
            '''root.after_cancel(self.coords_cancel) # to kill it'''


        HMS = '%H:%M:%S'
        MDY = '%m/%d/%y'
        YMD = '%Y-%m-%d'

        def update_location():
            '''retrieve the mount's physical location from the OnStep controller'''
            global LAT, LON
            LAT = self.scope.get_latitude()
            LON = self.scope.get_longitude()

        def update_displayDate():
            '''current date'''
            global str_DisplayDate, str_ScopeDate
            str_ScopeDate = DateTime.strftime(DateTime.strptime(self.scope.get_date(), MDY), YMD)
            ## convert from "mm/dd/yy" to "DoW, yyyy-MON-dd"
            str_DisplayDate = DateTime.strftime(DateTime.strptime(self.scope.get_date(), MDY), "%a, %Y-%b-%d")
            self.app_data["var_DisplayDate"].set(str_DisplayDate)

        def update_time_offsets():
            '''UTC offset, TZ offset, TZ code (dst or not)'''
            global  str_UTC_OFFSET,  float_UTC_OFFSET,  TZ_OFFSET,  TZ_CODE
            str_UTC_OFFSET = self.scope.get_utc()
            float_UTC_OFFSET = conversion.hms_To_float(str_UTC_OFFSET)
            TZ_OFFSET, TZ_CODE = self.scope.get_TZoffset()
            TZ_CODE = '('+TZ_CODE+')'

        def update_lst():
            '''fetch LST from controller and display it'''
            self.app_data["var_LST"].set(self.scope.get_sidereal())
            self.lst_cancel = root.after(940, update_lst) # every second-ish

        def check_time():
            '''checks if the OnStep time is wildly out-of-sync'''
            '''
                if system time and controller time are off by more than 20 minutes (1200 seconds),
                print a reminder to check the time (and maybe re-init the controller)

                does NOT init by default, in case there's a reason not to
            '''
            dt_ChekTime = dt_OnStepTime + TimeDelta( hours=(float_UTC_OFFSET + TZ_OFFSET) )
            if dt_SystemTime > dt_ChekTime:
                tdelta = abs( int( TimeDelta(seconds=(dt_SystemTime - dt_ChekTime).seconds).total_seconds() ) ) % 86400
            else:
                tdelta = abs( int( TimeDelta(seconds=(dt_ChekTime - dt_SystemTime).seconds).total_seconds() ) ) % 86400
            #print(config.CUR_POS.format(config.TIME_LINE+1,74), end='');  print('{}'.format(tdelta), end="")
            return tdelta

        def update_times():
            """Local Sidereal Time, Coordinated Universal Time, TimeZone Offset"""
            #had to declare these two as globals, or "run_repeatedly()" wouldn't work
            global dt_OnStepTime, dt_SystemTime
            global do_time_display
            do_time_display = False
            ##   nine_hours_from_now = DateTime.now() + TimeDelta(hours=9)
            ##   scope time is 'str_UTC_OFFSET hours' behind UTC
            dt_SystemTime = DateTime.now()
            # for some reason, OnStep counts time to 24:00:00 (for just one second!) and then
            # resets to 00:00:01 -- so we have to test for 2400 hours all the live-long frikken day
            # because Python only accepts 0 to 23:59:59
            the_time = self.scope.get_time()
            str_OnStepTime = the_time if the_time < '24:00:00' else '00:00:00'
            dt_OnStepTime = DateTime.strptime(str_ScopeDate+' '+str_OnStepTime, YMD+' '+HMS)
            UTC = DateTime.strftime(dt_OnStepTime + TimeDelta(hours=(float_UTC_OFFSET)), HMS)
            #if tdelta < 1200:   #tdelta comes from check_time() every 20 minutes
            #self.app_data["var_LST"].set(LST)
            self.app_data["var_OnStepTime"].set(str_OnStepTime)
            self.app_data["var_UTCoffset"].set(str_UTC_OFFSET)
            self.app_data["var_UTC"].set(UTC)
            self.app_data["var_TZoffset"].set(TZ_OFFSET)
            self.app_data["var_TZcode"].set(TZ_CODE)

            self.times_cancel = root.after(980, update_times)

        self.GUIDE_RATE = ('0.25x', '0.5x', '1x', '2x', '4x', '8x', '20x', '48x', 'half', 'max')
        self.TRACKING_RATE = ('sid','lun','sol','kng','SID','LUN','SOL','KNG')
        self.STATUS = ('Needs alignment', '1-star aligned', '2-star aligned', '3-star aligned', 'unavailable')

        def update_stats():
            """update status items """
            #toggles the star when status area is updated
            var = self.app_data["var_Pulse"].get()
            if var == " *":
                self.app_data["var_Pulse"].set("")
            else:
                self.app_data["var_Pulse"].set(" *")

            self.scope.update_status()
            self.app_data["var_Parked"].set(  'YES   <--' if self.scope.is_parked   else 'no')
            self.app_data["var_AtHome"].set(  'YES   <--' if self.scope.is_home     else 'no')
            self.app_data["var_Slewing"].set( 'YES   <--' if self.scope.is_slewing  else 'no')
            self.app_data["var_PierSide"].set( str(self.scope.pier_side) )

            if self.scope.auto_flip:
                self.app_data["var_AutoFlip"].set('On')
                self.app_data["var_AFlip_State"].set(1)
            else:
                self.app_data["var_AutoFlip"].set('off')
                self.app_data["var_AFlip_State"].set(0)

            if self.scope.pause_at_home:
                self.app_data["var_PauseHome"].set('On')
                self.app_data["var_Pause_State"].set(1)
            else:
                self.app_data["var_PauseHome"].set('Off')
                self.app_data["var_Pause_State"].set(0)

            self.app_data["var_AFlip_Pos"].set(self.scope.position)

            x = self.scope.get_last_error()
            self.app_data["var_LastError"].set( 'none' if (int(x)==0) else str(x) )

            status_string = self.scope.get_mount_status()
            if status_string != "0":
                status_string = self.STATUS[int(status_string[2])]
                self.app_data["var_MountStatus"].set( status_string )
            else:
                self.app_data["var_MountStatus"].set(" not aligned ")

            if self.scope.is_tracking:
                a = 'YES'
                """not sure why, but status_bitpacked sometimes returns
                with a value that causes RATES[s] to throw an index-out-
                of-range error...we'll catch it"""
                t_rate = self.scope.status_bitpacked()
                tmp = bytearray(t_rate)
                s = tmp[1] & 127
                try:
                    t_rate = self.TRACKING_RATE[s]
                except IndexError:
                    t_rate = ' ? '
                self.app_data["var_IsTracking"].set(1)
            else:
                a = 'No'
                t_rate = ''
                self.app_data["var_IsTracking"].set(0)
            trk = '{} - {}'.format(a, t_rate)
            self.app_data["var_Tracking"].set( trk )

            self.app_data["var_PEC"].set( self.scope.pec )
            self.app_data["var_PECrecorded"].set( 'Yes' if self.scope.pec_recorded else 'no' )
            self.app_data["var_PPS"].set(  'On' if self.scope.pps else 'off'  )
            ohl = int(self.scope.get_overhead_limit().replace('*',''))
            hor = int(self.scope.get_horizon_limit().replace('*',''))
            alt = int(self.scope.get_alt().split('*')[0]) #whole degrees only
            dec = int(self.scope.get_de().split('*')[0]) #whole degrees only
            if alt - 5 <= hor or dec - 5 <= hor:
                msg='Warning: >near Horizon Limit!< '
                self.controller.DisplayWarning(msg)
            if alt <= hor or dec <= hor:
                msg='ERROR: >HORIZON LIMIT!< '
                self.controller.DisplayError(msg)
            if ohl < 90:
                if alt >= ohl -5:
                    msg='Warning: >near O/head Limit!< '
                    self.controller.DisplayWarning(msg)
                if alt >= ohl:
                    msg='ERROR: >OVERHEAD LIMIT!< '
                    self.controller.DisplayError(msg)
            self.app_data["var_Overhead"].set( ohl )
            self.app_data["var_Horizon"].set(  hor )
            self.app_data["var_ConeCorr"].set( self.scope.get_cor_do()  )
            self.app_data["var_AltCorr"].set(  self.scope.get_cor_alt() )
            self.app_data["var_AzCorr"].set(   self.scope.get_cor_azm() )
            self.app_data["var_Backlash1"].set(self.scope.get_backlash(1) )
            self.app_data["var_Backlash2"].set(self.scope.get_backlash(2) )
            self.app_data["var_PastE"].set(    self.scope.get_degrees_past_E() )
            self.app_data["var_PastW"].set(    self.scope.get_degrees_past_W() )
            # get num (0-3) of currently selected site from eeprom
            site_num = int(self.scope.get_site().replace('#',''))
            self.app_data["var_SiteNum"].set( site_num + 1 )
            #                          get_name command takes 'M' thru 'P' . . . 77 = M
            self.app_data["var_SiteName"].set( self.scope.get_site_name(chr(site_num + 77)).replace('#','') )
            self.app_data["var_Lat"].set(       self.scope.get_latitude()  )
            self.app_data["var_Lon"].set(       self.scope.get_longitude() )
            self.app_data["var_UTCoffset"].set( self.scope.get_utc() )

            # ##self.scope.update_status()
            # print('GX92-get_max_slew() <{}>'.format(self.scope.get_max_slew() ) )
            # print('GX93-get_max_base() <{}>'.format(self.scope.get_max_base() ) )
            # print('GX97-get_speed() <{}>'.format(self.scope.get_slew_speed_max() ) ) ## degrees-per-second
            # print('status.guide_rate <{}>'.format(self.scope.guide_rate ) )
            # print(' ')
            # #self.app_data['var_Slew_Max']

            self.stats_cancel = root.after(3200, update_stats) # x3 seconds
            '''root.after_cancel(self.stats_cancel) # to kill it'''

        #update_status() # called by "initial_connection()"


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        # END of __init__
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    #Functions in Class MainWindow:

    def DisplayWarning(self, msg):
        '''show a brief message on-screen in the Warning zone'''
        self.controller.reset_Warning()
        self.controller.WARNING.config(bg='goldenrod1')
        self.controller.frame_WARNING.config(bg='goldenrod1')
        self.controller.app_data["var_WARNING"].set(msg)
        self.warning_reset_cancel = root.after(12030, self.reset_Warning) # ~12 seconds

    def DisplayError(self, msg):
        '''show a brief message on-screen in the Error zone'''
        self.controller.reset_Error()
        self.controller.ERROR.config(bg='light pink')
        self.controller.frame_ERROR.config(bg='light pink')
        self.controller.app_data["var_ERROR"].set(msg)
        self.error_reset_cancel = root.after(12010, self.reset_Error) # ~12 seconds

        """5000 milliseconds evaluate to 5 seconds."""

    def reset_Warning(self):
        '''clear the Warning zone'''
        self.app_data["var_WARNING"].set("warnings")
        self.WARNING.config(bg='grey')
        self.frame_WARNING.config(bg='grey')

    def reset_Error(self):
        '''clear the Error zone'''
        self.app_data["var_ERROR"].set("errors")
        self.ERROR.config(bg='grey')
        self.frame_ERROR.config(bg='grey')


    def _exit(self):
        '''adds a log entry on our way out'''
        logging.info(f'Exiting on user input')
        exit()



if __name__ == "__main__":

    # wh_font_map = {k: v for k, v in zip(range(700, 1980, 60), range(12, 32))}
    # print(wh_font_map)
    # def change_font(event):
    #     font_size = wh_font_map[next(k for k in wh_font_map if (root.winfo_width() + root.winfo_height()) / 2 <= k)]
    #     root.def_font.config(size=font_size)
    #     print("{}  ".format(font_size), end='')

    root = tk.Tk()
    # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # sw = int(w*0.270)
    # sh = int(h*0.520)
    # dims = 'w{}| h{}| sw{}| sh{}|'.format(w,h,sw,sh)
    # root.geometry("%dx%d+0+0" % (sw,sh))
    # root.minsize(700, 450)
    root.geometry("%dx%d+0+0" % (820,520))
    root.minsize(700, 450)
    root.configure(background='black', bd=6, relief='sunken')
    root.option_add('*tearOff', False)

    app = MainWindow(root)
    ## TkDefaultFont, TkTextFont, TkFixedFont
    app.def_font = tk.font.nametofont("TkDefaultFont")
    app.def_font.config(size=15)
    # app.bind("<Configure>", change_font)

    PLATFORM = root.tk.call('tk', 'windowingsystem')     # will return x11, win32 or aqua
    app_title="OnStep Control Console v{} -- {} -- OnStep v{}".format(CONSOLE_VERSION, PLATFORM, ONSTEP)
    #root.wm_title(app_title)
    root.wm_title(app_title)
    #WindowTitle.set(app_title)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    app.mainloop()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## EOF
