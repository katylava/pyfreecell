#!/usr/bin/env python

import copy
from carddeck import Card, CardStack, Deck, CardSuit, CardRank

class FreecellCard(Card):

    def __init__(self, rank, suit):
        super(FreecellCard, self).__init__(rank, suit)

    def __repr__(self):
        return self.color(8)


class FreecellDeck(Deck):
    """
    >>> deck = FreecellDeck()
    >>> len(deck.cards)
    52
    >>> card = deck.next()
    >>> isinstance(card, FreecellCard)
    True
    """

    def __init__(self):
        super(FreecellDeck, self).__init__()
        basic_cards = self.cards
        self.cards = []
        for c in basic_cards:
            self.cards.append(FreecellCard(c.rank, c.suit))


class NoFreecellsError(Exception):
    pass

class FreeCellOccupiedError(Exception):
    pass

class InvalidColumnCardError(Exception):
    pass

class InvalidFoundationCardError(Exception):
    pass

class FreecellInvalidMoveError(Exception):
    pass


class FoundationPile(CardStack):
    """
    >>> deck = FreecellDeck()
    >>> fp = FoundationPile('Hearts')
    >>> ace_hearts = FreecellCard(rank=CardRank('Ace'), suit=CardSuit('Hearts'))
    >>> two_hearts = FreecellCard(rank=CardRank('Two'), suit=CardSuit('Hearts'))
    >>> fp.next_card() == ace_hearts
    True
    >>> fp.add_card(ace_hearts)
    >>> fp.next_card() == two_hearts
    True
    >>> fp.add_card(two_hearts)
    >>> fp.rank() == CardRank('Two')
    True
    """

    def __init__(self, suit):
        super(FoundationPile, self).__init__([])
        self.suit = CardSuit(suit)

    def rank(self):
        top = self.top_card()
        if top:
            return top.rank
        else:
            return None

    def add_card(self, card):
        if card == self.next_card():
            self.cards.append(card)
        else:
            raise InvalidFoundationCardError

    def next_card(self):
        top = self.top_card()
        if not top:
            return FreecellCard(rank=CardRank('Ace'), suit=self.suit)
        else:
            return FreecellCard(top.rank.next_rank(), suit=self.suit)


class AltDescCardColumn(CardStack):

    def add_card(self, card):
        if card in self.allowed_cards():
            self.cards.append(card)
        else:
            raise InvalidColumnCardError

    def allowed_cards(self):
        top = self.top_card()
        rank = top.rank.prev_rank()
        if top.color == 'red':
            return [
                FreecellCard(rank, CardSuit('Spades')),
                FreecellCard(rank, CardSuit('Clubs')),
            ]
        else:
            return [
                FreecellCard(rank, CardSuit('Hearts')),
                FreecellCard(rank, CardSuit('Diamonds')),
            ]


class Freecells:
    """
    >>> fcs = Freecells()
    >>> fcs.free()
    4
    """
    empty_cell = CardStack([], 1)

    def __init__(self):
        self.cells = []
        for n in range(0,4):
            self.cells.append(copy.copy(self.empty_cell))

    def free(self):
        return self.cells.count(self.empty_cell)

    def add_card(self, card, position=None):
        if self.free():
            if not position:
                position = self.cells.index(None)
            if self.cells[position] == None:
                self.cells[position].add_card(card)
                return position
            else:
                raise FreeCellOccupiedError
        else:
            raise NoFreecellsError

    def get_card_at_position(self, position):
        return self.cells[position]

    def remove_card_from_position(self, position):
        card = self.cells[position]
        self.cells[position] = None
        return card

    def remove_card(self, card):
        position = self.cells.index(card)
        self.cells[position] = None


class FreecellGame():
    """
    >>> game = FreecellGame()
    >>> game.columns[0].length
    7
    >>> game.columns[7].length
    6
    >>> game.freecell_count()
    4
    """

    def __init__(self):
        self.deck = FreecellDeck()
        self.deck.shuffle()
        self.columns = []
        self.freecells = Freecells()
        self.foundation = {
            'S': FoundationPile('Spades'),
            'H': FoundationPile('Hearts'),
            'D': FoundationPile('Diamonds'),
            'C': FoundationPile('Clubs'),
        }
        self.history = []
        columns = self.deck.deal(8)
        for c in columns:
            self.columns.append(AltDescCardColumn(c))

    def move(self, moves):
        moves = list(moves)
        cols = list('asdfjkl;')
        cells = list('qwert')
        found = 'u'
        while len(moves) >= 2:
            fr, to = (moves.pop(0), moves.pop(0))
            if fr in cols and to in cols:
                self.move_from_column_to_column(cols.index(fr), cols.index(to))
            elif fr in cols and to in cells:
                fcpos = None if to == 't' else cells.index(to)
                self.move_to_freecell(cols.index(fr), fcpos)
            elif fr in cols and to in found:
                self.move_from_column_to_foundation(cols.index(fr))
            elif fr in cells and to in cols:
                self.move_from_freecell_to_column(cells.index(fr), cols.index(to))
            elif fr in cells and to in found:
                self.move_from_freecell_to_foundation(cells.index(fr))


    def freecell_count(self):
        return self.freecells.free()

    def move_to_freecell(self, from_col, position=None):
        card = self.columns[from_col].top_card()
        try:
            self.freecells.add_card(card, position)
        except NoFreecellsError:
            print 'No free cells'
        except FreeCellOccupiedError:
            print 'Already a card in that cell'
        else:
            self.columns[from_col].remove_top_card()

    def move_from_freecell_to_column(self, fc, col):
        card = self.freecells.get_card_at_position(fc)
        try:
            self.columns[col].add_card(card)
        except InvalidColumnCardError:
            print 'Bad move'
        else:
            self.freecells.remove_card(card)

    def move_from_column_to_column(self, from_col, to_col):
        card = self.columns[from_col].top_card()
        try:
            self.columns[to_col].add_card(card)
        except InvalidColumnCardError:
            print 'Bad move'
        else:
            self.columns[from_col].remove_top_card()

    def move_from_freecell_to_foundation(self, fc):
        card = self.freecells.get_card_at_position(fc)
        try:
            self.foundation[card.suit.c].add_card(card)
        except InvalidFoundationCardError:
            print 'Invalid foundation card'
        else:
            self.freecells.remove_card(card)

    def move_from_column_to_foundation(self, col):
        card = self.columns[col].top_card()
        try:
            self.foundation[card.suit.c].add_card(card)
        except InvalidFoundationCardError:
            print 'Invalid foundation card'
        else:
            self.columns[col].remove_top_card()

    def draw_board(self):
        pass



if __name__ == '__main__':
    from optparse import OptionParser
    usage = "Usage: %prog [--test]"
    parser = OptionParser(usage=usage)
    parser.add_option('-t', '--test', action='store_true', default=False,
                      help="Run doctests")
    options, args = parser.parse_args()

    if options.test:
        import doctest
        doctest.testmod()
    else:
        print "eventually running this will let you play the game"
