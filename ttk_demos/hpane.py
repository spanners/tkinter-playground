# File: hpane.py
#    http://www.tcl.tk/man/tcl8.5/TkCmd/ttk_panedwindow.htm#M-orient

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class HorizPaneDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='horizpanedemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Horizontal Paned Window Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["Drag the 'sash' between the two coloured windows ",
                      "to resize them."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        pw = ttk.PanedWindow(demoPanel, orient=HORIZONTAL)
        pw.pack(side=TOP, expand=Y, fill=BOTH, 
                pady=2, padx='2m')

        # create widgets as 'children' of the paned window
        # if you plan on accessing their options through
        # PanedWindow.paneconfig()
        left = ttk.Label(pw, text='This is the\nleft side.', 
                         background='yellow', anchor=CENTER)
        right = ttk.Label(pw, text='This is the\nright side.', 
                          background='cyan', anchor=CENTER)
    
        # use .add() vs .grid() to add widgets to the paned window
        # this works whether or not the widgets have been created
        # with the paned window as 'parent'
        pw.add(left)
        pw.add(right)


if __name__ == '__main__':
    HorizPaneDemo().mainloop()
