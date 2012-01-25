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

class CardNotInStackError(Exception):
    pass

class InvalidCardStackAdditionError(Exception):
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
    >>> print rank.prev_rank()
    None
    >>> rank.next_rank().prev_rank().label
    'Ace'
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
            return CardRank(self.num - 1)

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
        if self.color == 'red':
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

    @property
    def label(self):
        return '{} of {}'.format(self.rank.label, self.suit.label)

    @property
    def code(self):
        return '{}{}'.format(self.rank.c, self.suit.c)

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
    5♡
    >>> stack.add_card(Card('6','c'))
    >>> stack.length
    2
    >>> print stack
    5♡, 6♣
    """

    def __init__(self, cards=[], maxlen=None):
        self.cards = cards
        self.maxlen = maxlen

    def top_card(self):
        try:
            return self.cards[-1]
        except IndexError:
            return None

    def bottom_card(self):
        return self.cards[0]

    def add_card(self, card, force=False):
        self = self + card

    def add_stack(self, stack, force=False):
        self = self + stack

    def pop_stack(self, length):
        stack = self.__class__()
        for n in range(0, length):
            stack.add_card(self.remove_top_card())
        stack.cards.reverse()
        return stack

    def slice_stack(self, card):
        try:
            index = self.cards.index(card)
        except ValueError:
            raise CardNotInStackError
        else:
            stack = self.__class__(self.cards[index:])
            self.cards = self.cards[:index]
            return stack

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
        cards = ['{}{}'.format(c.rank.c, c.suit.symbol) for c in self.cards]
        return ', '.join(cards)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.maxlen and self.length + other.length >= self.maxlen:
                raise CardStackFullError
            else:
                self.cards = self.cards + other.cards
        elif isinstance(other, Card):
            if self.maxlen and self.length == self.maxlen:
                raise CardStackFullError
            else:
                self.cards.append(other)
        else:
            raise InvalidCardStackAdditionError


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
    >>> as_str = deck.__repr__()
    >>> new_deck = Deck()
    >>> new_deck.loads(as_str)
    >>> new_deck.__repr__() == deck.__repr__()
    True
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

    def loads(self, string, overwrite=True):
        if overwrite:
            self.cards = []
        cards = string.split(',')
        for c in cards:
            rank = c[:-1]
            suit = c[-1]
            self.cards.append(Card(rank,suit))


    def __repr__(self):
        return ','.join(['{}{}'.format(c.rank.c,c.suit.c) for c in self.cards])



if __name__ == '__main__':
    import doctest
    doctest.testmod()
