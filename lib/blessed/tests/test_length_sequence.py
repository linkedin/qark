import itertools
import platform
import termios
import struct
import fcntl
import sys
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from accessories import (
    all_standard_terms,
    as_subprocess,
    TestTerminal,
    many_columns,
    many_lines,
    all_terms,
)

import pytest


def test_sequence_length(all_terms):
    """Ensure T.length(string containing sequence) is correct."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        # Create a list of ascii characters, to be seperated
        # by word, to be zipped up with a cycling list of
        # terminal sequences. Then, compare the length of
        # each, the basic plain_text.__len__ vs. the Terminal
        # method length. They should be equal.
        plain_text = ('The softest things of the world '
                      'Override the hardest things of the world '
                      'That which has no substance '
                      'Enters into that which has no openings')
        if t.bold:
            assert (t.length(t.bold) == 0)
            assert (t.length(t.bold('x')) == 1)
            assert (t.length(t.bold_red) == 0)
            assert (t.length(t.bold_red('x')) == 1)
            assert (t.strip(t.bold) == u'')
            assert (t.strip(t.bold('  x  ')) == u'x')
            assert (t.strip(t.bold_red) == u'')
            assert (t.strip(t.bold_red('  x  ')) == u'x')
            assert (t.strip_seqs(t.bold) == u'')
            assert (t.strip_seqs(t.bold('  x  ')) == u'  x  ')
            assert (t.strip_seqs(t.bold_red) == u'')
            assert (t.strip_seqs(t.bold_red('  x  ')) == u'  x  ')

        if t.underline:
            assert (t.length(t.underline) == 0)
            assert (t.length(t.underline('x')) == 1)
            assert (t.length(t.underline_red) == 0)
            assert (t.length(t.underline_red('x')) == 1)
            assert (t.strip(t.underline) == u'')
            assert (t.strip(t.underline('  x  ')) == u'x')
            assert (t.strip(t.underline_red) == u'')
            assert (t.strip(t.underline_red('  x  ')) == u'x')
            assert (t.strip_seqs(t.underline) == u'')
            assert (t.strip_seqs(t.underline('  x  ')) == u'  x  ')
            assert (t.strip_seqs(t.underline_red) == u'')
            assert (t.strip_seqs(t.underline_red('  x  ')) == u'  x  ')

        if t.reverse:
            assert (t.length(t.reverse) == 0)
            assert (t.length(t.reverse('x')) == 1)
            assert (t.length(t.reverse_red) == 0)
            assert (t.length(t.reverse_red('x')) == 1)
            assert (t.strip(t.reverse) == u'')
            assert (t.strip(t.reverse('  x  ')) == u'x')
            assert (t.strip(t.reverse_red) == u'')
            assert (t.strip(t.reverse_red('  x  ')) == u'x')
            assert (t.strip_seqs(t.reverse) == u'')
            assert (t.strip_seqs(t.reverse('  x  ')) == u'  x  ')
            assert (t.strip_seqs(t.reverse_red) == u'')
            assert (t.strip_seqs(t.reverse_red('  x  ')) == u'  x  ')

        if t.blink:
            assert (t.length(t.blink) == 0)
            assert (t.length(t.blink('x')) == 1)
            assert (t.length(t.blink_red) == 0)
            assert (t.length(t.blink_red('x')) == 1)
            assert (t.strip(t.blink) == u'')
            assert (t.strip(t.blink('  x  ')) == u'x')
            assert (t.strip(t.blink_red) == u'')
            assert (t.strip(t.blink_red('  x  ')) == u'x')
            assert (t.strip_seqs(t.blink) == u'')
            assert (t.strip_seqs(t.blink('  x  ')) == u'  x  ')
            assert (t.strip_seqs(t.blink_red) == u'')
            assert (t.strip_seqs(t.blink_red('  x  ')) == u'  x  ')

        if t.home:
            assert (t.length(t.home) == 0)
            assert (t.strip(t.home) == u'')
        if t.clear_eol:
            assert (t.length(t.clear_eol) == 0)
            assert (t.strip(t.clear_eol) == u'')
        if t.enter_fullscreen:
            assert (t.length(t.enter_fullscreen) == 0)
            assert (t.strip(t.enter_fullscreen) == u'')
        if t.exit_fullscreen:
            assert (t.length(t.exit_fullscreen) == 0)
            assert (t.strip(t.exit_fullscreen) == u'')

        # horizontally, we decide move_down and move_up are 0,
        assert (t.length(t.move_down) == 0)
        assert (t.length(t.move_down(2)) == 0)
        assert (t.length(t.move_up) == 0)
        assert (t.length(t.move_up(2)) == 0)

        # other things aren't so simple, somewhat edge cases,
        # moving backwards and forwards horizontally must be
        # accounted for as a "length", as <x><move right 10><y>
        # will result in a printed column length of 12 (even
        # though columns 2-11 are non-destructive space
        assert (t.length(u'x\b') == 0)
        assert (t.strip(u'x\b') == u'')

        # XXX why are some terminals width of 9 here ??
        assert (t.length(u'\t') in (8, 9))
        assert (t.strip(u'\t') == u'')
        assert (t.length(u'_' + t.move_left) == 0)

        if t.cub:
            assert (t.length((u'_' * 10) + t.cub(10)) == 0)

        assert (t.length(t.move_right) == 1)

        if t.cuf:
            assert (t.length(t.cuf(10)) == 10)

        # vertical spacing is unaccounted as a 'length'
        assert (t.length(t.move_up) == 0)
        assert (t.length(t.cuu(10)) == 0)
        assert (t.length(t.move_down) == 0)
        assert (t.length(t.cud(10)) == 0)

        # this is how manpages perform underlining, this is done
        # with the 'overstrike' capability of teletypes, and aparently
        # less(1), '123' -> '1\b_2\b_3\b_'
        text_wseqs = u''.join(itertools.chain(
            *zip(plain_text, itertools.cycle(['\b_']))))
        assert (t.length(text_wseqs) == len(plain_text))

    child(all_terms)


def test_env_winsize():
    """Test height and width is appropriately queried in a pty."""
    @as_subprocess
    def child():
        # set the pty's virtual window size
        os.environ['COLUMNS'] = '99'
        os.environ['LINES'] = '11'
        t = TestTerminal(stream=StringIO())
        save_init = t._init_descriptor
        save_stdout = sys.__stdout__
        try:
            t._init_descriptor = None
            sys.__stdout__ = None
            winsize = t._height_and_width()
            width = t.width
            height = t.height
        finally:
            t._init_descriptor = save_init
            sys.__stdout__ = save_stdout
        assert winsize.ws_col == width == 99
        assert winsize.ws_row == height == 11

    child()


@pytest.mark.skipif(platform.python_implementation() == 'PyPy',
                    reason='PyPy fails TIOCSWINSZ')
def test_winsize(many_lines, many_columns):
    """Test height and width is appropriately queried in a pty."""
    @as_subprocess
    def child(lines=25, cols=80):
        # set the pty's virtual window size
        val = struct.pack('HHHH', lines, cols, 0, 0)
        fcntl.ioctl(sys.__stdout__.fileno(), termios.TIOCSWINSZ, val)
        t = TestTerminal()
        winsize = t._height_and_width()
        assert t.width == cols
        assert t.height == lines
        assert winsize.ws_col == cols
        assert winsize.ws_row == lines

    child(lines=many_lines, cols=many_columns)


@pytest.mark.skipif(platform.python_implementation() == 'PyPy',
                    reason='PyPy fails TIOCSWINSZ')
def test_Sequence_alignment(all_terms, many_lines):
    """Tests methods related to Sequence class, namely ljust, rjust, center."""
    @as_subprocess
    def child(kind, lines=25, cols=80):
        # set the pty's virtual window size
        val = struct.pack('HHHH', lines, cols, 0, 0)
        fcntl.ioctl(sys.__stdout__.fileno(), termios.TIOCSWINSZ, val)
        t = TestTerminal(kind=kind)

        pony_msg = 'pony express, all aboard, choo, choo!'
        pony_len = len(pony_msg)
        pony_colored = u''.join(
            ['%s%s' % (t.color(n % 7), ch,)
             for n, ch in enumerate(pony_msg)])
        pony_colored += t.normal
        ladjusted = t.ljust(pony_colored)
        radjusted = t.rjust(pony_colored)
        centered = t.center(pony_colored)
        assert (t.length(pony_colored) == pony_len)
        assert (t.length(centered.strip()) == pony_len)
        assert (t.length(centered) == len(pony_msg.center(t.width)))
        assert (t.length(ladjusted.strip()) == pony_len)
        assert (t.length(ladjusted) == len(pony_msg.ljust(t.width)))
        assert (t.length(radjusted.strip()) == pony_len)
        assert (t.length(radjusted) == len(pony_msg.rjust(t.width)))

    child(kind=all_terms, lines=many_lines)


def test_sequence_is_movement_false(all_terms):
    """Test parser about sequences that do not move the cursor."""
    @as_subprocess
    def child_mnemonics_wontmove(kind):
        from blessed.sequences import measure_length
        t = TestTerminal(kind=kind)
        assert (0 == measure_length(u'', t))
        # not even a mbs
        assert (0 == measure_length(u'xyzzy', t))
        # negative numbers, though printable as %d, do not result
        # in movement; just garbage. Also not a valid sequence.
        assert (0 == measure_length(t.cuf(-333), t))
        assert (len(t.clear_eol) == measure_length(t.clear_eol, t))
        # various erases don't *move*
        assert (len(t.clear_bol) == measure_length(t.clear_bol, t))
        assert (len(t.clear_eos) == measure_length(t.clear_eos, t))
        assert (len(t.bold) == measure_length(t.bold, t))
        # various paints don't move
        assert (len(t.red) == measure_length(t.red, t))
        assert (len(t.civis) == measure_length(t.civis, t))
        if t.cvvis:
            assert (len(t.cvvis) == measure_length(t.cvvis, t))
        assert (len(t.underline) == measure_length(t.underline, t))
        assert (len(t.reverse) == measure_length(t.reverse, t))
        for _num in range(t.number_of_colors):
            assert (len(t.color(_num)) == measure_length(t.color(_num), t))
        assert (len(t.normal) == measure_length(t.normal, t))
        assert (len(t.normal_cursor) == measure_length(t.normal_cursor, t))
        assert (len(t.hide_cursor) == measure_length(t.hide_cursor, t))
        assert (len(t.save) == measure_length(t.save, t))
        assert (len(t.italic) == measure_length(t.italic, t))
        assert (len(t.standout) == measure_length(t.standout, t)
                ), (t.standout, t._wont_move)

    child_mnemonics_wontmove(all_terms)


def test_sequence_is_movement_true(all_standard_terms):
    """Test parsers about sequences that move the cursor."""
    @as_subprocess
    def child_mnemonics_willmove(kind):
        from blessed.sequences import measure_length
        t = TestTerminal(kind=kind)
        # movements
        assert (len(t.move(98, 76)) ==
                measure_length(t.move(98, 76), t))
        assert (len(t.move(54)) ==
                measure_length(t.move(54), t))
        assert not t.cud1 or (len(t.cud1) ==
                              measure_length(t.cud1, t))
        assert not t.cub1 or (len(t.cub1) ==
                              measure_length(t.cub1, t))
        assert not t.cuf1 or (len(t.cuf1) ==
                              measure_length(t.cuf1, t))
        assert not t.cuu1 or (len(t.cuu1) ==
                              measure_length(t.cuu1, t))
        assert not t.cub or (len(t.cub(333)) ==
                             measure_length(t.cub(333), t))
        assert not t.cuf or (len(t.cuf(333)) ==
                             measure_length(t.cuf(333), t))
        assert not t.home or (len(t.home) ==
                              measure_length(t.home, t))
        assert not t.restore or (len(t.restore) ==
                                 measure_length(t.restore, t))
        assert not t.clear or (len(t.clear) ==
                               measure_length(t.clear, t))

    child_mnemonics_willmove(all_standard_terms)
