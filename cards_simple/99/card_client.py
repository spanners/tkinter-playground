"""
A client to play a hand of cards through a server with several other clients.

Ok so this can only play 99,.. but its a start!
"""

import sys

sys.path.append("..")

import time

from getpass import getuser

try:
    from Tkinter import *
except:
    from tkinter import *


from cards_simple.iogui import IOGui, message
from cards_simple.inout import ClientIO

from cards_simple.deck import Card, Player

NAME = sys.argv[1] if len(sys.argv)>1 else getuser()

class CardClientGui(IOGui):
    """
    """
    BID_VALUE = {'clubs': 3, 'hearts': 2, 'spades': 1, 'diamonds': 0}

    def create_widgets(self):
        """
        """
        self.trumps = w = Label(self.root, text='')
        w.pack(side=TOP, expand=YES, fill=X)
        self.label = w = Label(self.root, text='Waiting for Server')
        w.pack(side=TOP, expand=YES, fill=X)
        self.canvas = w = Canvas(self.root, bg='white',width=800, height=400)
        w.pack(side=TOP, expand=YES, fill=BOTH)
        self.button = w = Button(self.root, text='', state=DISABLED)
        w.pack(side=TOP, expand=YES, fill=X)


    def bid_cmd(self):
        """
        Send the bid to the server.
        """
        self.put('bid_msg', *[c for c in self.bid])
        self.label.config(text='Waiting to play')
        self.button.config(text='', command=None, state=DISABLED)
        self.bind_cards( self.select_no_card, self.player, self.bid )
        
    def delete_all(self):
        """
        """
        self.cardidx = 0
        self.cardy = 20
        self.texty = 10
        self.canvas.delete('all')
        
    def create_text(self, text):
        """
        """
        result = self.canvas.create_text(10, self.texty, text=text, anchor=NW)
        self.texty += 10
        return result

    def bind_cards(self, method, *hands):
        """
        """
        for h in hands:
            for card in h:
                self.canvas.tag_bind(str(card), '<1>', lambda p0, p2=card, call=method: call(p0, p2))
        
    def create_card(self, card, inc=1):
        """
        """
        #if not hasattr(card, 'tkim'):
        card.tkim = PhotoImage(file=card.image_file)
        cidx = self.cardidx
        self.canvas.create_image(20+40*cidx, self.cardy, image=card.tkim, anchor=NW, tag=str(card))
        self.cardidx += inc

    def select_bid_card(self, event, card):
        """
        """
        if card in self.bid:
            self.bid.give(self.player, card)
        elif len(self.bid)!=3:
            self.player.give(self.bid, card)
        if len(self.bid)==3:
            self.button.config(text='Bid', command=self.bid_cmd, state=NORMAL)
        else:
            self.button.config(text='', command=None, state=DISABLED)
        self.show_cards()
        total = 0
        for c in self.bid:
            total += self.BID_VALUE[c.suit]
        self.label.config(text='You bid: %d' % total)
        self.bid_total = total

    def select_no_card(self, event, card):
        """
        """

    @message
    def started_msg(self, sender, host, port):
        """
        On startup say who you are.
        """
        self.put = sender.put # save the put command
        print("Saying hi to %s" % sender)
        sender.put('hi_msg', NAME)
                
    @message
    def select_game_request_msg(self, sender, *games):
        """
        """
        self.label.config(text='Select Game Now...')
        self.delete_all()
        self.canvas.configure(bg='darkgreen')
        for idx, game in enumerate(games):
            self.canvas.tag_bind(self.create_text(text=game), '<1>', lambda e, g=game: self.select_game_cmd(e, g))

    def select_game_cmd(self, event, game) :
        """
        """
        self.label.config(text='Wait for other Players')
        self.put('select_game_reply_msg', game)
        self.delete_all()

    @message
    def trumps_msg(self, sender, trumps):
        """
        """
        self.trump_suit = trumps
        self.trumps.config(text='Trumps:%s' % trumps)
        self.label.config(text='Select 3 cards for bid')
        self.bind_cards( self.select_bid_card, self.player, self.bid )
        
    @message
    def waiting_msg(self, sender, number, *names):
        """
        """
        number = int(number)
        self.create_text(text='waiting for %s players %s already waiting' % (number, ''.join(names)))
        if number == 0:
            self.player = Player(name=NAME)
            self.bid = Player(name='Bid')
            self.hands = []
            self.hand = None
            self.won_count = 0

    def show_cards(self):
        """
        """
        self.delete_all()
        for h in [self.player, self.bid]:
            h.sort()
            for c in h:
                self.create_card(c)
            if len(h):
                self.cardidx += 2
        self.cardidx = 0
        for h in self.hands:
            for idx, c in enumerate(h):
                self.cardy = 150+idx*30
                self.create_card(c, 0)
            self.cardidx += 2
        
    @message
    def deal_card_msg(self, sender, card):
        """
        """
        self.label.config(text='Deal in progress...')
        self.player.add(Card(*card.split('-')))
        self.show_cards()
        
    @message
    def error_msg(self, sender, msg):
        """
        """
        self.delete_all()
        self.create_text(text=msg)

    def select_play_card(self, event, card):
        """
        """
        if self.hands and len(self.hands[-1])!=3:
            if card.suit != self.hands[-1][0].suit and self.player.count_cards(suit=self.hands[-1][0].suit)!=0:
                self.label.config(text='Must play %s' % self.hands[-1][0].suit)
                return
        self.label.config(text='Waiting...')
        self.bind_cards( self.select_no_card, self.player )
        self.played = self.player.disappear(card)
        self.put('play_card_msg', card)
        self.show_cards()
        
    @message
    def play_card_msg(self, sender):
        """
        """
        self.label.config(text='Select card to play')
        self.bind_cards( self.select_play_card, self.player )

    def calc_result(self):
        """
        If you are the winner then tell the server.
        Otherwise hide the cards.
        """
        hand = self.hands[-1]
        if self.trump_suit == 'None':
            winner = hand.highest_rank(hand[0].suit)
        else:
            winner = hand.highest_rank(self.trump_suit)
        if str(self.played) == str(winner):
            self.put('i_won_msg')
            self.won_count += 1
        else:
            hand.show_backs()
         
    @message
    def played_card_msg(self, sender, card, hand):
        """
        """
        if hand != self.hand:
            self.hand = hand
            self.hands.append(Player(hand))
        self.hands[-1].add(Card(*card.split('-')))
        if len(self.hands[-1])==3:
            self.calc_result()
        self.show_cards()

    @message
    def waiting_for_msg(self, sender, who):
        """
        """
        self.label.config(text='Waiting for %s' % who)
        
CardClientGui(ClientIO(port=20000, name=NAME))
