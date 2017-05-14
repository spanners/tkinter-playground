"""
The idea here is to create a server to allow friends to sit at laptops running clients
and to play any game of cards with any of their own rules.

I expect I will provide them with a virtual table and unlimited packs of cards.

I may provide them with a way to record scores.

Not sure what else...

This project was started on holiday in Scotland (September 2009) on a day when the weather
could have been better but the location could not (Caradale on Mull of Kintire).
"""

import sys

sys.path.append("..")

try:
    from Tkinter import *
except:
    from tkinter import *

from cards.iogui import IOGui, message
from cards.io import ServerIO

class Server(IOGui):
    """
    Just sit around waiting for someone to connect to have a game of cards.
    """

    def create_widgets(self):
        """
        No user should ever need to look at the server, but, I expect it can help
        me to debug..
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
    def hi_msg(self, client, name):
        """
        """
        client.name = name
        self.create_text(text='%s is here' % name)

    @message
    def finished_msg(self, client):
        """
        """
        self.create_text(text='%s is gone' % client.name)
        
# run...
Server(ServerIO(name='freehand server', port=9998))
