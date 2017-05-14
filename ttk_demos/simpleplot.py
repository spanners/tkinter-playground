# File: simpleplot.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//canvas.html
#    http://www.tcl.tk/man/tcl8.5/TkCmd/canvas.htm
# Ref: canvassimple.py
#    http://tkinter.unpythonic.net/wiki/A_tour_of_Tkinter_widgets

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class SimplePlotDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='simpleplotdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Simple Plot Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["This window displays a canvas widget containing ",
                      "a simple 2-dimensional plot.  You can doctor the ",
                      "data by dragging any of the points with mouse button 1."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        plot = self._create_plot(demoPanel)
        self._create_bindings(plot)
        
    def _create_plot(self, parent):
        c = Canvas(parent, relief=RAISED, width=450, height=300)
        c.pack(side=TOP, fill=X)

        plotFont = ('Helv', 18)

        # create axes
        c.create_line(100, 250, 400, 250, width=2)
        c.create_line(100, 250, 100, 50, width=2)
        c.create_text(225, 20, text='A Simple Plot', font=plotFont, fill='brown')
        
        # create x-axis labels
        for i in range(11):
            x = 100 + i*30
            c.create_line(x, 250, x, 245, width=2)
            c.create_text(x, 254, text='{}'.format( (10*i) ),
                          anchor=N, font=plotFont)
        
        # create y-axis labels
        for i in range(1,6):
            y = 250 - (i*40)
            c.create_line(100, y, 105, y, width=2)
            c.create_text(96, y, text='{}'.format( (i*50.0)  ),
                          anchor=E, font=plotFont)
        
        # create data points    
        data = [(12, 56), (20, 94), (33, 98),
                (32, 120), (61, 180), (75, 160), (98, 223)]
        
        for p0, p1 in data:
            x = 100 + 3 * p0
            y = 250 - (4 * p1)/5
            item = c.create_oval(x-6, y-6, x+6, y+6, width=1,
                                 outline='black', fill='SkyBlue2')
            c.addtag_withtag('point', item)

        # add oldx, oldy attributes to canvas for use
        # by bound methods _point_enter() and _point_drag()
        c.oldx = 0
        c.oldy = 0
        
        return c
    
    def _create_bindings(self, plot):
        plot.tag_bind('point', '<Any-Enter>', 
                      lambda evt, p=plot: self._point_enter(evt, p)) 
        plot.tag_bind('point', '<Any-Leave>', 
                      lambda evt, p=plot: 
                        p.itemconfigure('current', fill='SkyBlue2'))
        plot.tag_bind('point', '<B1-Motion>', 
                      lambda evt, p=plot: self._point_drag(evt, p))
        
    def _point_enter(self, evt, plot):    
        plot.itemconfigure('current', fill='red') 
        plot.oldx = evt.x
        plot.oldy = evt.y
        
    def _point_drag(self, evt, plot):
        x,y = plot.canvasx(evt.x), plot.canvasy(evt.y)
        plot.move('current', x - plot.oldx, y - plot.oldy )
        plot.oldx, plot.oldy = x, y
        

if __name__ == '__main__':
    SimplePlotDemo().mainloop()
