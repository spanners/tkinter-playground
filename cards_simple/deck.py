import random
from time import sleep
from functools import total_ordering

ROOT = r'../cardset-gdkcard-bonded'

@total_ordering
class Card(object):
    """
    """
    suit_string = ['clubs', 'hearts', 'spades', 'diamonds']
    rank_string = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
    back_file = '%s/back191.gif' % ROOT
    image_size = 79, 123

    RANK = {'two':'02', 'three':'03', 'four':'04', 'five':'05', 'six':'06', 'seven':'07', 'eight':'08', 'nine':'09',
            'ten':'10', 'jack':'11', 'queen':'12', 'king':'13', 'ace':'01'}
    
    def __init__(self, suit, rank):
        """
        """
        self.suit = suit
        self.rank = rank
        self.image_file = '%s/%s%s.gif' % (ROOT, self.RANK[rank], suit[0].rstrip())

    def show_back(self):
        """
        """
        self.image_file = self.back_file
        
    def __cmp__(self, other):
        """
        """
        if self.suit == other.suit:
            return self.rank_string.index(other.rank) - self.rank_string.index(self.rank)
        return self.suit_string.index(self.suit)-self.suit_string.index(other.suit)
    
    def __repr__(self):
        """
        """
        return '%s-%s' % (self.suit, self.rank)

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank_string.index(other.rank) - self.rank_string.index(self.rank)
        return self.suit_string.index(self.suit)-self.suit_string.index(other.suit)

class Owner(object):
    db = {}

    def __init__(self, name, client=None):
        assert name not in self.db
        Owner.db[name] = self
        self._client =client
        self._data = []
        self.name = name

    @property
    def client(self):
        """
        """
        return self._client
    
    def add(self, card, msg=None):
        self._data.append(card)
        if self._client:
            assert msg
            self._client.put(msg, card)

    def __iter__(self):
        for d in self._data:
            yield d
            
    @property
    def data(self):
        return self._data

    def shuffle(self):
        saved = self._data
        card = []
        while saved:
            this = random.choice(saved)
            saved.remove(this)
            card.append(this)
        self._data = card

    def sort(self):
        self._data.sort()

    def give(self, owner, card):
        """
        remove the card and give it to another.
        """
        self.data.remove(card)
        owner.add(card)

    def disappear(self, card):
        """
        Use when no one to give it to.
        return in case its any use.
        """
        self.data.remove(card)
        return card
        
    def give_all(self, owner):
        card = self._data
        while card:
            owner.add(card.pop())
            
    def deal(self, owners, delay=0.0):
        card = self._data
        while card:
            for o in owners:
                if card:
                    o.add(card.pop(), 'deal_card_msg')
                    if delay:
                        sleep(delay)

    def discard(self, suit, rank):
        for c in self._data:
            if c.suit == suit and c.rank==rank:
                self._data.remove(c)
                return

    def highest_rank(self, suit):
        """
        Search for the highest rank of a given suit.
        """
        high = None
        for c in self:
            if c.suit!=suit:
                continue
            elif high is None:
                high = c
            elif c < high: # ordering a bit strange?
                high = c
        assert high is not None
        return high
        
    def count_cards(self, suit=None, rank=None):
        """
        """
        if rank and suit:
            result =[c for c in self if c.suit==suit and c.rank==rank]
        elif rank:
            result =[c for c in self if c.suit==suit]
        elif suit:
            result =[c for c in self if c.suit==suit]
        else:
            result = []
        return len(result)

    def show_backs(self):
        """
        """
        for c in self:
            c.show_back()
            
    def __getitem__(self, index):
        """
        """
        return self._data[index]
    
    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return '\n%s\n\t%s\n' % (self.name, self._data)
    
class Deck(Owner):
    count = 0
    def __init__(self, decks=1):
        Deck.count+=1
        Owner.__init__(self, 'Deck#%s' % self.count)
        for deck in range(decks):
            for suit in Card.suit_string:
                for rank in Card.rank_string:
                    if not self.discard(suit, rank):
                        self.add(Card(suit, rank))

    def discard(self, suit, rank):
        return False

class Player(Owner):
    pass

