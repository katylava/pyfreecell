#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def color_number(color_string):
    patterns = {
        'def': ('', re.compile('^(no?r?m?a?l?|defa?u?l?t?)$')),
        'blk': ('0', re.compile('^bl?a?c?k$')),
        'red': ('1', re.compile('^re?d?$')),
        'grn': ('2', re.compile('^gr?e?e?n?$')),
        'yel': ('3', re.compile('^ye?l?l?o?w?$')),
        'blu': ('4', re.compile('^bl?u?e?$')),
        'mag': ('5', re.compile('^ma?g?e?n?t?a?$')),
        'cya': ('6', re.compile('^cy?a?n?$')),
        'whi': ('7', re.compile('^wh?i?t?e?$')),
    }

    for c,p in patterns.iteritems():
        if p[1].match(color_string):
            return p[0]

def variant_number(variant_string):
    patterns = {
        'def': ('0', re.compile('^(no?r?m?a?l?|defa?u?l?t?)$')),
        'bol': ('1', re.compile('^bo?l?d?$')),
        'dim': ('2', re.compile('^di?m?$')),
        'und': ('4', re.compile('^un?d?e?r?l?i?n?e?$')),
        'bnk': ('5', re.compile('^(bnk|bk|bli?n?k?)$')),
        'rev': ('7', re.compile('^(r|i)(e|n)?v?e?r?s?')),
    }

    for v,p in patterns.iteritems():
        if p[1].match(variant_string):
            return p[0]

def colorize(text, fg='def', bg='def', var='def', bgalt=False, debug=False):
    tpl = '\033[{color}m{text}\033[m'
    fgc = color_number(fg)
    bgc = color_number(bg)
    vnm = variant_number(var)

    if fgc:
        whole = '{};3{}'.format(vnm, fgc)
    else:
        whole = vnm

    if bgc:
        bgnm = '10' if bgalt else '4'
        whole = '{};{}{}'.format(whole, bgnm, bgc)

    if debug:
        print whole

    return tpl.format(color=whole, text=text)

if __name__ == '__main__':
    from optparse import OptionParser
    usage="Usage: %prog --fg [fg] --bg [bg] --var [var] --bgalt 'text'"
    parser = OptionParser(usage=usage)
    parser.add_option('-f', '--fg', help='foreground color', default='def')
    parser.add_option('-b', '--bg', help='background color', default='def')
    parser.add_option('-v', '--var', help='variant style', default='def')
    parser.add_option('-a', '--bgalt', action='store_true', default=False,
                      help='use bright colors for backgroud')
    parser.add_option('-d', '--debug', action='store_true', default=False,
                      help='show color number used')
    options, args = parser.parse_args()

    if len(args) < 1:
        parser.error("You didn't provide a string of text to colorize")

    print(
        colorize(args[0], fg=options.fg, bg=options.bg, var=options.var,
                 bgalt=options.bgalt, debug=options.debug)
    )

