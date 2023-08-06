#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: hufeng.mao@carota.ai
Date: 2022-06-12 21:27:35
LastEditors: hufeng.mao@carota.ai
LastEditTime: 2022-06-17 16:35:57
Description: 
'''

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import (QColor, QTextCharFormat, QFont)

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'error': format('red', 'bold'),
    'success': format('blue', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'numbers': format('brown'),
}

default = QTextCharFormat()

class Highlighter(object):

    def __init__(self, formats=None):
        self.styles = styles = dict(STYLES, **(formats or {}))
        self.rules = [
            # Numeric literals
            (QRegExp(r'\b[+-]?[0-9]+[lL]?\b'), 0, styles['numbers']),
            (QRegExp(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b'), 0, styles['numbers']),
        ]

        self.rules += [
            (QRegExp(r'%s' % w), 0, styles['error']) 
            for w in ['error', 'Exception', 'unable']
        ]
        self.rules += [
            (QRegExp(r'%s' % w), 0, styles['success']) for w in ['success', 'ok', 'done']]
        
        self.progress_regex = QRegExp(r"progress[:=].?(\d+)%")
        self.hide_regex = QRegExp(r"hide.*progress[:=].?(\d+)%")

    def highlight(self, text):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = expression.matchedLength()
                yield (index, length, format)
                index = expression.indexIn(text, index + length)
    
    def progess(self, text):
        show = True
        if self.hide_regex.indexIn(text) >= 0:
            show = False
        expression = self.progress_regex
        nth = 0
        index = self.progress_regex.indexIn(text)
        while index >= 0:
            index = expression.pos(nth)
            length = expression.matchedLength()
            yield int(expression.cap(nth+1)), show
            index = expression.indexIn(text, index + length) 

__version__ = '1.0.0'
__author__ = 'hufeng.mao@carota.ai'

def main():
    hl = Highlighter()
    g = hl.progess("update progress: 87%\n")
    print(list(g))

if __name__ == '__main__':
    main()