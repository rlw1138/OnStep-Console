"""
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#   OnStep CONNECTIVITY SETTINGS

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

HOST = '192.168.0.1'        # default IP for OnStep "station mode"

many routers use network "192.168.0.xxx", with xxx between 1 and 254
(0 and 255 are usually 'reserved')

my ComCast router prefers "10.0.0.xxx", and my three (!) OnStep controllers
have been assigned static IP addresses 111, 112, and 113 in the router AND
in the controllers themselves, for "Station Mode" (turn A/P mode OFF)

PORT = '9999'         # the OnStep IP command channel

Use the OnStep web pages to change the WiFi configuration

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
#     Or, to connect over USB serial port
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

HOST = ''  # even though there is no "host" per se, still has to be defined
PORT = '/dev/ttyUSB0'   # linux/mac
PORT = 'COM8'           # windoze

"""

hosts = [
    ## hosts[0]       hosts[1]        hosts[2]
    ##  ip addr         port           label                   # comment

    ('10.0.0.111',   '9999',  'OnStep 1 - EQ-2 generic'         ),#0
    ('10.0.0.112',   '9999',  'OnStep 2 - LXD-500B Meade'       ),#1
    ('10.0.0.113',   '9999',  'OnStep 3 - CG-4 Celestron'       ),#2
    ('192.168.0.1',  '9999',  "OnStep's default network address"),#3
    (    '',         'COM8',  'a Windows serial port'           ),#4
    (    '', '/dev/ttyUSB0',  'first usb device, linux/mac'     ),#5
    ( ' -- ',      '  --  ',  'a new entry in "hosts.py"'       ),#new entry
]


class Hosts:

    def choose_hostGUI(self, parent, controller):
        def __init__(self):
            self.parent = parent
            self.controller = controller

        import tkinter as tk

        rbs=[]

        '''the Button.Bind() at the bottom passes 'event' info that we don't
           need in this situation, so we keep everyone happy with event=None'''
        def choose(event=None):
            x = connection.get()
            HOST = hosts[x][0]
            PORT = hosts[x][1]
            if PORT.isnumeric():
                COMM = HOST+' : '+PORT
            else:
                COMM = PORT
            self.controller.app_data["var_OnStep"].set(COMM)
            self.controller.app_data["var_Host"].set(HOST)
            self.controller.app_data["var_Port"].set(PORT)
            self.controller.DisplayWarning("connecting...")
            exit_pop()

        def exit_pop():
            pop.destroy()

        def select(rb):
            '''
            highlights the entire Radiobutton line

            '''
            rb.config(bg='brown4', fg='red3')
            for rb_ in rbs:
                if rb_ != rb:
                   rb_.config(bg=_bg, fg='brown4') ## return to defaults if not selected



        self.controller.app_data["var_lbl_Connection"].set("Connecting to ")
        x = parent.winfo_x()
        y = parent.winfo_y()
        _bg='black'
        _fg='tomato'
        pop = tk.Toplevel()
        pop.attributes('-topmost',True)
        pop.geometry("+%d+%d" % (x + 30, y + 30))
        pop.grab_set() # make pop 'modal' (must click to dismiss)
        pop.title("Choose an OnStep host")
        pop.config(bg=_bg, padx=10, pady=10)
        msg = tk.Message(pop, text="", bg=_bg, fg=_fg)
        msg.pack()

        connection = tk.IntVar()
        connection.set(0)
        x=0
        for host, port, description in hosts:
            if port.isnumeric():
                label = 'Network IP'
            else:
                label = 'Serial Port'

            text = '{0:>11} {1:>15}:{2:<13} - {3:<}'.format(label, host, port, description)
            '''
            selectcolor turns the buttons black so the red dot stands out better,
            highlightbackground and highlightthickness remove the thin white box
            around each entry
            '''
            f=tk.Frame(pop, bg=_bg)
            f.pack()
            b = tk.Radiobutton(f, text=text, variable=connection, value=x)
            b.config(bg=_bg, fg=_fg, width=80, anchor="w", font=("courier", 12, "bold") )
            b.config(selectcolor='black', relief='solid')
            b.config(activebackground='brown3', activeforeground='black')
            b.config(highlightbackground=_bg, highlightthickness=0)
            b.pack(side='left')
            b.deselect()
            if host=='192.168.0.1':
                b.select()
            x+=1
            b.config(command=lambda arg=b:select(arg))
            rbs.append(b)
            #f.update_idletasks()


        ## this red bar goes across the bottom of the pop-up
        separator= tk.Label(pop, bg='dark red', height=1, text='='*40)
        separator.pack(side='bottom', fill='x')
        ## frame just above the red bar
        bottomframe = tk.Frame(pop)
        bottomframe.configure(bg=_bg)
        bottomframe.pack( side = 'bottom' )

        cancel_button = tk.Button(bottomframe, text="Cancel", command=exit_pop)
        cancel_button.config(bg=_bg, fg=_fg, bd=0, activebackground='goldenrod1')
        cancel_button.config(highlightbackground='goldenrod1')
        cancel_button.config(highlightcolor='red')
        cancel_button.config(highlightthickness=2)
        cancel_button.pack(side='left')

        button = tk.Button(bottomframe, text="  OK  ", command=choose)
        button.config(bg=_bg, fg=_fg, bd=0, activebackground='red')
        button.config(highlightbackground='red')
        button.config(highlightcolor='green2')
        button.config(highlightthickness=2)
        button.pack(side='left')
        button.focus_set()
        button.bind("<Return>", choose)


if __name__ == "__main__":
    #Hosts.choose_hostGUI()
    pass
