# File: progress.py
#    http://www.tcl.tk/man/tcl8.5/TkCmd/ttk_progressbar.htm

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class ProgressBarDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='progressbardemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Progressbar Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["Below are two progress bars. The top one is a \u201Cdeterminate\u201D ",
                      "progress bar, which is used for showing how far through a defined task ",
                      "the program has got. The bottom one is an \u201Cindeterminate\u201D ",
                      "progress bar, which is used to show that the program is busy but does ",
                      "not know how long for. Both are run here in self-animated mode, which ",
                      "can be turned on and off using the buttons underneath."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        pb1 = ttk.Progressbar(demoPanel, mode='determinate', name='pb1')
        pb2 = ttk.Progressbar(demoPanel, mode='indeterminate', name='pb2')

        start = ttk.Button(text='Start Progress',
                   command=lambda: self._do_bars('start'))
        stop = ttk.Button(text='Stop Progress',
                   command=lambda: self._do_bars('stop'))

        # position and set resize behaviour
        pb1.grid(row=0,  column=0, columnspan=2, pady=5, padx=10)
        pb2.grid(row=1, column=0, columnspan=2, pady=5, padx=10)
        start.grid(in_=demoPanel, row=2, column=0, pady=5, padx=10, sticky=E)
        stop.grid(in_=demoPanel, row=2, column=1, pady=5, padx=10, sticky=W)
        demoPanel.columnconfigure('all', weight=1)
                
        
    def _do_bars(self, op):
        pb1 = self.nametowidget('demo.pb1')
        pb2 = self.nametowidget('demo.pb2')
        
        if op == 'start':
            pb1.start()
            pb2.start()
        else:
            pb1.stop()
            pb2.stop()
        


if __name__ == '__main__':
    ProgressBarDemo().mainloop()
