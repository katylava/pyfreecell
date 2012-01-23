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

class InvalidCardRankError(Exception):
    pass

class InvalidCardSuitError(Exception):
    pass


class CardRank:

    def __init__(self, rank):
        if isinstance(rank, str):
            rank = rank.title()
        for r in CARDRANKS:
            if rank == r or rank in r:
                self.rank = r
                break
        if not self.rank:
            raise InvalidCardRankError

    def next_rank(self, round_the_corner=False):
        if self.rank.label == 'King':
            if round_the_corner:
                return CardRank('Ace')
            else:
                return None
        else:
            return CardRank(self.rank.num + 1)

    def prev_rank(self, round_the_corner=False):
        if self.rank.label == 'Ace':
            if round_the_corner:
                return CardRank('King')
            else:
                return None
        else:
            return CardRank(self.rank.num - 1)

    @property
    def label(self):
        return self.rank[0]

    @property
    def c(self):
        return self.rank[1]

    @property
    def num(self):
        return self.rank[2]

    def __repr__(self):
        return self.c


class CardSuit:

    def __init__(self, suit):
        for s in CARDSUITS:
            if suit == s or suit.title() in s:
                self.suit = s
                break
        if not self.suit:
            raise InvalidCardSuitError

    @property
    def label(self):
        return self.suit[0]

    @property
    def c(self):
        return self.suit[1]

    @property
    def color(self):
        col = self.suit[2]
        return 'red' if col == 'R' else 'black'

    @property
    def filled_symbol(self):
        return self.suit[3]

    @property
    def hollow_symbol(self):
        return self.suit[4]

    @property
    def symbol(self):
        if self.color == 'R':
            return self.hollow_symbol
        else:
            return self.filled_symbol

    def __repr__(self):
        return self.symbol


class Card:

    def __init__(self, rank, suit):
        if isinstance(rank, CardRank):
            self.rank = rank
        else:
            self.rank = CardRank(rank)
        if isinstance(suit, CardSuit):
            self.suit = suit
        else:
            self.suit = CardSuit(suit)

    def color(self, width=8):
        color = self.suit.color
        text = ' {}{} '.format(self.rank.c, self.suit.filled_symbol)
        return colorize(text.ljust(width), fg=color, bg='white', bgalt=True)

    def is_same_suit_as(self, card):
        return self.suit == card.suit

    def is_same_color_as(self, card):
        return self.suit.color == card.suit.color

    def is_same_rank_as(self, card):
        return self.rank == card.rank

    def rel_rank(self, card, round_the_corner=False):
        rank_diff = self.rank.num - card.rank.num
        if round_the_corner and abs(rank_diff) == 12:
            # if self is A and card is K, rank_diff is -12, 
            # but we want it to be 1
            # if self is K and card is A, rank_diff is 12, 
            # but we want it to be -1
            rank_diff = 1 if rank_diff == -12 else -1

    def __repr__(self):
        return '{}{} '.format(self.rank, self.suit)

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


