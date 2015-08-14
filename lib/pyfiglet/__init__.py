#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
Python FIGlet adaption
"""

from __future__ import print_function, unicode_literals

import pkg_resources
import re
import sys
from optparse import OptionParser

from .version import __version__

__author__ = 'Peter Waller <peter.waller@gmail.com>'
__copyright__ = """
Copyright (C) 2007 Christopher Jones <cjones@gruntle.org>
Tweaks (C) 2011 Peter Waller <peter.waller@gmail.com>
       (C) 2011 Stefano Rivera <stefano@rivera.za.net>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""


DEFAULT_FONT = 'standard'


def figlet_format(text, font=DEFAULT_FONT, **kwargs):
    fig = Figlet(font, **kwargs)
    return fig.renderText(text)


def print_figlet(text, font=DEFAULT_FONT, **kwargs):
    print(figlet_format(text, font, **kwargs))


class FigletError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

class CharNotPrinted(FigletError):
    """
    Raised when the width is not sufficient to print a character
    """

class FontNotFound(FigletError):
    """
    Raised when a font can't be located
    """


class FontError(FigletError):
    """
    Raised when there is a problem parsing a font file
    """


class FigletFont(object):
    """
    This class represents the currently loaded font, including
    meta-data about how it should be displayed by default
    """

    reMagicNumber = re.compile(r'^[tf]lf2.')
    reEndMarker = re.compile(r'(.)\s*$')

    def __init__(self, font=DEFAULT_FONT):
        self.font = font

        self.comment = ''
        self.chars = {}
        self.width = {}
        self.data = self.preloadFont(font)
        self.loadFont()

    @classmethod
    def preloadFont(cls, font):
        """
        Load font data if exist
        """
        for extension in ('tlf', 'flf'):
            fn = '%s.%s' % (font, extension)
            if pkg_resources.resource_exists('pyfiglet.fonts', fn):
                data = pkg_resources.resource_string('pyfiglet.fonts', fn)
                data = data.decode('UTF-8', 'replace')
                return data
        else:
            raise FontNotFound(font)

    @classmethod
    def isValidFont(cls, font):
        if not font.endswith(('.flf', '.tlf')):
            return False
        f = pkg_resources.resource_stream('pyfiglet.fonts', font)
        header = f.readline().decode('UTF-8', 'replace')
        f.close()
        return cls.reMagicNumber.search(header)

    @classmethod
    def getFonts(cls):
        return [font.rsplit('.', 2)[0] for font
                in pkg_resources.resource_listdir('pyfiglet', 'fonts')
                if cls.isValidFont(font)]

    @classmethod
    def infoFont(cls, font, short=False):
        """
        Get informations of font
        """
        data = FigletFont.preloadFont(font)
        infos = []
        reStartMarker = re.compile(r"""
            ^(FONT|COMMENT|FONTNAME_REGISTRY|FAMILY_NAME|FOUNDRY|WEIGHT_NAME|
              SETWIDTH_NAME|SLANT|ADD_STYLE_NAME|PIXEL_SIZE|POINT_SIZE|
              RESOLUTION_X|RESOLUTION_Y|SPACING|AVERAGE_WIDTH|COMMENT|
              FONT_DESCENT|FONT_ASCENT|CAP_HEIGHT|X_HEIGHT|FACE_NAME|FULL_NAME|
              COPYRIGHT|_DEC_|DEFAULT_CHAR|NOTICE|RELATIVE_).*""", re.VERBOSE)
        reEndMarker = re.compile(r'^.*[@#$]$')
        for line in data.splitlines()[0:100]:
            if (cls.reMagicNumber.search(line) is None
                    and reStartMarker.search(line) is None
                    and reEndMarker.search(line) is None):
                infos.append(line)
        return '\n'.join(infos) if not short else infos[0]

    def loadFont(self):
        """
        Parse loaded font data for the rendering engine to consume
        """
        try:
            # Parse first line of file, the header
            data = self.data.splitlines()

            header = data.pop(0)
            if self.reMagicNumber.search(header) is None:
                raise FontError('%s is not a valid figlet font' % self.font)

            header = self.reMagicNumber.sub('', header)
            header = header.split()

            if len(header) < 6:
                raise FontError('malformed header for %s' % self.font)

            hardBlank = header[0]
            height, baseLine, maxLength, oldLayout, commentLines = map(
                int, header[1:6])
            printDirection = fullLayout = None

            # these are all optional for backwards compat
            if len(header) > 6:
                printDirection = int(header[6])
            if len(header) > 7:
                fullLayout = int(header[7])

            # if the new layout style isn't available,
            # convert old layout style. backwards compatability
            if fullLayout is None:
                if oldLayout == 0:
                    fullLayout = 64
                elif oldLayout < 0:
                    fullLayout = 0
                else:
                    fullLayout = (oldLayout & 31) | 128

            # Some header information is stored for later, the rendering
            # engine needs to know this stuff.
            self.height = height
            self.hardBlank = hardBlank
            self.printDirection = printDirection
            self.smushMode = fullLayout

            # Strip out comment lines
            for i in range(0, commentLines):
                self.comment += data.pop(0)

            def __char(data):
                """
                Function loads one character in the internal array from font
                file content
                """
                end = None
                width = 0
                chars = []
                for j in range(0, height):
                    line = data.pop(0)
                    if end is None:
                        end = self.reEndMarker.search(line).group(1)
                        end = re.compile(re.escape(end) + r'{1,2}$')

                    line = end.sub('', line)

                    if len(line) > width:
                        width = len(line)
                    chars.append(line)
                return width, chars

            # Load ASCII standard character set (32 - 127)
            for i in range(32, 127):
                width, letter = __char(data)
                if ''.join(letter) != '':
                    self.chars[i] = letter
                    self.width[i] = width

            # Load ASCII extended character set
            while data:
                line = data.pop(0).strip()
                i = line.split(' ', 1)[0]
                if (i == ''):
                    continue
                hex_match = re.search('^0x', i, re.IGNORECASE)
                if hex_match is not None:
                    i = int(i, 16)
                    width, letter = __char(data)
                    if ''.join(letter) != '':
                        self.chars[i] = letter
                        self.width[i] = width

        except Exception as e:
            raise FontError('problem parsing %s font: %s' % (self.font, e))

    def __str__(self):
        return '<FigletFont object: %s>' % self.font


