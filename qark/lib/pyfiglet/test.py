#!/usr/bin/env python

from __future__ import print_function
import os.path
import sys
from optparse import OptionParser
from pyfiglet import Figlet
from subprocess import Popen, PIPE
try:
    from colorama import init
    init(strip=not sys.stdout.isatty())
    from termcolor import cprint
except:
    def cprint(text, color):
        print(text)

__version__ = '0.1'

def fail(text):
    cprint(text, 'red')

def win(text):
    cprint(text, 'green')

def dump(text):
    for line in text.split('\n'):
        print(repr(line))

class Test(object):
    def __init__(self, opts):
        self.opts = opts
        self.ok = 0
        self.fail = 0
        self.failed = []
        self.oked = []
        self.skip = ['runic','pyramid','eftifont']  # known bug..
        self.f = Figlet()

    def outputUsingFigletorToilet(self, text, font, fontpath):
        if os.path.isfile(fontpath + '.flf'):
            cmd = ('figlet', '-d', 'pyfiglet/fonts', '-f', font, text)
        elif os.path.isfile(fontpath + '.tlf'):
            cmd = ('toilet', '-d', 'pyfiglet/fonts', '-f', font, text)
        else:
            raise Exception('Missing font file: '+fontpath)

        p = Popen(cmd, bufsize=4096, stdout=PIPE)
        outputFiglet = p.communicate()[0].decode('utf8')
        return outputFiglet

    def validate_font_output(self, font, outputFiglet, outputPyfiglet):
        if outputPyfiglet == outputFiglet:
            win('[OK] %s' % font)
            self.ok += 1
            self.oked.append(font)
            return

        fail('[FAIL] %s' % font)
        self.fail += 1
        self.failed.append(font)
        self.show_result(outputFiglet, outputPyfiglet, font)

    def show_result(self, outputFiglet, outputPyfiglet, font):
        if self.opts.show is True:
            print('[PYTHON] *** %s\n\n' % font)
            dump(outputPyfiglet)
            print('[FIGLET] *** %s\n\n' % font)
            dump(outputFiglet)
            raw_input()

    def check_font(self, text, font):
        if font in self.skip:
            return
        fontpath = os.path.join('pyfiglet', 'fonts', font)

        self.f.setFont(font=font)

        outputPyfiglet = self.f.renderText(text)
        outputFiglet = self.outputUsingFigletorToilet(text, font, fontpath)

        # Our TLF rendering isn't perfect, yet
        strict = os.path.isfile(fontpath + '.flf')
        if not strict:
            outputPyfiglet = outputPyfiglet.strip('\n')
            outputFiglet = outputFiglet.strip('\n')

        self.validate_font_output(font, outputFiglet, outputPyfiglet)


    def check_text(self, text):
        for font in self.f.getFonts():
            self.check_font(text, font)

    def check_result(self):
        print('OK = %d, FAIL = %d' % (self.ok, self.fail))
        if len(self.failed) > 0:
            print('FAILED = %s' % repr(self.failed))

        return self.failed, self.oked

def banner(text):
    cprint(Figlet().renderText(text), "blue")

def main():
    parser = OptionParser(version=__version__)

    parser.add_option('-s', '--show', action='store_true', default=False,
                      help='pause at each failure and compare output '
                           '(default: %default)')

    opts, args = parser.parse_args()
    test = Test(opts)
    banner("TESTING one word")
    test.check_text("foo")
    banner("TESTING cut at space")
    test.check_text("This is a very long text with many spaces and little words")
    banner("TESTING cut at last char")
    test.check_text("Averylongwordthatwillbecutatsomepoint I hope")
    banner("TESTING explicit new line")
    test.check_text("this text\nuse new line")
    if len(test.check_result()[0]) == 0:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
