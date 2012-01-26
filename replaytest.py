#!/usr/bin/env python
# -*- coding: utf-8 -*-

from freecell import FreecellGame

replay = u'lhaszzjgjgjgjfjgjhrjwjfj;j;l;d;gq;afagfazzzzzzzzq;lglgldlhzzzzzzzzkgfgkfqkaszzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwjfjas;g;l;d;gq;zzzz'
game = FreecellGame(u'7S,5D,QH,JC,5C,AS,5S,8S,QD,9H,KS,7C,2D,3S,JH,8H,QC,10H,2S,KC,4C,3H,6D,9C,KD,8C,5H,8D,QS,AC,6C,6H,JD,JS,4H,10D,9D,10C,10S,9S,AD,KH,4S,7H,7D,6S,3C,AH,2H,4D,3D,2C')
game.move(replay)
board = game.draw_board()

board_should_be = '                            \x1b[4;30;107m   A\xe2\x99\xa0 \x1b[m \xe2\x99\xa1_____ \xe2\x99\xa2_____ \xe2\x99\xa3_____ \n  q      w      e      r      u      i      o      p    \n\x1b[4;30;107m   8\xe2\x99\xa0 \x1b[m \x1b[4;30;107m   5\xe2\x99\xa3 \x1b[m ______ ______                             \n                                                        \n\x1b[4;30;107m   2\xe2\x99\xa3 \x1b[m \x1b[4;31;107m   3\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   4\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   2\xe2\x99\xa5 \x1b[m \x1b[4;31;107m   A\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   3\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   6\xe2\x99\xa0 \x1b[m \x1b[4;31;107m   7\xe2\x99\xa6 \x1b[m \n\x1b[4;31;107m   7\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   4\xe2\x99\xa0 \x1b[m \x1b[4;31;107m   K\xe2\x99\xa5 \x1b[m \x1b[4;31;107m   A\xe2\x99\xa6 \x1b[m \x1b[4;30;107m   9\xe2\x99\xa0 \x1b[m \x1b[4;30;107m  10\xe2\x99\xa0 \x1b[m \x1b[4;30;107m  10\xe2\x99\xa3 \x1b[m \x1b[4;31;107m   9\xe2\x99\xa6 \x1b[m \n\x1b[4;31;107m  10\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   4\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   J\xe2\x99\xa0 \x1b[m \x1b[4;31;107m   J\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   6\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   6\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   A\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   Q\xe2\x99\xa0 \x1b[m \n\x1b[4;31;107m   8\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   5\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   8\xe2\x99\xa3 \x1b[m \x1b[4;31;107m   K\xe2\x99\xa6 \x1b[m \x1b[4;30;107m   9\xe2\x99\xa3 \x1b[m \x1b[4;31;107m   6\xe2\x99\xa6 \x1b[m \x1b[4;31;107m   3\xe2\x99\xa5 \x1b[m        \n\x1b[4;30;107m   K\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   2\xe2\x99\xa0 \x1b[m \x1b[4;31;107m  10\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   Q\xe2\x99\xa3 \x1b[m \x1b[4;31;107m   8\xe2\x99\xa5 \x1b[m \x1b[4;31;107m   J\xe2\x99\xa5 \x1b[m \x1b[4;30;107m   3\xe2\x99\xa0 \x1b[m   ;    \n\x1b[4;30;107m   7\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   K\xe2\x99\xa0 \x1b[m \x1b[4;31;107m   9\xe2\x99\xa5 \x1b[m \x1b[4;31;107m   Q\xe2\x99\xa6 \x1b[m \x1b[4;30;107m   7\xe2\x99\xa0 \x1b[m \x1b[4;30;107m   5\xe2\x99\xa0 \x1b[m \x1b[4;31;107m   2\xe2\x99\xa6 \x1b[m        \n       \x1b[4;31;107m   Q\xe2\x99\xa5 \x1b[m \x1b[4;31;107m   5\xe2\x99\xa6 \x1b[m                                    \n  a    \x1b[4;30;107m   J\xe2\x99\xa3 \x1b[m \x1b[4;30;107m   4\xe2\x99\xa3 \x1b[m   f      j      k      l           \n                                                        \n         s      d                                       '

if not board.__repr__() == board_should_be.__repr__():
    print 'NOT EQUAL'
    print 'BOARD SHOULD BE'
    print board_should_be
    print 'BOARD IS'
    print board
