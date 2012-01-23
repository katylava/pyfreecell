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
    >>> five_hearts = FreecellCard('5', 'Hearts')
    >>> fcs.add_card(five_hearts) # returns position card was added to
    0
    >>> fcs.get_card_at_position(0) == fcs.empty_cell
    False
    >>> fcs.cells
    [Five of Hearts, , , ]
    >>> fcs.empty_cell == CardStack([], 1)
    True
    >>> fcs.free()
    3
    >>> fcs.get_card_at_position(0) == five_hearts
    True
    >>> two_hearts = FreecellCard('Two', 'Hearts')
    >>> fcs.add_card(two_hearts, 3)
    3
    >>> fcs.free()
    2
    >>> fcs.first_open()
    1
    >>> fcs.cells
    [Five of Hearts, , , Two of Hearts]
    """
    empty_cell = CardStack([], 1)

    def __init__(self):
        self.cells = []
        for n in range(0,4):
            self.cells.append(copy.deepcopy(self.empty_cell))

    def free(self):
        return self.cells.count(self.empty_cell)

    def first_open(self):
        return self.cells.index(self.empty_cell)

    def add_card(self, card, position=None):
        if self.free():
            if not position:
                position = self.first_open()
            if self.cells[position].length == 0:
                self.cells[position].add_card(card)
                return position
            else:
                raise FreeCellOccupiedError
        else:
            raise NoFreecellsError

    def get_card_at_position(self, position):
        return self.cells[position].top_card()

    def remove_card_from_position(self, position):
        card = self.cells[position].top_card()
        self.cells[position].remove_top_card()
        return card

    def remove_card(self, card):
        position = self.cells.index(CardStack([card], 1))
        self.cells[position].remove_top_card()


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

    def __init__(self, deck=None):
        if not deck:
            self.deck = FreecellDeck()
            self.deck.shuffle()
        else:
            self.deck = deck
        self.columns = []
        self.freecells = Freecells()
        self.foundation = {
            'S': FoundationPile('Spades'),
            'H': FoundationPile('Hearts'),
            'D': FoundationPile('Diamonds'),
            'C': FoundationPile('Clubs'),
        }
        self.history = []
        self.replay = []
        columns = self.deck.deal(8)
        for c in columns:
            self.columns.append(AltDescCardColumn(c))

    def parse_moves(self, moves):
        movelist = []
        if moves in ['z', 'zz']:
            movelist.append(('z','z'))
        else:
            moves = list(moves)
            while len(moves) >= 2:
                movelist.append((moves.pop(0), moves.pop(0)))
        return movelist

    def move(self, moves):
        cols = list('asdfjkl;')
        cells = list('qwert')
        found = list('uiopy')
        found_order = list('SHDC')

        movelist = self.parse_moves(moves)

        for fr, to in movelist:

            if fr in cols:
                move_from = self.columns[cols.index(fr)]
            elif fr in cells[:-1]: # the last one, 't', is only for moving to
                move_from = self.freecells.cells[cells.index(fr)]
            elif fr in found[:-1]: # the last one, 'y', is only for moving to
                key = found_order[found.index(fr)]
                move_from = self.foundation[key]
            elif fr == 'z':
                # note the swapped order of 'to' and 'from' wrt to
                # order when appended to history
                card, move_to, move_from = self.history[-1]
            else:
                raise FreecellInvalidMoveError

            card = move_from.top_card()

            if to in cols:
                move_to = self.columns[cols.index(to)]
            elif to in cells:
                if to == 't':
                    index = self.freecells.first_open()
                else:
                    index = cells.index(to)
                move_to = self.freecells.cells[index]
            elif to in found:
                if to == 'y':
                    key = card.suit.c
                else:
                    key = found_order[found.index(to)]
                move_to = self.foundation[key]
            elif to == 'z':
                pass # move_to already set in fr == 'z' condition
            else:
                raise FreecellInvalidMoveError

            if self.move_card(card, move_from, move_to):
                self.replay.append('{}{}'.format(fr, to))

    def move_card(self, card, move_from, move_to):
        try:
            move_to.add_card(card)
        except:
            raise
        else:
            move_from.remove_top_card()
            self.history.append([card, move_from, move_to])
            return True

    def freecell_count(self):
        return self.freecells.free()

    def draw_board(self, colwidth=5):
        longest_column = 0
        for c in self.columns:
            if c.length > longest_column:
                longest_column = c.length







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
