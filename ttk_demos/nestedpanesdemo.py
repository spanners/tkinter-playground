# File: nestedpanesdemo.py
#    http://www.tcl.tk/man/tcl8.5/TkCmd/ttk_panedwindow.htm#M-orient
#    http://www.tcl.tk/man/tcl/TclCmd/clock.htm

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

from demopanels import MsgPanel, SeeDismissPanel

class NestedPanesDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='nestedpanesdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Nested Panes Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["This demonstration shows off a nested set of themed paned ",
                      "windows. Their sizes can be changed by grabbing the area ",
                      "between each contained pane and dragging the divider."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        self._create_wnd_struct(demoPanel)
        self._fill_button_pane()
        self._fill_clock_pane()
        self._fill_progress_pane()
        self._fill_text_pane()
        
    def _create_wnd_struct(self, parent):
        outer = ttk.PanedWindow(parent, orient=HORIZONTAL, name='outer')
        outer.pack(expand=Y, fill=BOTH, padx=10, pady=(6,10))
        
        left = ttk.PanedWindow(outer, orient=VERTICAL, name='left')
        right = ttk.PanedWindow(outer, orient=VERTICAL, name='right')
        outer.add(left)
        outer.add(right)
        
        ltop = ttk.LabelFrame(left, text='Button', padding=3, name='ltop')
        lbot = ttk.LabelFrame(left, text='Clocks', padding=3, name='lbot')
        left.add(ltop)
        left.add(lbot)
        
        rtop = ttk.LabelFrame(right, text='Progress', padding=3, name='rtop')
        rbot = ttk.LabelFrame(right, text='Text', padding=3, name='rbot')
        right.add(rtop)
        right.add(rbot)

    def _fill_button_pane(self):
        # create and add button
        ltop = self.nametowidget('demo.outer.left.ltop')
        b = ttk.Button(ltop, text='Press Me', command=self._say_ouch)
        b.pack(padx=2, pady=3)
        
    def _say_ouch(self):
        # triggered when the button is pressed
        showinfo(title='Button Pressed', message='Ouch!',
                 detail='That hurt...', parent=self)
        
    def _fill_progress_pane(self):
        # create and add progress bar
        rtop = self.nametowidget('demo.outer.right.rtop')
        pb = ttk.Progressbar(rtop, mode='indeterminate')
        pb.pack(fill=BOTH, expand=Y, padx=2, pady=5)
        pb.start()
        
    def _fill_text_pane(self):
        # create and add text widget
        rbot = self.nametowidget('demo.outer.right.rbot')
        f = ttk.Frame(rbot)
        f.pack(expand=Y, fill=BOTH)
        
        txt = Text(f, wrap=WORD, width=30, bd=0)
        vscroll = ttk.Scrollbar(f, orient=VERTICAL, command=txt.yview)
        txt['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        txt.pack(fill=BOTH, expand=Y)
                
    def _fill_clock_pane(self):
        # create and add clock labels
        # makes use of the Tcl/Tk 'clock' functions
        zones = (':Europe/Berlin',
                 ':America/Argentina/Buenos_Aires',
                 ':Africa/Johannesburg',
                 ':Europe/London',
                 ':America/Los_Angeles',
                 ':Europe/Moscow',
                 ':America/New_York',
                 ':Asia/Singapore',
                 ':Australia/Sydney',
                 ':Asia/Tokyo')

        # Force a pre-load of all the timezones 
        # needed to avoid sync problems
        for z in zones:
            c = self.tk.call('clock', 'format', 0, '-timezone', z)

        lbot = self.nametowidget('demo.outer.left.lbot')            
        for z in zones:
            # extract and format city name
            city = z.split('/')[-1] 
            city = [c if c != '_' else ' ' for c in city] 
            
            # create two labels for each city; one with the name
            # the other to hold the city's time
            lbl = ttk.Label(lbot, text=''.join(city), anchor=W)
            time = ttk.Label(lbot,  textvariable=StringVar(), anchor=W)
            lbl.pack(fill=X)
            time.pack(fill=X)
            ttk.Separator(lbot).pack(fill=X)

            # set the current time for the indicated zone        
            self._tick(time, z)
            
    def _tick(self, time, zone):
            # clock label helper function
            # sets the time immediately and updates it every 1000ms
            # (makes use of Tcl/Tk time handling routines)
            #
            # time - one of the 'clock' labels
            # zone - the associated timezone
                    
            cs = self.tk.call('clock', 'seconds')   # current clock time in seconds
            c = self.tk.call('clock', 'format', cs, '-timezone', zone, '-format', '%T')

            varname = time.cget('textvariable')
            time.setvar(varname, c)
            
            self.after(1000, self._tick, *(time, zone))
            

if __name__ == '__main__':
    NestedPanesDemo().mainloop()
