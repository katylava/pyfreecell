#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from colorize import colorize
from carddeck import Card, CardStack, Deck, CardSuit, CardRank

class FreecellCard(Card):

    def __init__(self, rank, suit):
        super(FreecellCard, self).__init__(rank, suit)

    def draw(self, width=8):
        color = self.suit.color
        text = ' {}{} '.format(self.rank.c, self.suit.filled_symbol)
        return colorize(text.rjust(width), fg=color, bg='white', var='und', bgalt=True)


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

class InvalidColumnStackError(Exception):
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

    def add_card(self, card, force=False):
        if isinstance(card, CardStack):
            card = card.top_card()
        if card == self.next_card():
            self = self + card
        else:
            msg = "{} on {}".format(card, self.top_card())
            raise InvalidFoundationCardError(msg)

    def next_card(self):
        top = self.top_card()
        if not top:
            return FreecellCard(rank=CardRank('Ace'), suit=self.suit)
        else:
            return FreecellCard(top.rank.next_rank(), suit=self.suit)

    def __repr__(self):
        if self.length == 0:
            return self.suit.symbol
        else:
            return self.top_card().__repr__()


class AltDescCardColumn(CardStack):
    """
    >>> jc = FreecellCard('J','c')
    >>> qh = FreecellCard('Q','h')
    >>> col = AltDescCardColumn()
    >>> col.add_card(qh)
    >>> col.top_card().rank.prev_rank().label
    'Jack'
    >>> jc.rank == col.top_card().rank.prev_rank()
    True
    >>> col.add_card(jc)
    >>> col.valid()
    True
    >>> td = FreecellCard(10,'d')
    >>> col.add_card(td)
    >>> col.valid()
    True
    >>> stack = col.slice_stack(jc)
    >>> stack.top_card() == td
    True
    >>> stack.bottom_card() == jc
    True
    >>> deck = Deck()
    >>> deck.shuffle()
    >>> fresh = AltDescCardColumn(deck.cards[:5])
    >>> fresh.add_stack(stack, force=True)
    >>> fresh.top_stack() == stack
    True
    >>> fresh.add_card(FreecellCard(9,'s'))
    >>> fresh.top_stack().length
    3
    >>> fresh.top_stack().bottom_card() == jc
    True
    >>> js = FreecellCard('J','s')
    >>> fresh.top_stack_for(js).bottom_card() == td
    True
    >>> print fresh.top_stack_for(FreecellCard(2,'s'))
    None
    >>> print fresh.top_stack_for(FreecellCard('k','s'))
    None
    >>> fresh.remove_top_stack_for(js)
    Ten of Diamonds, Nine of Spades
    >>> fresh.top_card() == jc
    True
    """

    def top_stack(self):
        clone = copy.deepcopy(self)
        while not clone.valid():
            clone.cards.pop(0)
        return clone

    def add_card(self, card, force=False):
        if force or self.allow_card(card):
            self = self + card
        else:
            msg = "{} on {}".format(card, self.top_card())
            raise InvalidColumnCardError(msg)

    def add_stack(self, stack, force=False):
        if isinstance(stack, AltDescCardColumn):
            if force or self.allow_stack(stack):
                self = self + stack
        else:
            raise InvalidColumnStackError

    def allow_stack(self, stack):
        return self.allow_card(stack.bottom_card()) and stack.valid()

    def allow_card(self, card):
        top = self.top_card()
        if not top:
            return True
        else:
            return card.rank == top.rank.prev_rank() \
                   and not card.is_same_color_as(top)

    def top_stack_for(self, card):
        stack = self.top_stack()
        temp = self.__class__([card])
        while stack.length > 0 and not temp.allow_stack(stack):
            stack.cards.pop(0)
        return None if stack.length == 0 else stack

    def remove_top_stack(self):
        bottom_card = self.top_stack().bottom_card()
        return self.slice_stack(bottom_card)

    def remove_top_stack_for(self, card):
        bottom_card = self.top_stack_for(card).bottom_card()
        return self.slice_stack(bottom_card)

    def valid(self):
        temp = self.__class__([])
        for c in self.cards:
            try:
                temp.add_card(c)
            except InvalidColumnCardError:
                return False
        return True


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
    >>> fcs.all_cards()
    [5♥ , None, None, 2♥ ]
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

    def all_cards(self):
        return [stack.top_card() for stack in self.cells]

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
    mv_cols = list('asdfjkl;')
    mv_cells = list('qwertg')
    mv_found = list('uiopyh')
    mv_found_order = list('SHDC')


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

    def top_cards(self):
        return [c.top_card() for c in self.columns]

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
        movelist = self.parse_moves(moves)

        for fr, to in movelist:

            if fr in self.mv_cols:
                move_from = self.columns[self.mv_cols.index(fr)]
            elif fr in self.mv_cells[:-2]: # the last ones are only for moving 'to'
                move_from = self.freecells.cells[self.mv_cells.index(fr)]
            elif fr in self.mv_found[:-2]: # the last ones are only for moving 'to' 'y', is only for moving to
                key = self.mv_found_order[self.mv_found.index(fr)]
                move_from = self.foundation[key]
            elif fr == 'z':
                # note the swapped order of 'to' and 'from' wrt to
                # order when appended to history
                card, move_to, move_from = self.history[-1]
            else:
                raise FreecellInvalidMoveError("'{}' is not a move".format(fr))

            card = move_from.top_card()

            if to in self.mv_cols:
                move_to = self.columns[self.mv_cols.index(to)]
            elif to in self.mv_cells:
                if to in 'tg':
                    index = self.freecells.first_open()
                else:
                    index = self.mv_cells.index(to)
                move_to = self.freecells.cells[index]
            elif to in self.mv_found:
                if to in 'yh':
                    key = card.suit.c
                else:
                    key = self.mv_found_order[self.mv_found.index(to)]
                move_to = self.foundation[key]
            elif to == 'z':
                pass # move_to already set in fr == 'z' condition
            else:
                raise FreecellInvalidMoveError("'{}' is not a move".format(to))

            if self.move_card(card, move_from, move_to, (fr=='z')):
                self.replay.append('{}{}'.format(fr, to))

    def move_card(self, card, move_from, move_to, force=False):
        try:
            move_to.add_card(card, force)
        except:
            self.move_stack(move_from, move_to, force=force)
        else:
            move_from.remove_top_card()
            self.history.append([card, move_from, move_to])
            return True

    def move_stack(self, move_from, move_to, force=False):
        stack = move_from.top_stack_for(move_to.top_card())

        if not stack:
            raise FreecellInvalidMoveError(
                "No cards in '{}' for {}".format(move_from, move_to.top_card())
            )

        if stack.length <= self.freecell_count()+1:
            try:
                move_to.add_stack(stack)
            except InvalidColumnStackError:
                raise
            else:
                move_from.remove_top_stack_for(move_to.top_card())
        else:
            raise FreecellInvalidMoveError(
                "Not enough freecells to move stack '{}'".format(stack)
            )


    def move_all_to_foundation(self):
        next_on_founds = [f.next_card() for f in self.foundation.values()]
        for i, card in enumerate(self.top_cards()):
            if card in next_on_founds:
                self.move('{}y'.format(self.mv_cols[i]))


    def freecell_count(self):
        return self.freecells.free() + self.top_cards().count(None)

    def draw_board(self, cardwidth=8, suit_offset=2):
        # the suit symbols take up less than one character, so the offset
        # is how much you have to subtract from the width in spots that
        # do not have a suit character
        if cardwidth - suit_offset < 5:
            cardwidth = 5 + suit_offset

        longest_column = 0
        for c in self.columns:
            if c.length > longest_column:
                longest_column = c.length

        space = " "*((cardwidth - suit_offset)+1)
        blank = "_"*(cardwidth - suit_offset) + " "
        found = "{}" + "_"*(cardwidth - suit_offset - 1) + " "

        # empty space before foundations
        board = space*4
        # foundations
        for s in ['S','H','D','C']:
            f = self.foundation[s]
            if f.length == 0:
                board = board + found.format(f.suit.symbol)
            else:
                board = board + f.top_card().draw(cardwidth) + " "
        # freecells
        board = board + "\n"
        for c in self.freecells.cells:
            if c.length == 0:
                board = board + blank
            else:
                board = board + c.top_card().draw(cardwidth) + " "
        # empty space after freecells
        board = board + space*4
        # empty row to avoid confusing freecells with columns
        board = board + "\n" + space*8
        # rows
        for n in range(0, longest_column):
            board = board + "\n"
            for c in self.columns:
                card = c.card_at(n)
                if card:
                    board = board + card.draw(cardwidth) + " "
                else:
                    board = board + space
        return board



if __name__ == '__main__':
    from optparse import OptionParser
    usage = "Usage: %prog [--test]"
    parser = OptionParser(usage=usage)
    parser.add_option('-t', '--test', action='store_true', default=False,
                      help="Run doctests")
    parser.add_option('-w', '--width', default=7, help="Card width")
    options, args = parser.parse_args()

    if options.test:
        import doctest
        doctest.testmod()
    else:
        game = FreecellGame()
        move = None
        print game.draw_board(options.width)
        while move not in ['q','Q','quit','exit']:
            print "> "
            move = raw_input()
            if move in ['n','N','new']:
                game = FreecellGame()
            elif move in ['save','Save']:
                pass
            else:
                try:
                    game.move(move)
                except InvalidColumnCardError, e:
                    print "Error: {}".format(e)
                except InvalidFoundationCardError:
                    print "Can't move that card to foundation"
                except Exception, e:
                    print e
            print game.draw_board(options.width)
