import random
import pytest

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def show (self):
        print("{} of {}".format(self.val, self.suit))


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        self.cards = []
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1, 14):
                self.cards.append(Card(s , v))
               

    def add_joker(self, num):
        for t in range(0, num):
            self.cards.append('Joker')
            print("Joker Added")

    def shuffle(self):
        for i in range(len(self.cards) -1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

        

    def show_deck(self):
        for i in self.cards:
            i.show()
            
    def draw(self):
        return self.cards.pop()

class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name

    def draw(self, deck):
        self.hand.append(deck.draw())

    def discard(self):
        return self.hand.pop()

    def showhand(self):
        for card in self.hand:
            card.show()


            
def test_show():
    suit = 'Heart'
    val = 6
    card = Card('Heart', 6)
    assert suit == 'Heart'
    assert val == 6 


def test_build():
    A = Deck.build()
    assert len(A) == 52

