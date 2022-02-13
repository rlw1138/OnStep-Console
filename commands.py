''' various command methods '''

import tkinter as tk
from tkinter import scrolledtext
import time
from datetime import datetime
import logging
from slew import Slew


class Commands:

    def movement(self, parent, controller):
        '''
        displays a "control pad" of buttons

        moves North, NorthEast, East, SouthEast,
        South, SouthWest, West, NorthWest
        '''
        self.parent = parent
        self.controller = controller

        def _EXIT():
            self.controller.scope.stop()
            self.pop.destroy()

        def _HALT(event=None):
            self.controller.scope.stop()
            self.PRESSED = None
            self.btn_TOP.config(         bg='brown4', )
            self.btn_BOTTOM.config(      bg='brown4', )
            self.btn_RIGHT.config(       bg='brown4', )
            self.btn_LEFT.config(        bg='brown4', )
            self.btn_TOP_RIGHT.config(   bg='brown4', )
            self.btn_TOP_LEFT.config(    bg='brown4', )
            self.btn_BOTTOM_RIGHT.config(bg='brown4', )
            self.btn_BOTTOM_LEFT.config( bg='brown4', )

        _bg='grey20'

        self.TOP            = 'n'
        self.TOP_LEFT_1     = 'n'
        self.TOP_LEFT_2     = 'w'
        self.TOP_RIGHT_1    = 'n'
        self.TOP_RIGHT_2    = 'e'
        self.BOTTOM         = 's'
        self.BOTTOM_LEFT_1  = 's'
        self.BOTTOM_LEFT_2  = 'w'
        self.BOTTOM_RIGHT_1 = 's'
        self.BOTTOM_RIGHT_2 = 'e'
        self.LEFT           = 'w'
        self.RIGHT          = 'e'

        self.PRESSED = None

        def clicked():
            self.btn_TOP.config(         bg=_bg, )
            self.btn_BOTTOM.config(      bg=_bg, )
            self.btn_RIGHT.config(       bg=_bg, )
            self.btn_LEFT.config(        bg=_bg, )
            self.btn_TOP_RIGHT.config(   bg=_bg, )
            self.btn_TOP_LEFT.config(    bg=_bg, )
            self.btn_BOTTOM_RIGHT.config(bg=_bg, )
            self.btn_BOTTOM_LEFT.config( bg=_bg, )

            self.PRESSED.config(bg='orangeRed4')


        def _TOP_LEFT():
            self.controller.scope.move(self.TOP_LEFT_1)
            self.controller.scope.move(self.TOP_LEFT_2)
            self.PRESSED=self.btn_TOP_LEFT
            clicked()

        def _TOP_RIGHT():
            self.controller.scope.move(self.TOP_RIGHT_1)
            self.controller.scope.move(self.TOP_RIGHT_2)
            self.PRESSED=self.btn_TOP_RIGHT
            clicked()

        def _BOTTOM_LEFT():
            self.controller.scope.move(self.BOTTOM_LEFT_1)
            self.controller.scope.move(self.BOTTOM_LEFT_2)
            self.PRESSED=self.btn_BOTTOM_LEFT
            clicked()

        def _BOTTOM_RIGHT():
            self.controller.scope.move(self.BOTTOM_RIGHT_1)
            self.controller.scope.move(self.BOTTOM_RIGHT_2)
            self.PRESSED=self.btn_BOTTOM_RIGHT
            clicked()

        def _TOP():
            self.controller.scope.move(self.TOP)
            self.PRESSED=self.btn_TOP
            clicked()

        def _LEFT():
            self.controller.scope.move(self.LEFT)
            self.PRESSED=self.btn_LEFT
            clicked()

        def _RIGHT():
            self.controller.scope.move(self.RIGHT)
            self.PRESSED=self.btn_RIGHT
            clicked()

        def _BOTTOM():
            self.controller.scope.move(self.BOTTOM)
            self.PRESSED=self.btn_BOTTOM
            clicked()

        def fix_corners():
            _HALT()
            self.btn_TOP_LEFT['text']    =(self.TOP.upper() +  self.TOP_LEFT_2.upper())
            self.btn_TOP_RIGHT['text']   =(self.TOP.upper() +  self.TOP_RIGHT_2.upper())
            self.btn_BOTTOM_LEFT['text'] =(self.BOTTOM.upper()+self.BOTTOM_LEFT_2.upper())
            self.btn_BOTTOM_RIGHT['text']=(self.BOTTOM.upper()+self.BOTTOM_RIGHT_2.upper())

        def swap_NS():
            if self.TOP=='n':
                self.TOP            = 's'
                self.TOP_LEFT_1     = 's'
                self.TOP_RIGHT_1    = 's'
                self.BOTTOM         = 'n'
                self.BOTTOM_LEFT_1  = 'n'
                self.BOTTOM_RIGHT_1 = 'n'
                self.btn_TOP['text']        =('South')
                self.btn_BOTTOM['text']     =('North')
                self.btn_swapNS.config(bg='goldenrod3')
            else:
                self.TOP            = 'n'
                self.TOP_LEFT_1     = 'n'
                self.TOP_RIGHT_1    = 'n'
                self.BOTTOM         = 's'
                self.BOTTOM_LEFT_1  = 's'
                self.BOTTOM_RIGHT_1 = 's'
                self.btn_TOP['text']        =('North')
                self.btn_BOTTOM['text']     =('South')
                self.btn_swapNS.config(bg='brown4')
            fix_corners()

        def swap_EW():
            if self.LEFT=='w':
                self.TOP_LEFT_2     = 'e'
                self.BOTTOM_LEFT_2  = 'e'
                self.LEFT           = 'e'
                self.TOP_RIGHT_2    = 'w'
                self.BOTTOM_RIGHT_2 = 'w'
                self.RIGHT          = 'w'
                self.btn_LEFT['text']       =('East')
                self.btn_RIGHT['text']      =('West')
                self.btn_swapEW.config(bg='goldenrod3')
            else:
                self.TOP_LEFT_2     = 'w'
                self.BOTTOM_LEFT_2  = 'w'
                self.LEFT           = 'w'
                self.TOP_RIGHT_2    = 'e'
                self.BOTTOM_RIGHT_2 = 'e'
                self.RIGHT          = 'e'
                self.btn_LEFT['text']        =('West')
                self.btn_RIGHT['text']      =('East')
                self.btn_swapEW.config(bg='brown4')
            fix_corners()

        self.rate = 2 ## set guide rate to 1x (default)
        Commands.guide_rate(self, self.parent, self.controller, self.rate)
        ##                       0       1      2     3     4     5      6      7      8       9
        ## self.GUIDE_RATE = ('0.25x', '0.5x', '1x', '2x', '4x', '8x', '20x', '48x', 'half', 'max')

        def _Fast():
            if self.rate <= 8:
                self.rate += 1
                Commands.guide_rate(self, self.parent, self.controller, self.rate)

        def _Slow():
            if self.rate >= 1:
                self.rate -= 1
                Commands.guide_rate(self, self.parent, self.controller, self.rate)


        self.pop = tk.Toplevel()
        self.pop.title("<Space> also stops!")
        self.pop.config(bg=_bg, ) #padx=10, pady=10)
        self.btn_TOP = tk.Button(         self.pop, borderwidth=0, text="North", command=_TOP)
        self.btn_BOTTOM = tk.Button(      self.pop, borderwidth=0, text="South", command=_BOTTOM)
        self.btn_RIGHT = tk.Button(       self.pop, borderwidth=0, text="East",  command=_RIGHT)
        self.btn_LEFT = tk.Button(        self.pop, borderwidth=0, text="West",  command=_LEFT)
        self.btn_TOP_RIGHT = tk.Button(   self.pop, borderwidth=0, text="NE",   command=_TOP_RIGHT)
        self.btn_TOP_LEFT = tk.Button(    self.pop, borderwidth=0, text="NW",   command=_TOP_LEFT)
        self.btn_BOTTOM_RIGHT = tk.Button(self.pop, borderwidth=0, text="SE",   command=_BOTTOM_RIGHT)
        self.btn_BOTTOM_LEFT = tk.Button( self.pop, borderwidth=0, text="SW",   command=_BOTTOM_LEFT)
        self.btn_halt = tk.Button(self.pop, text="HALT\n<space>",  command=_HALT ) # command=lambda: self.controller.scope.stop())

        self.btn_TOP.config(         width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_BOTTOM.config(      width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_RIGHT.config(       width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_LEFT.config(        width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_TOP_RIGHT.config(   width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_TOP_LEFT.config(    width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_BOTTOM_RIGHT.config(width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_BOTTOM_LEFT.config( width=5, height=3, relief='flat', bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_halt.config(        width=5, height=3, bg='brown4', activebackground='orangeRed3')

        if self.controller.scope.is_tracking == False:
            ##label with # WARNING:
            warning_label = tk.Label(self.pop, text='ERROR: tracking must be ON', width=31, height=5, bg='goldenrod3', fg='brown3')
            warning_label.grid(columnspan=3)
        else:

            self.btn_TOP_LEFT.grid(     row=0, column=0, sticky='nw', ipadx=20, ipady=20, )#pady=10)
            self.btn_TOP.grid(          row=0, column=1, sticky='n' , ipadx=20, ipady=20, )#pady=10)
            self.btn_TOP_RIGHT.grid(    row=0, column=2, sticky='ne', ipadx=20, ipady=20, )#pady=10)
            self.btn_LEFT.grid(         row=1, column=0, sticky='w' , ipadx=20, ipady=20, )#pady=10)
            self.btn_halt.grid(         row=1, column=1, ipadx=10, ipady=10, pady=10 )
            self.btn_RIGHT.grid(        row=1, column=2, sticky='e' , ipadx=20, ipady=20, )#pady=10)
            self.btn_BOTTOM_LEFT.grid(  row=2, column=0, sticky='sw', ipadx=20, ipady=20, )#pady=10)
            self.btn_BOTTOM.grid(       row=2, column=1, sticky='s' , ipadx=20, ipady=20, )#pady=10)
            self.btn_BOTTOM_RIGHT.grid( row=2, column=2, sticky='se', ipadx=20, ipady=20, )#pady=10)

        self.buttonFrame = tk.Frame(self.pop, )
        self.buttonFrame.grid(columnspan=3, padx=10, pady=10)

        self.btn_Slow = tk.Button(self.buttonFrame, text='-', command=_Slow)
        self.btn_Slow.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_Slow.pack(side='left', anchor='sw')

        self.btn_Done = tk.Button(self.buttonFrame, text="Done", command=_EXIT)
        self.btn_Done.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='gold3')
        self.btn_Done.pack(side='left')

        self.btn_swapNS = tk.Button(self.buttonFrame, text="N-S", command=swap_NS)
        self.btn_swapNS.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='gold3')
        self.btn_swapNS.pack(side='left')

        self.btn_swapEW = tk.Button(self.buttonFrame, text="E-W", command=swap_EW)
        self.btn_swapEW.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='gold3')
        self.btn_swapEW.pack(side='left')

        self.btn_Sync = tk.Button(self.buttonFrame, text="Sync", command=lambda: self.controller.scope.sync2target())
        self.btn_Sync.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_Sync.pack(side='left')

        self.btn_Fast = tk.Button(self.buttonFrame, text='+', command=_Fast)
        self.btn_Fast.config(bg='brown4', highlightbackground=_bg, highlightthickness=0, activebackground='orangeRed3')
        self.btn_Fast.pack(side='right', anchor='se')

        self.pop.bind('<Control-C>', self.pop.destroy)
        self.pop.bind('<Escape>', self.pop.destroy)
        self.pop.bind('<space>', _HALT)
    ## movement()


    def guide_rate(self, parent, controller, rate):
        self.parent = parent
        self.controller = controller
        self.rate = rate
        speed = self.controller.GUIDE_RATE[self.rate]
        self.controller.scope.set_speed(speed)
        self.controller.app_data["var_Guide_Rate"].set(speed)


    def slew_speed_max(self, parent, controller, rate):
        self.parent = parent
        self.controller = controller
        self.rate = rate ## 1 <= rate <= 5

        self.controller.scope.set_slew_speed_max(self.rate)
        self.controller.app_data["var_Slew_Max"].set(self.rate)


    def accept_align(self, parent, controller):
        '''confirm an alignment point'''
        self.parent = parent
        self.controller=controller
        ret = self.scope.align_accept()
        if ret == 0:
            msg='ERROR: align point FAILED'
            self.controller.DisplayError(msg)
            logging.error(msg.replace("\n", ""))


    def slew_polar(self, parent, controller):
        '''slew to the assumed position of a celestial target'''
        self.parent = parent
        self.controller=controller
        rc, error = self.scope.slew_polar()
        if rc != '0':
            msg='''Slew to assumed position failed -- rc: {} -- Error: {}'''.format(rc, error)
            self.controller.DisplayError(msg)
            logging.error(msg.replace("\n", ""))


    def alignment_stars(self, header):
        """best stars for where / when you are """
        ##this is actually just the window, to hold the output from align_stars()
        _bg='grey'
        self.pop = tk.Toplevel()
        self.pop.title("Best Alignment Stars for current location & time")
        self.pop.config(bg=_bg, padx=10, pady=10)
        lat = self.app_data["var_Lat"].get()
        lst = self.app_data["var_LST"].get()

        import align_stars
        all_valid_stars = align_stars.align_stars(lst, lat, header)

        self.scroll_txt = scrolledtext.ScrolledText(self.pop, undo=True)
        self.scroll_txt.config(bg='black', fg='red')
        self.scroll_txt.insert(tk.INSERT, all_valid_stars)
        self.scroll_txt['font'] = ('consolas', '12')
        self.scroll_txt.pack(expand=True, fill='both')



    """ DIALOGS """

    '''
    Drift Test was broken by OnStepX
            OnStepX no longer responds to the :GXFE# command in get_debug_equ()
    '''

    def drift_test(self, parent, controller):
        """Monitors motor position relative to time, to calculate axis 'drift' from ideal"""
        self.parent = parent
        self.controller=controller

        def _EXIT(file, FILE_PATH):
                    file.close()
                    FMT = '\n Data saved to self.file {} \n'
                    RESULT += FMT.format(FILE_PATH)
                    return RESULT

        def stop(event=None):
            self.bail_out = True
            Slew.abort(self, self.parent, self.controller)
            _EXIT(self.file, self.FILE_PATH)
            #new_thread.terminate()
            button_text = self.button.cget('text')
            print('button text :{}:'.format(button_text))
            if button_text == 'Close': self.pop.destroy()


        _bg='grey19'
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.pop = tk.Toplevel()
        self.pop.attributes('-topmost',True)
        self.pop.geometry("+%d+%d" % (x + 50, y + 50))
        self.pop.title("Tracking Drift test")
        self.pop.config(bg=_bg, padx=10, pady=10)

        self.lbl = tk.Label(self.pop, text=" It will take ~20 minutes to run 1400 iterations... patience please! ")
        self.lbl.config(bg='goldenrod1', fg='black')
        self.lbl.pack()
        self.pop.update_idletasks() # force window to draw

        self.scroll_txt = scrolledtext.ScrolledText(self.pop, undo=True)
        self.scroll_txt.config(bg='black', fg='red')
        self.scroll_txt['font'] = ('consolas', '12')
        self.bail_out = False
        RESULT = FMT = ""
        self.NEWLINE = '\n'
        TIMESTAMP = "{}".format( int( datetime.timestamp( datetime.now() ) ) )
        self.FILE_PATH = "./logs/OnStep_drift-test_"+TIMESTAMP+".txt"
        self.file = open(self.FILE_PATH, 'w+')
        self.controller.scope.update_status()
        if self.controller.scope.is_tracking is False:
            if self.controller.scope.is_parked is True:
                self.controller.scope.un_park()
            else:
                self.controller.scope.tracking_on()
        date = datetime.now().strftime('%Y-%m-%d')
        output = '{}  --  R/A: {}  DEC: {}'.format(date, self.controller.scope.get_ra(), self.controller.scope.get_de())
        RESULT = output+self.NEWLINE
        self.file.write(output+self.NEWLINE)
        self.scroll_txt.insert(tk.INSERT, RESULT)
        self.scroll_txt.pack(expand=True, fill='both')

        self.button = tk.Button(self.pop, text="Stop Motors", command=stop)
        self.button.pack()
        self.pop.bind('<Control-C>', stop)
        self.pop.bind('<Escape>', stop)

        self.pop.update_idletasks() # force window to draw

        ''' enclose the test code in a function '''
        def TheLoop():
            iterations = 1400
            interval = 1
            ra_min = 0.0
            count = 0

            while True:
                if self.bail_out: break
                count += 1
                if count > iterations:
                    logging.info(f"Drift Test completed")
                    _EXIT(self.file, self.FILE_PATH)
                    return
                self.controller.scope.update_status()
                status = 'N/A '
                if self.controller.scope.is_home is True:
                    status = 'Home'
                if self.controller.scope.is_slewing is True:
                    status = 'SLEW'
                if self.controller.scope.is_tracking is True:
                    status = 'TRAK'
                # get_debug_equ() returns coords in decimal
                equ = self.controller.scope.get_debug_equ()
                print('equ :{}:'.format(equ))
                ra = float(equ.split(',')[0])
                de = float(equ.split(',')[1])
                if ra_min == 0.0: # First pass, initialize values
                    ra_min = ra
                    ra_max = ra
                    de_min = de
                    de_max = de
                    time_start = datetime.now()
                    ra_arc_secs = 0.0
                    de_arc_secs = 0.0
                else:
                    # Record maximums and minimums
                    if ra < ra_min:          ra_min = ra
                    if ra > ra_max:          ra_max = ra
                    if de < de_min:          de_min = de
                    if de > de_max:          de_max = de
                    # Calculate elapsed time
                    time_now = datetime.now()
                    elapsed = (time_now - time_start)
                    secs = elapsed.seconds
                    # calculate drift
                    ra_arc_secs = ((ra_max - ra_min) / 0.000278) / (secs / 60)
                    de_arc_secs = ((de_max - de_min) / 0.000278) / (secs / 60)
                #print the title rows, and every 25 rows after
                if count == 1 or count % 25 == 0:
                    output = '{:>5}{}{}'.format(count, ' '*31, '---Drift----  Pier')
                    RESULT = output+self.NEWLINE
                    self.file.write(output+self.NEWLINE)
                    output = ' Time   Status    R/A       DEC      R/A    DEC   Side'
                    RESULT += output+self.NEWLINE
                    self.file.write(output+self.NEWLINE)
                    output = '-------- ---- ---------- ---------  -----  -----  ----'
                    RESULT += output+self.NEWLINE
                    self.file.write(output+self.NEWLINE)
                    self.scroll_txt.insert(tk.INSERT, RESULT)
                    self.pop.update_idletasks() # force window to draw
                _time = datetime.now().strftime('%H:%M:%S')
                output = '{:>8} {:<4} {:10.6f} {:9.6f} {:6.3f} {:6.3f}  {}'.format(_time, status, ra, de, ra_arc_secs, de_arc_secs, self.controller.scope.pier_side)
                RESULT = output+self.NEWLINE
                self.file.write(output+self.NEWLINE)
                self.scroll_txt.insert(tk.INSERT, RESULT)
                self.pop.update_idletasks() # force window to draw
                self.scroll_txt.see(tk.END)
            #wend
        ##TheLoop()

        self.button.config(text="Close")
        #self.controller.scope.return_home()

        ''' run the test code in a new thread '''
        from threading import Thread
        new_thread = Thread(target=TheLoop)
        new_thread.start()

    #drift_test


    def stress_test(self, parent, controller, num_iterations=2):
        """excercises the motors with long slews"""

        #def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        ## if you'd like, you can tweak 'alt' until both motors stop
        ## at the same time....I think it's cooler that way
        '''alt must be signed plus or minus'''
        self.altitude     = '+48:30:00' # looong test
        #altitude     = '+32:00:00' # quick-test

        ''' degrees must have 3 digits: 001, 033, 110, etc '''
        self.azimuth_w = '191:00:00' # looong test
        self.azimuth_e = '169:00:00' # looong test
        # azimuth_w = '019:00:00' # quick test
        # azimuth_e = '341:00:00' # quick test

        import random
        coin_toss = random.randint(1, 2)
        if coin_toss == 1 :
            self.azimuth = self.azimuth_e
        else:
            self.azimuth = self.azimuth_w

        self.poll_duration = 2
        self.tracking_duration = 5
        self.slewing = True
        self.bail_out = False
        text=""

        def msg_update(text):
            try:
                self.scroll_txt.insert(tk.END, text)
                self.scroll_txt.see(tk.END)
                self.scroll_txt.update_idletasks()
            except:
                stop()

        def print_status(text):
            msg_update(text)
            # print("slew:{} - trak:{} - home:{}".format(self.controller.scope.is_slewing, self.controller.scope.is_tracking, self.controller.scope.is_home))
            self.after(self.poll_duration*1000, None) # 1000ms 1sec delay

        def stop(event=None):
            self.bail_out = True
            Slew.abort(self, self.parent, self.controller)
            #new_thread.terminate()
            button_text = self.button.cget('text')
            # print('button text :{}:'.format(button_text))
            if button_text == 'Close': self.pop.destroy()
            if button_text == 'Stop Motors': self.button.config(text="Close")


        ## these bits are in a 'stub' in main.py
        _bg='grey'
        self.pop = tk.Toplevel()
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.pop.geometry("+%d+%d" % (x + 100, y + 70))
        self.pop.title("Stress Test - long slews")
        self.pop.config(bg=_bg, padx=10, pady=10)

        self.scroll_txt = scrolledtext.ScrolledText(self.pop, wrap=tk.WORD)
        self.scroll_txt.config(bg='black', fg='red', width=60, height=24)
        self.scroll_txt['font'] = ('consolas', '12')
        self.scroll_txt.insert(tk.END, text)
        self.scroll_txt.pack(expand=True, fill='both')

        self.button = tk.Button(self.pop, text="Stop Motors", command=stop)
        self.button.pack()
        self.pop.bind('<Control-C>', stop)
        self.pop.bind('<Escape>', stop)

        if self.controller.scope.is_parked is True:
            self.controller.scope.un_park()
        self.controller.scope.set_target_alt(self.altitude)

        ''' enclose the test code in a function '''
        def TheLoop():
            for count in range(1,num_iterations+1):
                self.parent.update_idletasks()
                self.pop.update_idletasks()

                ## catch the "bail-out" flag and 'return', so the code will
                ## end 'naturally' and allow the thread to die.
                ## put this into *every* loop, maybe elsewhere
                if self.bail_out is True: return

                if self.controller.scope.is_home is False:
                    text = '\n Returning Home '
                    msg_update(text)
                    self.controller.scope.return_home() ##sets is_slewing=true
                    text = '.'
                    self.slewing = True
                    while self.slewing:
                        if self.bail_out: return
                        try:
                            print_status(text)
                            self.controller.scope.update_status()
                            self.slewing = self.controller.scope.is_slewing ##true until is_home=true
                        except KeyboardInterrupt:
                            stop(event=None)
                    ##wend

                if self.bail_out: return
                text = '\n\n Iteration {} - '.format(count)
                if self.azimuth == self.azimuth_w:
                    self.azimuth = self.azimuth_e
                    text += "Slewing EAST\n"
                else:
                    self.azimuth = self.azimuth_w
                    text += "Slewing WEST\n"
                msg_update(text)

                if self.bail_out: return
                self.controller.scope.set_target_azm(self.azimuth)
                rc, tmp = self.controller.scope.slew_hor()

                text = '< {} > {} <\n'.format(rc,tmp)
                if int(rc) > 0 :     msg_update(text)
                self.after(self.tracking_duration*1000, None) # 5000ms 5sec delay
                #if rc: return

                text = ' *'
                self.slewing = True
                while self.slewing:
                    try:
                        if self.bail_out: return
                        print_status(text)
                        self.controller.scope.update_status()
                        if self.controller.scope.is_tracking is True and self.controller.scope.is_slewing is False:
                            self.slewing = False
                    except KeyboardInterrupt:
                        stop(event=None)
                ##wend

                if self.bail_out: return
                text = '\n Slew complete, Tracking '
                msg_update(text)
                text = '.'
                for count in range(1,self.tracking_duration+1):
                    if self.bail_out: return
                    msg_update(text)
                    self.after(1000, None)
            ##loop for count()

            logging.info(f"Stress test completed")
            text = '\n\n\n Stress Test completed -- returning Home\n'
            msg_update(text)
            self.button.config(text="Close")
            self.controller.scope.return_home()
        ##TheLoop()

        ''' run the test code in a new thread '''
        from threading import Thread
        new_thread = Thread(target=TheLoop)
        new_thread.start()

        ''' run the test code in a new process '''
        #import multiprocessing
        # new_thread = multiprocessing.Process(target=TheLoop)
        # new_thread.start()

        if self.bail_out: stop()
    ##StressTest()


    def n_star(self, parent, controller):
        """dialog to select stars and do an align """
        ##this is actually just the window, to hold the output
        self.parent = parent
        self.controller = controller

        from n_star import NStar_Align
        NStar_Align.get_stars(self, self.parent, self.controller)


    def tune_backlash(self, parent, controller, axis):
        '''dialog for backlash tuning procedure'''
        def __init__(self):
            self.parent = parent
            self.controller = controller
        from backlash import Tune_Backlash
        backlash = Tune_Backlash.tune_backlash1(self, self.parent, self.controller, axis)


    """ SETTINGS """

    def coordinates(self, parent):
        '''enter coordinates'''
        def __init__(self):
            self.parent = parent
        from settings import Coordinates_Settings
        coordinates = Coordinates_Settings(self, self.parent)

    def location(self, parent):
        '''settings: location'''
        def __init__(self):
            self.parent = parent
        from settings import Location
        location = Location(self, self.parent)

    def backlash(self, parent):
        '''settings: backlash'''
        def __init__(self):
            self.parent = parent
        from settings import Backlash_Settings
        backlash = Backlash_Settings(self, self.parent)

    def overhead(self, parent):
        '''settings: overhead'''
        def __init__(self):
            self.parent = parent
        from settings import Overhead_Limit
        overhead = Overhead_Limit(self, self.parent)

    def horizon(self, parent):
        '''settings: horizon'''
        def __init__(self):
            self.parent = parent
        from settings import Horizon_Limit
        horizon = Horizon_Limit(self, self.parent)

    def pastE(self, parent):
        '''settings: east of meridian'''
        def __init__(self):
            self.parent = parent
        from settings import PastE_Limit
        pastE = PastE_Limit(self, self.parent)

    def pastW(self, parent):
        '''settings: west of meridian'''
        def __init__(self):
            self.parent = parent
        from settings import PastW_Limit
        pastW = PastW_Limit(self, self.parent)
