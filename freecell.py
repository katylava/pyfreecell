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
            if top.rank.label == 'King':
                return None
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
    10♢, 9♠
    >>> fresh.top_card() == jc
    True
    """

    def top_stack(self, length=None):
        clone = copy.deepcopy(self)
        while not clone.valid() or (length and clone.length > length):
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
        if card:
            temp = self.__class__([card])
            while stack.length > 0 and not temp.allow_stack(stack):
                stack.cards.pop(0)
        return None if stack.length == 0 else stack

    def remove_top_stack(self, length=None):
        bottom_card = self.top_stack(length).bottom_card()
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
    [5♡, , , ]
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
    [5♡, , , 2♡]
    >>> fcs.all_cards()
    [5♡ , None, None, 2♡ ]
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
    >>> game.move('ag')
    True
    >>> game.freecell_count()
    3
    >>> game.move('m')
    True
    >>> game.columns[7].cards = []
    >>> game.freecell_count()
    4
    >>> game.move('q;') # test moving from freecell to empty column
    True
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
        self.history = []
        self.replay = []
        initial_state = {
            'columns': self.deck.deal(8),
            'foundation': {'S':[], 'H':[], 'D':[], 'C':[]},
            'freecells': [],
        }
        self.set_state(initial_state)
        self.add_history()

    def complete(self):
        all_kings = True
        for f in self.foundation.values():
            if not f.rank() or not f.rank().label == 'King':
                all_kings = False
        return all_kings

    def get_state(self):
        return self.__getstate__()

    def __getstate__(self):
        foundation = {}
        for s in self.foundation.keys():
            foundation[s] = self.foundation[s].cards[:]
        return {
            'columns': [c.cards[:] for c in self.columns],
            'foundation': foundation,
            'freecells': self.freecells.all_cards()
        }

    def set_state(self, state):
        self.__setstate__(state)

    def __setstate__(self, state):
        self.columns = []
        self.freecells = Freecells()
        self.foundation = {
            'S': FoundationPile('Spades'),
            'H': FoundationPile('Hearts'),
            'D': FoundationPile('Diamonds'),
            'C': FoundationPile('Clubs'),
        }
        for col in state['columns']:
            self.columns.append(AltDescCardColumn(col))
        for suit in self.foundation.keys():
            self.foundation[suit].cards = state['foundation'][suit]
        for pos, card in enumerate(state['freecells']):
            if card:
                self.freecells.add_card(card, pos)

    def add_history(self):
        self.history.append(self.get_state())

    def undo(self):
        if len(self.history) == 1:
            self.set_state(self.history[0])
        else:
            if self.get_state() == self.history[-1]:
                self.history.pop()
            self.set_state(self.history.pop())

    def top_cards(self):
        return [c.top_card() for c in self.columns]

    def parse_moves(self, moves):
        movelist = []
        if moves in ['z', 'zz']:
            movelist.append(('z','z'))
        elif moves in ['m', 'mm']:
            self.move_all_to_foundation()
        else:
            moves = list(moves)
            while len(moves) >= 2:
                movelist.append((moves.pop(0), moves.pop(0)))
        return movelist

    def move(self, moves):
        movelist = self.parse_moves(moves)

        for fr, to in movelist:
            card = None

            if fr in self.mv_cols:
                move_from = self.columns[self.mv_cols.index(fr)]
            elif fr in self.mv_cells[:-2]: # the last ones are only for moving 'to'
                move_from = self.freecells.cells[self.mv_cells.index(fr)]
                card = move_from.top_card()
            elif fr in self.mv_found[:-2]: # the last ones are only for moving 'to' 'y', is only for moving to
                key = self.mv_found_order[self.mv_found.index(fr)]
                move_from = self.foundation[key]
                card = move_from.top_card()
            elif fr == 'z':
                self.undo()
                self.replay.append('zz')
                return True
            else:
                raise FreecellInvalidMoveError("'{}' is not a move".format(fr))

            if to in self.mv_cols:
                move_to = self.columns[self.mv_cols.index(to)]
            elif to in self.mv_cells:
                if to in 'tg':
                    index = self.freecells.first_open()
                else:
                    index = self.mv_cells.index(to)
                card = move_from.top_card()
                move_to = self.freecells.cells[index]
            elif to in self.mv_found:
                if to in 'yh':
                    key = move_from.top_card().suit.c
                else:
                    key = self.mv_found_order[self.mv_found.index(to)]
                card = move_from.top_card()
                move_to = self.foundation[key]
            else:
                raise FreecellInvalidMoveError("'{}' is not a move".format(to))

            success = False
            if card:
                success = self.move_card(card, move_from, move_to)
            else:
                success = self.move_stack(move_from, move_to)
            if success:
                self.replay.append('{}{}'.format(fr, to))
                self.add_history()
            else:
                self.set_state(self.history[-1])
                return False
        return True

    def move_card(self, card, move_from, move_to):
        try:
            move_to.add_card(card)
        except:
            raise
        else:
            move_from.remove_top_card()
            return True

    def move_stack(self, move_from, move_to):
        onto_card = move_to.top_card()

        if onto_card:
            stack = move_from.top_stack_for(onto_card)
        else:
            length = self.freecell_count()
            if move_to.length > 0:
                length = length + 1
            stack = move_from.top_stack(length)

        if not stack:
            raise FreecellInvalidMoveError(
                "No cards in '{}' for {}".format(move_from, onto_card)
            )

        if stack.length <= self.freecell_count()+1:
            try:
                move_to.add_stack(stack)
            except InvalidColumnStackError:
                raise FreecellInvalidMoveError(
                    "Can't move stack '{}' to {}".format(stack, onto_card)
                )
            else:
                if onto_card:
                    move_from.remove_top_stack_for(onto_card)
                else:
                    move_from.remove_top_stack(length)
                return True
        else:
            raise FreecellInvalidMoveError(
                "Not enough freecells to move stack '{}'".format(stack)
            )

    def move_all_to_foundation(self):
        def recurse():
            next_on_founds = [f.next_card() for f in self.foundation.values()]
            for i, card in enumerate(self.top_cards()):
                if card and card in next_on_founds:
                    self.move('{}y'.format(self.mv_cols[i]))
                    return True
            for i, card in enumerate(self.freecells.all_cards()):
                if card and card in next_on_founds:
                    self.move('{}y'.format(self.mv_cells[i]))
                    return True
        while recurse():
            recurse()

    def freecell_count(self):
        return self.freecells.free() + self.top_cards().count(None)

    def draw_board(self, cardwidth=8, suit_offset=2):
        # the suit symbols take up less than one character, so the offset
        # is how much you have to subtract from the width in spots that
        # do not have a suit character
        if cardwidth - suit_offset < 5:
            cardwidth = 5 + suit_offset

        longest_column = max([c.length for c in self.columns])

        space = " "*((cardwidth - suit_offset)+1)
        blank = "_"*(cardwidth - suit_offset) + " "
        found = "{}" + "_"*(cardwidth - suit_offset - 1) + " "
        movel = "%".center(cardwidth - suit_offset) + " "

        board = ''

        # empty space before foundations
        board = space*4
        # foundations
        for s in ['S','H','D','C']:
            f = self.foundation[s]
            if f.length == 0:
                board = board + found.format(f.suit.symbol)
            else:
                board = board + f.top_card().draw(cardwidth) + " "

        board = board + "\n"

        # free cell move hints
        for l in self.mv_cells[:4]:
            board = board + movel.replace('%',l)
        # foundation move hints
        for l in self.mv_found[:4]:
            board = board + movel.replace('%',l)

        board = board + "\n"

        # freecells
        for c in self.freecells.cells:
            if c.length == 0:
                board = board + blank
            else:
                board = board + c.top_card().draw(cardwidth) + " "
        # empty space after freecells
        board = board + space*4

        board = board + "\n" + space*8

        # rows
        for n in range(0, longest_column+2):
            board = board + "\n"
            for c in self.columns:
                card = c.card_at(n)
                if card:
                    board = board + card.draw(cardwidth) + " "
                elif n == c.length + 1:
                    pos = self.columns.index(c)
                    board = board + movel.replace('%',self.mv_cols[pos])
                else:
                    board = board + space
        return board



if __name__ == '__main__':
    from subprocess import call
    from datetime import datetime
    from optparse import OptionParser
    usage = "Usage: %prog [--test]"
    parser = OptionParser(usage=usage)
    parser.add_option('-t', '--test', action='store_true', default=False,
                      help="Run doctests")
    parser.add_option('-w', '--width', type="int", default=7, help="Card width")
    parser.add_option('-o', '--offset', default=0, type="int",
                      help="If the 10s make the cards different widths"
                           " then try some different numbers here")
    options, args = parser.parse_args()

    if options.test:
        import doctest
        doctest.testmod()
    else:
        start = datetime.now()
        game = FreecellGame()
        move = None
        error = ""
        call(['clear'])
        print game.draw_board(options.width, options.offset)
        while move not in ['q','Q','quit','exit']:
            print error
            print "Your move > ",
            move = raw_input()
            call(['clear'])
            if move in ['n','N','new']:
                start = datetime.now()
                game = FreecellGame()
            elif move in ['save','Save']:
                pass
            elif move.startswith('game.'):
                print eval(move)
            else:
                try:
                    game.move(move)
                except Exception, e:
                    error =  "Error: {}".format(e)
                else:
                    error = ""
            if game.complete():
                finish = datetime.now()
                duration = finish - start
                print "Completed Game! Time: {}, Moves: {}" \
                      .format(duration, len(game.replay))
            else:
                print game.draw_board(options.width, options.offset)