unicode_string = type(''.encode('ascii').decode('ascii'))


class FigletString(unicode_string):
    """
    Rendered figlet font
    """

    # translation map for reversing ascii art / -> \, etc.
    __reverse_map__ = (
        '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
        '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        ' !"#$%&\')(*+,-.\\'
        '0123456789:;>=<?'
        '@ABCDEFGHIJKLMNO'
        'PQRSTUVWXYZ]/[^_'
        '`abcdefghijklmno'
        'pqrstuvwxyz}|{~\x7f'
        '\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
        '\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
        '\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
        '\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
        '\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
        '\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
        '\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
        '\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')

    # translation map for flipping ascii art ^ -> v, etc.
    __flip_map__ = (
        '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
        '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        ' !"#$%&\'()*+,-.\\'
        '0123456789:;<=>?'
        '@VBCDEFGHIJKLWNO'
        'bQbSTUAMXYZ[/]v-'
        '`aPcdefghijklwno'
        'pqrstu^mxyz{|}~\x7f'
        '\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
        '\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
        '\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
        '\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
        '\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
        '\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
        '\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
        '\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')

    def reverse(self):
        out = []
        for row in self.splitlines():
            out.append(row.translate(self.__reverse_map__)[::-1])

        return self.newFromList(out)

    def flip(self):
        out = []
        for row in self.splitlines()[::-1]:
            out.append(row.translate(self.__flip_map__))

        return self.newFromList(out)

    def newFromList(self, list):
        return FigletString('\n'.join(list) + '\n')


class FigletRenderingEngine(object):
    """
    This class handles the rendering of a FigletFont,
    including smushing/kerning/justification/direction
    """

    def __init__(self, base=None):
        self.base = base

    def render(self, text):
        """
        Render an ASCII text string in figlet
        """
        builder = FigletBuilder(text,
                                self.base.Font,
                                self.base.direction,
                                self.base.width,
                                self.base.justify)

        while builder.isNotFinished():
            builder.addCharToProduct()
            builder.goToNextChar()

        return builder.returnProduct()

class FigletProduct(object):
    """
    This class stores the internal build part of
    the ascii output string
    """
    def __init__(self):
        self.queue = list()
        self.buffer_string = ""

    def append(self, buffer):
        self.queue.append(buffer)

    def getString(self):
        return FigletString(self.buffer_string)


