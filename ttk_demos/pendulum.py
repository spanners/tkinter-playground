# File: pendulum.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//canvas.html
# Other Reference:
#    http://rosettacode.org/wiki/Animate_a_pendulum#Python

import math

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class PendulumDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='pendulumdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Pendulum Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["This demonstration shows how Tkinter can be used to carry out animations ",
                      "that are linked to simulations of physical systems. In the left canvas ",
                      "is a graphical representation of the physical system itself, a simple ",
                      "pendulum, and in the right canvas is a graph of the phase space of the ",
                      "system, which is a plot of the angle (relative to the vertical) against ",
                      "the angular velocity. The pendulum bob may be repositioned by clicking ",
                      "and dragging anywhere on the left canvas."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        # variables used by the widgets
        self.__theta = 45.0 # pendulum angle
        self.__dtheta = 0.0 # new pendulum angle
        self.__length = 150 # rod length
        self.__home = 160   # rod 'attach' position
        
        self.__points = []   # coords describing phase motion
        self.__psw = 320/2   # phase space panel width
        self.__psh = 200/2   # phase space panel height
        
        # tag and colour names for the phase space oval which
        #  is drawn in segments to allow colour variations
        # (in a dict to avoid building/discarding strings during animation)
        self.__graph = {0: ('graph0','grey0'), 10: ('graph10','grey10'),
                        20: ('graph20', 'grey20'), 30: ('graph30','grey30'), 
                        40: ('graph40','grey40'), 50: ('graph50','grey50'),
                        60: ('graph60','grey60'), 70: ('graph70','grey70'),
                        80: ('graph80','grey80'), 90: ('graph90','grey90')}
                
        # build panels                
        pw = ttk.Panedwindow(demoPanel, orient=HORIZONTAL)
        pw.pack(side=TOP, fill=BOTH, expand=Y)

        self.__pen = self._create_pendulum_panel(pw)
        self.__phase = self._create_phase_panel(pw)
        self._show_pendulum()
        
        # add bindings
        self._create_bindings()
        
        # start animations after slight pause
        self.after(500, self._repeat)   

    # =====================================================================================
    # Animation handler
    # =====================================================================================
    def _repeat(self):
        self._recompute_angle() # define pendulum position and swing parameters
        self._show_pendulum()   # display pendulum
        self._show_phase()      # display phase space
        
        self.after(15, self._repeat)    # repeat animation

    # =====================================================================================
    # Bindings and bound methods
    # =====================================================================================
    
    def _create_bindings(self):
        # allow user to re-position pendulum with Left Mouse button click
        self.__pen.bind('<1>', self._change_pendulum)
        self.__pen.bind('<B1-Motion>', self._change_pendulum)
        self.__pen.bind('<ButtonRelease-1>', lambda e, repeat=True: self._change_pendulum(e, repeat))

        # capture window resize and resize phase space panel
        self.__phase.bind('<Configure>', self._phase_configure)

    def _change_pendulum(self, evt, repeat=False):
        # triggered when user clicks in 'Pendulum Simulation' panel
        # re-positions the pendulum bob and resizes the rod
        self._show_pendulum(evt.x, evt.y)
        
        if repeat:
            self.after(15, self._repeat)

    def _phase_configure(self, evt):
        # triggered when the user resizes the window
        # resizes the phase space panel
        width = self.__phase.winfo_width()
        height = self.__phase.winfo_height()
        self.__psh = height / 2
        self.__psw = width / 2
        self.__phase.coords('x_axis', 2, self.__psh, width-2, self.__psh )
        self.__phase.coords('y_axis', self.__psw, height-2, self.__psw, 2)
        self.__phase.coords('label_dtheta', self.__psw-4, 6)
        self.__phase.coords('label_theta', width-6, self.__psh+4)
                
    # =====================================================================================
    # Routines to build and control the pendulum
    # =====================================================================================                
    def _create_pendulum_panel(self, parent):
        
        left = ttk.Labelframe(parent, text="Pendulum Simulation")
        parent.add(left)
        
        # Create the canvas containing the graphical representation of the
        # simulated system

        c = Canvas(left, width=320, height=200, background='white',
                   bd=2, relief=SUNKEN, name='pen_canvas')
        c.create_text(5, 5, anchor='nw', text='Click to Adjust Bob Start Position',
                      state='disabled', disabledfill='grey50')
        c.create_line(0,25,320,25, tags='plate', fill='grey50', width=2)
        c.create_oval(155,20,165,30, tags='pivot', fill='grey50')
        c.create_line(1,1,1,1, tags='rod', fill='black', width=3)
        c.create_oval(1,1,2,2, tags='bob', fill='yellow', outline='black')
        c.pack(fill=BOTH,  expand=Y)
                
        return c
                
    def _show_pendulum(self, x=None, y=None):
        # display the pendulum
        if (x and y) and (x != self.__home or y != 25):
            self.__dtheta = 0.0
            x2 = x - self.__home
            y2 = y - 25
            self.__length = math.hypot(x2,y2)
            self.__theta = math.atan2(x2, y2) * 180/math.pi
        else:
            angle = math.radians(self.__theta)
            x = self.__home + self.__length * math.sin(angle)
            y = 25 + self.__length * math.cos(angle)
        
        self.__pen.coords('rod', self.__home, 25, x, y)
        self.__pen.coords('bob', x-15, y-15, x+15, y+15)


    def _recompute_angle(self):
        # core animation routine for a simple rotational
        # pendulum; recomputes the angle parameters
        # (the original Tcl file says there is a better
        #  way to do this but it requires a better knowledge
        #  of derivatives)
        
        scaling = 3000.0/self.__length/self.__length
        
        # first estimate
        firstDDtheta = -math.sin(math.radians(self.__theta)) * scaling
        midDtheta = self.__dtheta + firstDDtheta
        midtheta = self.__theta + (self.__dtheta + midDtheta)/2.0
 
        # second estimate
        midDDtheta = -math.sin(math.radians(midtheta)) * scaling
        midDtheta = self.__dtheta + (firstDDtheta + midDDtheta)/2.0
        midtheta = self.__theta + (self.__dtheta + midDtheta)/2.0

        # first double estimate
        midDDtheta = -math.sin(math.radians(midtheta)) * scaling
        lastDtheta = midDtheta + midDDtheta
        lasttheta = midtheta + (midDtheta + lastDtheta)/2.0
 
        # second double estimate
        lastDDtheta = -math.sin(math.radians(lasttheta)) * scaling
        lastDtheta = midDtheta + (midDDtheta + lastDDtheta)/2.0
        lasttheta = midtheta + (midDtheta + lastDtheta)/2.0                
        
        self.__theta = lasttheta
        self.__dtheta = lastDtheta
        
    # =====================================================================================
    # Routines to build and control the phase space
    # =====================================================================================                
    def _create_phase_panel(self, parent):
        
        right = ttk.Labelframe(parent, text="Phase Space")
        parent.add(right)
        
        # Create the canvas containing the phase space graph; this consists of
        # a line that gets gradually paler as it ages, which is an effective
        # visual trick.

        c = Canvas(right, width=320, height=200, background='white',
                   bd=2, relief=SUNKEN, name='phase_canvas')
        c.create_line(160,200,160,0, fill='grey75', arrow='last', tags='y_axis')
        c.create_line(0,100,320,100, fill='grey75', arrow='last', tags='x_axis')
        
        for i in range(90, -1, -10):
            c.create_line(0,0,1,1, smooth='true', tags=self.__graph[i][0], 
                          fill=self.__graph[i][1])
        
        c.create_text(0,0, anchor='ne', text='q', font=('Symbol', 8), 
                      tags='label_theta')
        c.create_text(0,0, anchor='ne', text='dq', font=('Symbol', 8), 
                      tags='label_dtheta')
        c.pack(fill=BOTH, expand=Y)
        
        return c

    def _show_phase(self):
        # Update the phase-space graph according to the current angle and the
        # rate at which the angle is changing (the first derivative with
        # respect to time.)

        self.__points.extend([self.__theta+self.__psw,
                              -20 * self.__dtheta+self.__psh])
    
        end = len(self.__points)
        if end > 100:   # start over
            self.__points = []

        pts = []
        for i in range(0,100,10):
            pts = self.__points[end-i:end-i-12]
            if len(pts) >= 4:  # coords for affected portion of the line
                self.__phase.coords(self.__graph[i][0], *pts)
                

if __name__ == '__main__':
    PendulumDemo().mainloop()
