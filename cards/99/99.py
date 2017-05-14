import sys

sys.path.append("..")

from cards.deck import Deck, Player

player=[Player('steve'), Player('vicki'), Player('fran')]

class Deck99(Deck):
    def discard(self, suit, rank):
        return rank in ('two', 'three', 'four', 'five')

d=Deck99()

try:
    from Tkinter import *
except:
    from tkinter import *

def card_bind(event, player, card, image):
    canvas.move(str(card), 0, -20 if card.selected else 20)
    card.selected = not card.selected
    
def display_hand(pidx, p):
    canvas.create_text(10,10+130*pidx, text=p.name, anchor=NW)
    for cidx, c in enumerate(p):
        c.tkim = PhotoImage(file=c.image_file)
        w,h = c.image_size
        i = canvas.create_image(20+80*cidx, 20+130*pidx, image=c.tkim, anchor=NW, tag=str(c))
        canvas.tag_bind(i, '<1>', lambda p0, p1=p, p2=c, p3=i: card_bind(p0, p1, p2, p3))

def redeal():
    [p.give_all(d) for p in player]
    [setattr(c, 'selected', False) for c in d]
    d.shuffle()
    d.deal(player)
    [p.sort() for p in player]
    canvas.delete('all')
    [display_hand(pidx, p) for pidx, p in enumerate(player)]
    canvas.create_window(20+80*6, 480, window=Button(root, text='Redeal', command=redeal))
    p=player.pop()
    player.insert(0, p)
    
root= Tk()
canvas = Canvas(root, bg='darkgreen', width=20*2+80*12, height=500)
redeal()
canvas.pack(expand=YES, fill=BOTH)
root.mainloop()