class FigletBuilder(object):
    """
    Represent the internals of the build process
    """
    def __init__(self, text, font, direction, width, justify):

        self.text = list(map(ord, list(text)))
        self.direction = direction
        self.width = width
        self.font = font
        self.justify = justify

        self.iterator = 0
        self.maxSmush = 0
        self.newBlankRegistered = False

        self.curCharWidth = 0
        self.prevCharWidth = 0
        self.currentTotalWidth = 0

        self.blankMarkers = list()
        self.product = FigletProduct()
        self.buffer = ['' for i in range(self.font.height)]

        # constants.. lifted from figlet222
        self.SM_EQUAL = 1    # smush equal chars (not hardblanks)
        self.SM_LOWLINE = 2    # smush _ with any char in hierarchy
        self.SM_HIERARCHY = 4    # hierarchy: |, /\, [], {}, (), <>
        self.SM_PAIR = 8    # hierarchy: [ + ] -> |, { + } -> |, ( + ) -> |
        self.SM_BIGX = 16    # / + \ -> X, > + < -> X
        self.SM_HARDBLANK = 32    # hardblank + hardblank -> hardblank
        self.SM_KERN = 64
        self.SM_SMUSH = 128

    # builder interface

    def addCharToProduct(self):
        curChar = self.getCurChar()

        # if the character is a newline, we flush the buffer
        if self.text[self.iterator] == ord("\n"):
                self.blankMarkers.append(([row for row in self.buffer], self.iterator))
                self.handleNewLine()
                return None

        if curChar is None:
            return
        if self.width < self.getCurWidth():
            raise CharNotPrinted("Width is not enough to print this character")
        self.curCharWidth = self.getCurWidth()
        self.maxSmush = self.currentSmushAmount(curChar)

        self.currentTotalWidth = len(self.buffer[0]) + self.curCharWidth - self.maxSmush

        if self.text[self.iterator] == ord(' '):
            self.blankMarkers.append(([row for row in self.buffer], self.iterator))

        if self.text[self.iterator] == ord('\n'):
            self.blankMarkers.append(([row for row in self.buffer], self.iterator))
            self.handleNewLine()

        if (self.currentTotalWidth >= self.width):
            self.handleNewLine()
        else:
            for row in range(0, self.font.height):
                self.addCurCharRowToBufferRow(curChar, row)


        self.prevCharWidth = self.curCharWidth

    def goToNextChar(self):
        self.iterator += 1

    def returnProduct(self):
        """
        Returns the output string created by formatProduct
        """
        if self.buffer[0] != '':
            self.flushLastBuffer()
        self.formatProduct()
        return self.product.getString()

    def isNotFinished(self):
        ret = self.iterator < len(self.text)
        return ret

    # private

    def flushLastBuffer(self):
        self.product.append(self.buffer)

    def formatProduct(self):
        """
        This create the output string representation from
        the internal representation of the product
        """
        string_acc = ''
        for buffer in self.product.queue:
            buffer = self.justifyString(self.justify, buffer)
            string_acc += self.replaceHardblanks(buffer)
        self.product.buffer_string = string_acc

    def getCharAt(self, i):
        if i < 0 or i >= len(list(self.text)):
            return None
        c = self.text[i]

        if c not in self.font.chars:
            return None
        else:
            return self.font.chars[c]

    def getCharWidthAt(self, i):
        if i < 0 or i >= len(self.text):
            return None
        c = self.text[i]
        if c not in self.font.chars:
            return None
        else:
            return self.font.width[c]

    def getCurChar(self):
        return self.getCharAt(self.iterator)

    def getCurWidth(self):
        return self.getCharWidthAt(self.iterator)

    def getLeftSmushedChar(self, i, addLeft):
        idx = len(addLeft) - self.maxSmush + i
        if idx >= 0 and idx < len(addLeft):
            left = addLeft[idx]
        else:
            left = ''
        return left, idx

    def currentSmushAmount(self, curChar):
        return self.smushAmount(self.buffer, curChar)

    def updateSmushedCharInLeftBuffer(self, addLeft, idx, smushed):
        l = list(addLeft)
        if idx < 0 or idx > len(l):
            return addLeft
        l[idx] = smushed
        addLeft = ''.join(l)
        return addLeft

    def smushRow(self, curChar, row):
        addLeft = self.buffer[row]
        addRight = curChar[row]

        if self.direction == 'right-to-left':
            addLeft, addRight = addRight, addLeft

        for i in range(0, self.maxSmush):
            left, idx = self.getLeftSmushedChar(i, addLeft)
            right = addRight[i]
            smushed = self.smushChars(left=left, right=right)
            addLeft = self.updateSmushedCharInLeftBuffer(addLeft, idx, smushed)
        return addLeft, addRight

    def addCurCharRowToBufferRow(self, curChar, row):
        addLeft, addRight = self.smushRow(curChar, row)
        self.buffer[row] = addLeft + addRight[self.maxSmush:]

    def cutBufferCommon(self):
        self.currentTotalWidth = len(self.buffer[0])
        self.buffer = ['' for i in range(self.font.height)]
        self.blankMarkers = list()
        self.prevCharWidth = 0
        curChar = self.getCurChar()
        if curChar is None:
            return
        self.maxSmush = self.currentSmushAmount(curChar)

    def cutBufferAtLastBlank(self, saved_buffer, saved_iterator):
        self.product.append(saved_buffer)
        self.iterator = saved_iterator
        self.cutBufferCommon()

    def cutBufferAtLastChar(self):
        self.product.append(self.buffer)
        self.iterator -= 1
        self.cutBufferCommon()

    def blankExist(self, last_blank):
        return last_blank != -1

    def getLastBlank(self):
        try:
            saved_buffer, saved_iterator = self.blankMarkers.pop()
        except IndexError:
            return -1,-1
        return (saved_buffer, saved_iterator)

    def handleNewLine(self):
        saved_buffer, saved_iterator = self.getLastBlank()
        if self.blankExist(saved_iterator):
            self.cutBufferAtLastBlank(saved_buffer, saved_iterator)
        else:
            self.cutBufferAtLastChar()

    def justifyString(self, justify, buffer):
        if justify == 'right':
            for row in range(0, self.font.height):
                buffer[row] = (
                        ' ' * (self.width - len(buffer[row]) - 1)
                        ) + buffer[row]
        elif justify == 'center':
            for row in range(0, self.font.height):
                buffer[row] = (
                        ' ' * int((self.width - len(buffer[row])) / 2)
                        ) + buffer[row]
        return buffer

    def replaceHardblanks(self, buffer):
        string = '\n'.join(buffer) + '\n'
        string = string.replace(self.font.hardBlank, ' ')
        return string

    def smushAmount(self, buffer=[], curChar=[]):
        """
        Calculate the amount of smushing we can do between this char and the
        last If this is the first char it will throw a series of exceptions
        which are caught and cause appropriate values to be set for later.

        This differs from C figlet which will just get bogus values from
        memory and then discard them after.
        """
        if (self.font.smushMode & (self.SM_SMUSH | self.SM_KERN)) == 0:
            return 0

        maxSmush = self.curCharWidth
        for row in range(0, self.font.height):
            lineLeft = buffer[row]
            lineRight = curChar[row]
            if self.direction == 'right-to-left':
                lineLeft, lineRight = lineRight, lineLeft

            linebd = len(lineLeft.rstrip()) - 1
            if linebd < 0:
                linebd = 0

            if linebd < len(lineLeft):
                ch1 = lineLeft[linebd]
            else:
                linebd = 0
                ch1 = ''

            charbd = len(lineRight) - len(lineRight.lstrip())
            if charbd < len(lineRight):
                ch2 = lineRight[charbd]
            else:
                charbd = len(lineRight)
                ch2 = ''

            amt = charbd + len(lineLeft) - 1 - linebd

            if ch1 == '' or ch1 == ' ':
                amt += 1
            elif (ch2 != ''
                    and self.smushChars(left=ch1, right=ch2) is not None):
                amt += 1

            if amt < maxSmush:
                maxSmush = amt

        return maxSmush

    def smushChars(self, left='', right=''):
        """
        Given 2 characters which represent the edges rendered figlet
        fonts where they would touch, see if they can be smushed together.
        Returns None if this cannot or should not be done.
        """
        if left.isspace() is True:
            return right
        if right.isspace() is True:
            return left

        # Disallows overlapping if previous or current char has a width of 1 or
        # zero
        if (self.prevCharWidth < 2) or (self.curCharWidth < 2):
            return

        # kerning only
        if (self.font.smushMode & self.SM_SMUSH) == 0:
            return

        # smushing by universal overlapping
        if (self.font.smushMode & 63) == 0:
            # Ensure preference to visiable characters.
            if left == self.font.hardBlank:
                return right
            if right == self.font.hardBlank:
                return left

            # Ensures that the dominant (foreground)
            # fig-character for overlapping is the latter in the
            # user's text, not necessarily the rightmost character.
            if self.direction == 'right-to-left':
                return left
            else:
                return right

        if self.font.smushMode & self.SM_HARDBLANK:
            if (left == self.font.hardBlank
                    and right == self.font.hardBlank):
                return left

        if (left == self.font.hardBlank
                or right == self.font.hardBlank):
            return

        if self.font.smushMode & self.SM_EQUAL:
            if left == right:
                return left

        smushes = ()

        if self.font.smushMode & self.SM_LOWLINE:
            smushes += (('_', r'|/\[]{}()<>'),)

        if self.font.smushMode & self.SM_HIERARCHY:
            smushes += (
                ('|', r'|/\[]{}()<>'),
                (r'\/', '[]{}()<>'),
                ('[]', '{}()<>'),
                ('{}', '()<>'),
                ('()', '<>'),
            )

        for a, b in smushes:
            if left in a and right in b:
                return right
            if right in a and left in b:
                return left

        if self.font.smushMode & self.SM_PAIR:
            for pair in [left+right, right+left]:
                if pair in ['[]', '{}', '()']:
                    return '|'

        if self.font.smushMode & self.SM_BIGX:
            if (left == '/') and (right == '\\'):
                return '|'
            if (right == '/') and (left == '\\'):
                return 'Y'
            if (left == '>') and (right == '<'):
                return 'X'
        return


