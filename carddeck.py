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

class CardStackFullError(Exception):
    pass

class BaseObject(object):
    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.__dict__ == other.__dict__


class CardRank(BaseObject):
    """
    >>> rank = CardRank('Ace')
    >>> rank.num
    1
    >>> rank.label
    'Ace'
    >>> next = CardRank('Two')
    >>> rank.next_rank() == next
    True
    """
    rank = None

    def __init__(self, rank):
        if isinstance(rank, str):
            rank = rank.title()
        for r in CARDRANKS:
            if rank == r or rank in r:
                self.rank = r
                break
        if not self.rank:
            raise InvalidCardRankError(rank)

    def next_rank(self, round_the_corner=False):
        if self.label == 'King':
            if round_the_corner:
                return CardRank('Ace')
            else:
                return None
        else:
            return CardRank(self.num + 1)

    def prev_rank(self, round_the_corner=False):
        if self.label == 'Ace':
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


class CardSuit(BaseObject):
    """
    >>> h = CardSuit('Hearts')
    >>> h.label
    'Hearts'
    """
    suit = None

    def __init__(self, suit):
        if isinstance(suit, str):
            suit = suit.title()
        for s in CARDSUITS:
            if suit == s or suit in s:
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


class Card(BaseObject):
    """
    >>> c1 = Card('10','h')
    >>> c2 = Card('7', 'd')
    >>> len(c1.color())== len(c2.color())
    True
    """

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
        return colorize(text.rjust(width), fg=color, bg='white', bgalt=True)

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

class CardStack(BaseObject):
    """
    A CardStack is a list of cards in which only the top card
    is accessible
    >>> stack = CardStack([])
    >>> card = Card('5','h')
    >>> stack.add_card(card)
    >>> stack.length
    1
    >>> print stack
    Five of Hearts
    >>> stack.add_card(Card('6','c'))
    >>> stack.length
    2
    >>> print stack
    Five of Hearts, Six of Clubs
    """

    def __init__(self, cards, maxlen=None):
        self.cards = cards
        self.maxlen = maxlen

    def top_card(self):
        try:
            return self.cards[-1]
        except IndexError:
            return None

    def add_card(self, card):
        if self.length == self.maxlen:
            raise CardStackFullError
        else:
            self.cards.append(card)

    def card_at(self, position):
        try:
            return self.cards[position]
        except IndexError:
            return None

    def remove_top_card(self):
        return self.cards.pop()

    def remove_card(self):
        return self.remove_top_card()

    @property
    def length(self):
        return len(self.cards)

    def __repr__(self):
        cards = ['{} of {}'.format(c.rank.label, c.suit.label) for c in self.cards]
        return ', '.join(cards)


class Deck(BaseObject):
    """
    >>> deck = Deck()
    >>> len(deck.cards)
    52
    >>> deck = Deck(2)
    >>> len(deck.cards)
    104
    >>> testcard = Card(3, 'Clubs')
    >>> deck.cards.count(testcard)
    2
    """

    def __init__(self, number_of_decks=1):
        self.cards = []
        self.used = []
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
