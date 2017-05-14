"""
A server to serve out games of cards to several players (clients).
"""

import sys

sys.path.append("..")

import time

try:
    from Tkinter import *
except:
    from tkinter import *

from cards_simple.iogui import IOGui, message
from cards_simple.inout import ServerIO

from cards_simple.deck import Deck, Player

NAME = sys.argv[1] if len(sys.argv)>1 else "server"

class Deck99(Deck):
    def discard(self, suit, rank):
        return rank in ('two', 'three', 'four', 'five')

class CardServerGui(IOGui):
    """
    """
    NINETY9 =  '99 - Ninety Nine'
    GAMES = NINETY9,

    def create_widgets(self):
        """
        """
        self.users = []
        self.players = dict([(key, []) for key in self.GAMES]) # dict of games and lists of players
        root = self.root
        self.canvas = w = Canvas(root, bg='thistle')
        w.pack(expand=YES, fill=BOTH)
        root.after(1000,self.monitor)
        
    def monitor(self):
        """
        """
        canvas = self.canvas
        canvas.delete('all')
        for idx, u in enumerate(self.users):
            canvas.create_text(10, 10+20*idx,  text=u.name, anchor=W)
        self.root.after(1000,self.monitor)

    @message
    def started_msg(self, client, host, port):
        """
        A new client add to list of clients.
        """
        print("started_msg self %s client %s host %s port %s" % (self, client, host, str(port)))
        self.users.append(client)

    @message
    def hi_msg(self, client, name):
        """
        """
        print("Got hi_msg from", client)
        client.name = '%s-%d' % (name, len(self.users))
        client.put('select_game_request_msg', *self.GAMES)

    @message
    def select_game_reply_msg(self, client, game):
        """
        """
        self.game = game
        players = self.players[game.lstrip()]
        players.append(Player(client.name, client))
        names = [p.client.name for p in players]
        for p in players:
            p.client.put('waiting_msg', 3-len(players), *names)
        if len(players) == 3:
            d = self.deck= Deck99()
            d.shuffle()
            d.deal(players)
            for p in players:
                p.client.put('trumps_msg', None)
                self.bids = 0
        
    @message
    def finished_msg(self, client):
        """
        Only finish when no users.
        """
        self.users.remove(client)
        if not self.users:
            IOGui.finished_msg(self, client)

    def wait4play(self, client=None):
        """
        """
        p = self.players[self.game]
        if client:
            while p[0].client != client:
                p.insert(0, p.pop())
        else:
            p.insert(0, p.pop())
        p[0].client.put('play_card_msg')
        for i in (1,2):
            p[i].client.put('waiting_for_msg', p[0].client.name)
       
    @message
    def bid_msg(self, client, *bid):
        """
        """
        self.bids += 1
        if self.bids==3:
            self.hand = 1
            self.played = 0
            self.wait4play()

    @message
    def play_card_msg(self, client, card):
        """
        """
        players = self.players[self.game] 
        for p in players:
            p.client.put('played_card_msg', card, self.hand)
        self.played += 1
        if self.played ==3:
            self.played = 0
            self.hand +=1
        else:
            self.wait4play()

    @message
    def i_won_msg(self, client):
        """
        """
        print(client, 'won')
        self.wait4play(client)
        
CardServerGui(ServerIO(port=20000, name=NAME))
