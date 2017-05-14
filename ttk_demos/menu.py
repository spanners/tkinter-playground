# File: menu.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//menu.html
#    http://tkinter.unpythonic.net/wiki/A_tour_of_Tkinter_widgets (menu.py)
#    http://stackoverflow.com/questions/3485397/python-tkinter-dropdown-menu-w-keyboard-shortcuts
#
# Notes:
#    - under Windows, the underlines for the menu shortcut keys
#      don't appear until 'Alt' is pressed

from tkinter import *
from tkinter import ttk
from demopanels import MsgPanel, SeeDismissPanel

class MenuDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='menudemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Menu Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        if self.isapp:             
            SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        msg = ["This window contains a menubar with cascaded menus.  You can post ",
              "a menu from the keyboard by typing Alt+x, where \"x\" is the ",
              "character underlined on the menu.\n\tYou can then traverse among the ",
              "menus using the arrow keys.\n\tWhen a menu is posted, you can invoke ",
              "the current entry by typing space, or you can invoke any entry by ",
              "typing its underlined character.\n\tIf a menu entry has an accelerator, ",
              "you can invoke the entry without posting the menu just by typing ",
              "the accelerator.\n\tThe rightmost menu can be torn off into a palette ",
              "by selecting the first item in the menu."]
        
        lbl = ttk.Label(demoPanel, text=''.join(msg), wraplength='4i', justify=LEFT)
        lbl.pack(side=TOP, padx=5, pady=5)
        
        # create statusbar 
        statusBar = ttk.Frame()
        self.__status = ttk.Label(self.master, text=' ', relief=SUNKEN, borderwidth=1,
                              font=('Helv 10'), anchor=W, name='status')
        
        self.__status.pack(side=LEFT, padx=2, expand=Y, fill=BOTH)
        statusBar.pack(side=BOTTOM, fill=X, pady=2)
                
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tearoff's
        self._menu = Menu(self.master, name='menu')
        self._build_submenus()
        self.master.config(menu=self._menu)
        
        # set up standard bindings for the Menu class
        # (essentially to capture mouse enter/leave events)
        self._menu.bind_class('Menu', '<<MenuSelect>>', self._update_status)

    def _build_submenus(self):
        # create the submenus
        # the routines are essentially the same:
        #    1. create the submenu, passing the main menu as parent
        #    2. add the submenu to the main menu as a 'cascade'
        #    3. add the submenu's individual items
        
        self._add_file_menu()
        self._add_basic_menu()
        self._add_cascades_menu()
        self._add_icons_menu()
        self._add_more_menu()
        self._add_colors_menu()

    # ================================================================================
    # Submenu routines
    # ================================================================================ 

    # File menu ------------------------------------------------------------------                
    def _add_file_menu(self):
        fmenu = Menu(self._menu, name='fmenu')
        self._menu.add_cascade(label='File', menu=fmenu, underline=0)
        labels = ('Open...', 'New', 'Save', 'Save As...', 'Print Setup...',
                   'Print...', )

        for item in labels:
            fmenu.add_command(label=item,
                              command=lambda m=item: self._demo_only(m))

        fmenu.add_separator()
        fmenu.add_command(label='Exit Demo', 
                          command=lambda: self.master.destroy()) # kill toplevel wnd
        
    # Basic menu ------------------------------------------------------------------        
    def _add_basic_menu(self):
        bmenu = Menu(self._menu)
        self._menu.add_cascade(menu=bmenu, label='Basic', underline=0)
        bmenu.add_command(label='Long entry that does nothing')
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        for item in labels:
            bmenu.add_command(label='Print letter "{}"'.format(item),
                              underline=14, 
                              accelerator='Control+{}'.format(item),
                              command=lambda i=item: self._print_it(None, i))
            
            # bind accelerator key to a method; the bind is on ALL the
            # applications widgets
            self.bind_all('<Control-{}>'.format(item.lower()), 
                            lambda e, i=item: self._print_it(e, i))

    # Cascades menu ------------------------------------------------------------------            
    def _add_cascades_menu(self):
        cascades = Menu(self._menu)
        self._menu.add_cascade(label='Cascades', menu=cascades, underline=0)
        
        cascades.add_command(label='Print Hello', underline=6,
                             accelerator='Control+H',
                             command=lambda: self._print_it(None, 'Hello'))

        cascades.add_command(label='Print Goodbye', underline=6,
                             accelerator='Control+G',
                             command=lambda: self._print_it(None, 'Goodbye'))

        # add submenus        
        self._add_casc_cbs(cascades)    # check buttons
        self._add_casc_rbs(cascades)    # radio buttons

        # bind accelerator key to a method; the bind is on ALL the
        # applications widgets
        self.bind_all('<Control-h>', 
                        lambda e: self._print_it(e, 'Hello'))
        self.bind_all('<Control-g>', 
                        lambda e: self._print_it(e, 'Goodbye'))

    def _add_casc_cbs(self, cascades):
        # build the Cascades->Check Buttons submenu
        check = Menu(cascades)
        cascades.add_cascade(label='Check Buttons', underline=0,
                               menu=check)
        
        self.__vars = {}
        labels = ('Oil checked', 'Transmission checked',
                  'Brakes checked', 'Lights checked' )

        for item in labels:
            self.__vars[item] = IntVar()
            check.add_checkbutton(label=item, variable=self.__vars[item])
            
        # set items 1 and 3 to 'selected' state
        check.invoke(1)
        check.invoke(3)
            
        check.add_separator()
        check.add_command(label='Show values',
                          command=lambda lbls=labels: self._show_vars(lbls))
                    
    def _add_casc_rbs(self, cascades):
        # build Cascades->Radio Buttuns subment
        submenu = Menu(cascades)
        cascades.add_cascade(label='Radio Buttons', underline=0,
                               menu=submenu)
        
        self.__vars['size'] = StringVar()
        self.__vars['font'] = StringVar()
        
        for item in (10,14,18,24,32):
            submenu.add_radiobutton(label='{} points'.format(item), 
                                    variable=self.__vars['size'])
            
        submenu.add_separator()
        for item in ('Roman', 'Bold', 'Italic'):
            submenu.add_radiobutton(label=item, 
                                    variable=self.__vars['font'])
    
        # set items 1 and 7 to 'selected' state
        submenu.invoke(1)
        submenu.invoke(7)
            
        submenu.add_separator()
        submenu.add_command(label='Show values',
                            command=lambda: self._show_vars(('size','font')))
        

    # Icons menu ------------------------------------------------------------------        
    def _add_icons_menu(self):       
        menu = Menu(self._menu)
        self._menu.add_cascade(label='Icons', menu=menu, underline=0)
        
        # 'info', 'questhead', and 'error' are Tk built-in icons
        for bm in ('@images/pattern.xbm', 'info', 'questhead', 'error'):
            menu.add_command(bitmap=bm, hidemargin=1,
                             command=lambda b=bm: self._you_invoked((b, 'bitmap')))
            
        menu.entryconfigure(2, columnbreak=1)      
    
    # More menu ------------------------------------------------------------------    
    def _add_more_menu(self):
        menu = Menu(self._menu)
        self._menu.add_cascade(label='More', menu=menu, underline=0)
        
        labels = ('An entry', 'Another entry', 'Does nothing',
                'Does almost nothing', 'Make life meaningful')
        
        for item in labels:
            menu.add_command(label=item,
                             command=lambda i=item: self._you_invoked((i, 'entry')))
            
        menu.entryconfig(3, bitmap='questhead', compound=LEFT,
                         command=lambda i=labels[3]: 
                                    self._you_invoked((i, 
                                                      'entry; a bitmap and a text string')))            
          
    # Colors menu ------------------------------------------------------------------           
    def _add_colors_menu(self):
        menu = Menu(self._menu, tearoff=True)
        self._menu.add_cascade(label='Colors', menu=menu, underline=1)
        
        for c in ('red', 'orange', 'yellow', 'green', 'blue'):
            menu.add_command(label=c, background=c,
                             command=lambda c=c: self._you_invoked((c, 'color')))    
                    
    # ================================================================================
    # Bound and Command methods
    # ================================================================================                
    def _print_it(self, e, txt):
        # triggered by multiple menu items that print letters or greetings
        # or by an accelerator keypress (Ctrl+a, Ctrl+b, etc).
        print(txt)
        
    def _demo_only(self, menuItem):
        # triggered when unimplemented submenu items are clicked
        self.bell()
        self.__status.configure(background='red', foreground='white',
                                text="No action has been defined for menu item '" + menuItem + "'")        
        
    def _update_status(self, evt):
        # triggered on mouse entry if a menu item has focus 
        # (focus occurs when user clicks on a top level menu item)
        try:
            item = self.tk.eval('%s entrycget active -label' % evt.widget )
            self.__status.configure(background='gray90', foreground='black',
                                    text=item)
        except TclError:
            # no label available, ignore
            pass
        
    def _show_vars(self, values):
        # called when Cascades->Check Buttons or Radio Buttons
        # 'Show Values' item is selected
        # displayf variable values in the status bar
        v = []
        for e in values:
            t = self.__vars[e].get()
            s = '{}: {}  '.format(e, t)
            v.append(s)
        
        self.__status.configure(background='white', foreground='black',
                                text=''.join(v))
    
    def _you_invoked(self, value):
        # triggered when an entry in the Icons, More or Colors menu is selected
        self.bell()
        self.__status.configure(background='SeaGreen1', foreground='black',
                                text="You invoked the '{}' {}.".format(value[0], 
                                                                       value[1]))
        
if __name__ == '__main__':
    MenuDemo().mainloop()