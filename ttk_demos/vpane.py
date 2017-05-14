# File: vpane.py
#    http://www.tcl.tk/man/tcl8.5/TkCmd/ttk_panedwindow.htm#M-orient
#    http://docs.python.org/py3k/library/tkinter.scrolledtext.html

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from demopanels import MsgPanel, SeeDismissPanel

class VerticalPaneDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='verticalpanedemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Vertical Paned Window Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["Drag the 'sash' between the two scrolled windows ",
                      "to resize them."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        pw = ttk.PanedWindow(demoPanel, orient=VERTICAL)
        pw.pack(side=TOP, expand=Y, fill=BOTH, 
                pady=2, padx='2m')

        # create widgets for top and bottom panes
        top = self._create_listbox(pw)  
        bottom = self._create_text_wnd(pw)
        
        # add widgets to the pane window
        pw.add(top)
        pw.add(bottom)
        
    def _create_listbox(self, parent):
        
        f = ttk.Frame(parent)   # frame to hold listbox and scrollbar
        
        # listbox values
        wnames = ('List of Tk Widgets',
                    'button','canvas', 'checkbutton', 'entry',
                    'frame', 'label', 'labelframe', 'listbox',
                    'menu', 'menubutton', 'message', 'panedwindow',
                    'radiobutton', 'scale', 'scrollbar', 'spinbox',
                    'text', 'toplevel')
        
        paneList = StringVar()  # use a Tkinter variable for list values
        paneList.set(wnames)    # add list of widget names to the variable
        
        lb = Listbox(f, listvariable=paneList)
        
        # highlight the first item in the list
        lb.itemconfigure(0, background=lb.cget('fg'), fg=lb.cget('bg'))
        
        # add a vertical scrollbar
        vscroll = ttk.Scrollbar(f, orient=VERTICAL, command=lb.yview)
        lb['yscrollcommand'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        lb.pack(fill=BOTH, expand=Y)
        
        return f
        
    def _create_text_wnd(self, parent):
        
        # ScrolledText only has the vertical scrollbar
        txt = ScrolledText(height=8, width=30, wrap=None)
        txt.insert(END, 'This is just a normal text widget.')
        txt.pack(expand=Y, fill=BOTH)
        
        return txt
        

if __name__ == '__main__':
    VerticalPaneDemo().mainloop()
