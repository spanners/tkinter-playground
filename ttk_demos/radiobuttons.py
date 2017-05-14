# File: radiobuttons.py
# References:
#    http://www.tcl.tk/man/tcl8.5/TkCmd/ttk_labelframe.htm#M-labelwidget
#    http://wiki.tcl.tk/20054
#    http://www.pythonware.com/library/tkinter/introduction/x444-fonts.htm
#    http://www.tcl.tk/man/tcl8.5/TkCmd/colors.htm
#
# Image source: 
#    http://findicons.com/icon/94113/dialog_question?width=72#

from tkinter import *
from tkinter import ttk
from tkinter.font import *
from PIL import Image, ImageTk
from demopanels import MsgPanel, SeeDismissPanel

class RadiobuttonDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='radiobuttondemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Radiobutton Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self, 
                     ["Three groups of radiobuttons are displayed below.  If you click on a button then ",
                      "the button will become selected exclusively among all the buttons in its group. ",
                      "A control variable is associated with each group to indicate which of the group's ",
                      "buttons is selected.\n\n",
                      "Selecting a Point Size or Color changes the associated Labelframe text.\n\n",
                      "Selecting an Alignment repositions the graphic with respect ",
                      "to the label i.e. 'Bottom' puts the graphic 'below' the label."])
            
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        points = self._create_points_panel(demoPanel)   
        color = self._create_color_panel(demoPanel)
        align = self._create_image_panel(demoPanel)
        vars = self._create_var_panel(demoPanel)

        # position the BOTTOM panel first, otherwise it will get
        # tacked onto the end of the LEFT rather than placed at the bottom
        vars.pack(side=BOTTOM, expand=True, padx=10, pady=10, fill=X, anchor=SW)
        
        points.pack(side=LEFT, padx=10, pady=10, fill=BOTH)
        color.pack(side=LEFT, padx=10, pady=10, fill=BOTH)
        align.pack(side=LEFT, expand=True, padx=10, pady=10, fill=BOTH)
        
        
    def _create_points_panel(self, parent):
        # assign a style that applies only to this panel
        f = ttk.Labelframe(parent, text='Point Size', style='Points.TLabelframe', width=100)
        
        font = Font(f)                  # get font used by LabelFrame
        family=font.actual()['family']  # save font family
        weight=font.actual()['weight']  # save font weight
        
        # font sizes are in 'points', to give size in
        # pixels use a negative value e.g. -10, -12, etc.
        # The default font size for ttk.Labelframe is 12 pixels
        points = [10, 12, 14, 18, 24]
        self.size = IntVar()
        rb = []
        for p in points:
            rb.append(ttk.Radiobutton(f, text="Point size " + str(p),
                                         variable = self.size,
                                         value = p,
                                         command=lambda p=p: self._points_changed(family,p,weight)))
        for b in rb:
            b.pack(side=TOP, pady=2, padx=2, anchor=W, fill=X)
                
        return f
    
    def _points_changed(self,family, size, weight):
        ttk.Style().configure('Points.TLabelframe.Label', font=(family,-size,weight))
        self._show_vars()
                    
    def _create_color_panel(self, parent):
        # assign a style that applies only to this panel
        lbl = ttk.Label(text='Color', foreground='blue', style='Color.TLabelframe.Label')
        f = ttk.LabelFrame(parent, labelwidget=lbl)
                
        colors = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple']
        self.color = StringVar()
        rb = []
        for c in colors:
            rb.append(ttk.Radiobutton(f, text=c,
                                         variable = self.color,
                                         value = c,
                                         command=lambda c=c: self._color_changed(lbl, c)))
        for b in rb:
            b.pack(side=TOP, pady=2, padx=2, anchor=W, fill=X)
        
        return f
    
    def _color_changed(self,lbl, color):
        lbl.config(foreground=color)
        self._show_vars()
    
    def _create_image_panel(self, parent):
        f = ttk.Labelframe(parent, text='Alignment')
        
        im = Image.open('images/dialog_question.png')
        imh = ImageTk.PhotoImage(im)
        
        lbl = Label(text='Label', compound=LEFT, image=imh, 
                    font=('Helv', 10, 'bold italic'),
                    foreground='blue')  
        lbl.image = imh
        
        # set width and height to prevent label resizing when
        # image alignment changes
        lbl.configure(width=lbl.winfo_reqwidth(), compound=RIGHT)
        lbl.configure(height=lbl.winfo_reqheight(), compound=TOP)
        
        lbl.grid(in_=f, row=1, column=1, padx=5, pady=5)
        
        loc = ['Top', 'Left', 'Bottom', 'Right']
        self.align = StringVar()
        rb = []
        for l in loc:
            rb.append(ttk.Radiobutton(f, text=l,
                                         variable = self.align,
                                         value = l.lower(),
                                         width=7,
                                         command=lambda l=l: self._align_changed(lbl, l.lower())))
            
        
        rb[0].grid(in_=f, row=0, column=1)
        rb[1].grid(in_=f, row=1, column=0)
        rb[2].grid(in_=f, row=2, column=1)
        rb[3].grid(in_=f, row=1, column=2)
        
        return f

    def _align_changed(self, lbl, value):
        lbl.config(compound=value)
        self._show_vars()

    def _create_var_panel(self, parent):
        # panel to display radiobutton variable values
        right = ttk.LabelFrame(parent, text='Radiobutton Control Variables')
        
        self.vb0 = ttk.Label(right, font=('Courier', 10))        
        self.vb0.pack(side=LEFT, anchor=NW, pady=3, padx=15)
        
        self._show_vars()   
        
        return right

    def _show_vars(self):
        # set text for labels in var_panel to include the control 
        # variable name and current variable value
        self.vb0['text'] = 'size: {} \tcolor: {} \talign: {}'.format(self.size.get(),
                                                                    self.color.get(),
                                                                    self.align.get())
        

if __name__ == '__main__':
    RadiobuttonDemo().mainloop()
