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
    ('Ten',   'T', 10),
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
        self.rank = rank
        self.suit = suit

    def color(self, width=8):
        color = 'red' if self.suit[2] == 'R' else 'black'
        rank = '10' if self.rank[2] == 10 else self.rank[1]
        text = '{}{} '.format(rank, self.suit[3])
        return colorize(text.ljust(width), fg=color, bg='white', bgalt=True)

    def __repr__(self):
        suit = self.suit[4] if self.suit[2] == 'R' else self.suit[3]
        return '{}{} ({} of {})'.format(
            self.rank[1], suit, self.rank[0], self.suit[0]
        )

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
        self.cards = self.used
        self.used = []

    def deal(self, num_hands, num_per_hand=None):
        hands = []
        for n in range(0, num_hands):
            hands.append([])
        for n in range(0, num_hands):
            for i,c in enumerate(self):
                hand = i % num_hands
                if not num_per_hand or len(hands[hand]) < num_per_hand:
                    hands[hand].append(c)
        return hands


