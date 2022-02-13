#!/usr/bin/env python3
'''      BACKLASH TUNING DIALOG
'''
import time
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from messagebox_dark import AskOkCancel_Dark
from messagebox_dark import AskYesNo_Dark
from messagebox_dark import ShowInfo_Dark

_bg='gray19'
_fg='tomato'
params = [   ('East', 'w', 'East & West'),    ('South', 'n', 'North & South'),    ]


class Tune_Backlash:

    """revert to the old setting anytime user bails"""
    def _EXIT(self, parent, controller, axis):
        def __init__(self, parent, controller):
            self.parent = parent
            self.controller = controller
        self.axis=axis # "R/A" or "DEC"
        int_axis = 1
        if self.axis == "DEC": int_axis = 2
        self.controller.scope.set_backlash(int_axis,self.old_backlash)


    def tune_backlash1(self, parent, controller, axis):

        def __init__(self, parent, controller):
            self.parent = parent
            self.controller = controller

        self.axis=axis # "R/A" or "DEC"
        int_axis = 1
        if self.axis == "DEC": int_axis = 2
        MAX = self.controller.scope.max_backlash

        self.controller.scope.update_status()

        if self.controller.scope.is_parked is True: self.controller.scope.un_park()
        self.controller.scope.tracking_off()

        button = params[int_axis-1][0]
        direction = params[int_axis-1][1]
        testing = params[int_axis-1][2]

        self.old_backlash = self.controller.scope.get_backlash(int_axis)   # save current setting

        self.controller.scope.set_backlash(int_axis, 0) # zero it out

        window_title='Current Axis{} ({}) backlash: {} arc seconds'.format(int_axis, self.axis, self.old_backlash)

        msg_info = '''
Please do the following:\n
1. Slew the scope to a terrestrial object.  It should be\n
   fairly distant, and must be stationary.\n
2. Center the object carefully. Use a cross-hair eyepiece.\n
3. You must End the motion with the "{}" button.\n
\nPress "OK" when done.'''.format(button)
        ## answer = messagebox.askokcancel(window_title, msg_info)
        answer = AskOkCancel_Dark(parent, window_title, msg_info)
        if answer is False:
            Tune_Backlash._EXIT(self, parent, controller, int_axis)
            return

        self.controller.scope.set_speed('1x') # Set to low speed

        msg_info = 'When you press "OK", the scope will move\naway from the object for approximately\n15 seconds.'
        answer = AskOkCancel_Dark(parent, window_title, msg_info)
        if answer is False:
            Tune_Backlash._EXIT(self, parent, controller, int_axis)
            return

        pos1 = self.controller.scope.get_ax_motor_pos(int_axis)  # Get Start position

        self.controller.scope.move(direction)                # Move in the set direction

        # Time for about 240 arc seconds @ 1X 15"/sec, which should be enough for the worst backlash
        time.sleep(16)
        self.controller.scope.stop()

        msg_info = 'Now move the object back, centering it\nperfectly, using only the "{}" button.\n\nPress "OK" when done.'.format(button)
        answer = AskOkCancel_Dark(parent, window_title, msg_info)
        if answer is False:
            Tune_Backlash._EXIT(self, parent, controller, int_axis)
            return

        pos2 = self.controller.scope.get_ax_motor_pos(int_axis)   # Get position after movement
        spd = int(self.controller.scope.get_spd(int_axis))        # Get steps per degree
        steps = abs(float(pos1) - float(pos2))       # Calculate the backlash value
        backlash = round((steps * 3600) / spd)

        if backlash <= MAX:
            msg_info = 'Calculated backlash: {} arc seconds\n'.format(backlash)
            msg_info += '\nSetting backlash to calculated value\n'
            answer = AskOkCancel_Dark(parent, window_title, msg_info)
            if answer is False:
                Tune_Backlash._EXIT(self, parent, controller, int_axis)
                return
            self.controller.scope.set_backlash(int_axis, backlash)
            msg_info = 'Now test the {} axis by slewing back and forth,\n{}, and observing no jumps or lags.'.format(self.axis, testing)
            ShowInfo_Dark(parent, 'Operation Completed', msg_info)
        else:
            msg_info = 'Error: value exceeds Maximum of {}\n'.format(MAX)
            msg_info += 'This mount needs some further adjustment!\n'
            msg_info += '\nRevert Axis{} to previous backlash setting?'.format(int_axis)
            answer = AskYesNo_Dark(parent, 'Limit Exceeded', msg_info)
            if answer == 'Yes':
                self.controller.scope.set_backlash(int_axis, self.old_backlash)
            else:
                msg_info = 'Setting backlash for Axis{} to zero\n'.format(int_axis)
                ShowInfo_Dark(parent, 'Setting Cleared', msg_info)
                self.controller.scope.set_backlash(int_axis, 0)
