"""
A freeplay client.
"""

import sys

sys.path.append("..")


from getpass import getuser

try:
    from Tkinter import *
except:
    from tkinter import *

from cards.iogui import IOGui, message
from cards.io import ClientIO

NAME = getuser()

class Client(IOGui):
    """
    """

    def create_widgets(self):
        """
        Must have this method to create the basic set of user interface widgets.
        """
        self.texty = 10
        self.base_canvas = w = Canvas(self.root, bg='darkgreen')
        w.pack(expand=YES, fill=BOTH)

    def create_text(self, text):
        """
        """
        self.base_canvas.create_text(10, self.texty, text=text, anchor=NW)
        self.texty += 10
        
    @message
    def started_msg(self, sender, host, port):
        """
        On startup say who you are.
        """
        self.root.title('%s@%s' % (host, port))
        self.put = sender.put # save the put command
        self.put('hi_msg', NAME)

    @message
    def error_msg(self, sender, msg):
        """
        Display any error messages
        """
        self.create_text(text=msg)

# run...
Client(ClientIO(name=NAME, port=9998))