class Figlet(object):
    """
    Main figlet class.
    """

    def __init__(self, font=DEFAULT_FONT, direction='auto', justify='auto',
                 width=80):
        self.font = font
        self._direction = direction
        self._justify = justify
        self.width = width
        self.setFont()
        self.engine = FigletRenderingEngine(base=self)

    def setFont(self, **kwargs):
        if 'font' in kwargs:
            self.font = kwargs['font']

        self.Font = FigletFont(font=self.font)

    def getDirection(self):
        if self._direction == 'auto':
            direction = self.Font.printDirection
            if direction == 0:
                return 'left-to-right'
            elif direction == 1:
                return 'right-to-left'
            else:
                return 'left-to-right'

        else:
            return self._direction

    direction = property(getDirection)

    def getJustify(self):
        if self._justify == 'auto':
            if self.direction == 'left-to-right':
                return 'left'
            elif self.direction == 'right-to-left':
                return 'right'

        else:
            return self._justify

    justify = property(getJustify)

    def renderText(self, text):
        # wrapper method to engine
        return self.engine.render(text)

    def getFonts(self):
        return self.Font.getFonts()


def main():
    parser = OptionParser(version=__version__,
                          usage='%prog [options] [text..]')
    parser.add_option('-f', '--font', default=DEFAULT_FONT,
                      help='font to render with (default: %default)',
                      metavar='FONT')
    parser.add_option('-D', '--direction', type='choice',
                      choices=('auto', 'left-to-right', 'right-to-left'),
                      default='auto', metavar='DIRECTION',
                      help='set direction text will be formatted in '
                           '(default: %default)')
    parser.add_option('-j', '--justify', type='choice',
                      choices=('auto', 'left', 'center', 'right'),
                      default='auto', metavar='SIDE',
                      help='set justification, defaults to print direction')
    parser.add_option('-w', '--width', type='int', default=80, metavar='COLS',
                      help='set terminal width for wrapping/justification '
                           '(default: %default)')
    parser.add_option('-r', '--reverse', action='store_true', default=False,
                      help='shows mirror image of output text')
    parser.add_option('-F', '--flip', action='store_true', default=False,
                      help='flips rendered output text over')
    parser.add_option('-l', '--list_fonts', action='store_true', default=False,
                      help='show installed fonts list')
    parser.add_option('-i', '--info_font', action='store_true', default=False,
                      help='show font\'s information, use with -f FONT')
    opts, args = parser.parse_args()

    if opts.list_fonts:
        print('\n'.join(sorted(FigletFont.getFonts())))
        exit(0)

    if opts.info_font:
        print(FigletFont.infoFont(opts.font))
        exit(0)

    if len(args) == 0:
        parser.print_help()
        return 1

    args = map(lambda arg: arg.decode(sys.stdout.encoding), args)

    text = ' '.join(args)

    f = Figlet(
        font=opts.font, direction=opts.direction,
        justify=opts.justify, width=opts.width,
    )

    r = f.renderText(text)
    if opts.reverse:
        r = r.reverse()
    if opts.flip:
        r = r.flip()

    if sys.version_info > (3,):
        # Set stdout to binary mode
        sys.stdout = sys.stdout.detach()

    sys.stdout.write((r + '\n').encode('UTF-8'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
