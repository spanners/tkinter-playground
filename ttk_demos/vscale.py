# File: vscale.py

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class VerticalScaleDemo(ttk.Frame):
    def __init__(self, isapp=True, name='vscaledemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Vertical Scroll Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["An arrow and a vertical scale are displayed below. ",
                      "If you click or drag mouse button 1 in the scale, you ",
                      "can change the length of the arrow."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self, borderwidth=10, name='demo')
        demoPanel.pack()
        
        canvas = Canvas(demoPanel, width=50, height=50, 
                        bd=0, highlightthickness=0, name='arrow')

        # draw an arrow
        canvas.create_polygon('0 0 1 1 2 2', fill='SeaGreen3',
                              tags=('poly', ), outline='black')

        scale = ttk.Scale(orient=VERTICAL, length=284,
                          from_=0, to=250,
                          command=self._set_height)
        scale.set(75)
        
        # position and set resize behaviour
        canvas.pack(side=LEFT, fill=Y, anchor='nw')
        scale.pack(in_=demoPanel, side=LEFT, anchor='ne')


    def _set_height(self, height):
        # stretch the arrow
        canvas = self.nametowidget('demo.arrow')
        height = float(height) 
        y2 = height - 30 
        
        y2 = str(y2)
        height = str(height)
        
        shape = (15, 0, 35, 0, 35, y2, 45, y2, 25, height,
                 5, y2, 15, y2, 15, 0)
        
        canvas.coords('poly', shape)


if __name__ == '__main__':
    VerticalScaleDemo().mainloop()

