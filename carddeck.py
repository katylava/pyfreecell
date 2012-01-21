# -*- coding: utf-8 -*-

import random
from colorize import colorize

CARDRANKS = (
    ('Ace',   'A', 1),
    ('Two',   '2', 2),
    ('Three', '3', 3),
    ('Four',  '4', 4),
    ('Five',  '5', 5),
    ('Six',   '6', 6),
    ('Seven', '7', 7),
    ('Eight', '8', 8),
    ('Nine',  '9', 9),
    ('Ten',   '10', 10),
    ('Jack',  'J', 11),
    ('Queen', 'Q', 12),
    ('King',  'K', 13),
)

# Most common ordering, high to low
CARDSUITS = (
    ('Spades',   'S', 'B', '♠', '♤'),
    ('Hearts',   'H', 'R', '♥', '♡'),
    ('Diamonds', 'D', 'R', '♦', '♢'),
    ('Clubs',    'C', 'B', '♣', '♧'),
)

class Card:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def rank(self, fmt='short'):
        return {
            'short': self._rank[1],
            'long': self._rank[0],
            'number': self._rank[2],
            'all': self._rank,
        }[fmt]

    def suit(self, fmt='ideo'):
        return {
            'ideo': self._suit[4] if self._suit[2] == 'R' else self._suit[3],
            'long': self._suit[0],
            'short': self._suit[1],
            'color': self._suit[2],
            'filled': self._suit[3],
            'outline': self._suit[4],
        }[fmt]

    def color(self, width=8):
        color = 'red' if self.suit('color') == 'R' else 'black'
        text = ' {}{} '.format(self.rank(), self.suit('filled'))
        return colorize(text.ljust(width), fg=color, bg='white', bgalt=True)

    def __repr__(self):
        return '{}{} '.format(self.rank(), self.suit())

class Deck:
    cards = []
    used = []

    def __init__(self, number_of_decks=1):
        for n in range(0, number_of_decks):
            self.load_cards()

    def __iter__(self):
        return self

    def load_cards(self):
        for suit in CARDSUITS:
            for rank in CARDRANKS:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def next(self):
        try:
            card = self.cards.pop()
        except IndexError:
            raise StopIteration
        self.used.append(card)
        return card

    def reset(self):
        self.used.reverse()
        self.cards = self.cards + self.used
        self.used = []

    def deal(self, num_hands, num_per_hand=None):
        if not num_per_hand:
            num_per_hand = len(self.cards)
        hands = []
        for n in range(0, num_hands):
            hands.append([])
        for n in range(0, num_per_hand):
            for i in range(0, num_hands):
                try:
                    hands[i].append(self.next())
                except StopIteration:
                    pass
        return hands


