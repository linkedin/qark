" This sub-module provides 'sequence awareness' for blessed."

__author__ = 'Jeff Quast <contact@jeffquast.com>'
__license__ = 'MIT'

__all__ = ['init_sequence_patterns', 'Sequence', 'SequenceTextWrapper']

import functools
import textwrap
import warnings
import math
import re

_BINTERM_UNSUPPORTED = ('kermit', 'avatar')
_BINTERM_UNSUPPORTED_MSG = ('sequence-awareness for terminals emitting '
                            'binary-packed capabilities are not supported.')


def _merge_sequences(inp):
    """Merge a list of input sequence patterns for use in a regular expression.
    Order by lengthyness (full sequence set precedent over subset),
    and exclude any empty (u'') sequences.
    """
    return sorted(list(filter(None, inp)), key=len, reverse=True)


def _build_numeric_capability(term, cap, optional=False,
                              base_num=99, nparams=1):
    """ Build regexp from capabilities having matching numeric
        parameter contained within termcap value: n->(\d+).
    """
    _cap = getattr(term, cap)
    opt = '?' if optional else ''
    if _cap:
        args = (base_num,) * nparams
        cap_re = re.escape(_cap(*args))
        for num in range(base_num-1, base_num+2):
            # search for matching ascii, n-1 through n+2
            if str(num) in cap_re:
                # modify & return n to matching digit expression
                cap_re = cap_re.replace(str(num), r'(\d+)%s' % (opt,))
                return cap_re
        warnings.warn('Unknown parameter in %r (%r, %r)' % (cap, _cap, cap_re))
    return None  # no such capability


def _build_any_numeric_capability(term, cap, num=99, nparams=1):
    """ Build regexp from capabilities having *any* digit parameters
        (substitute matching \d with pattern \d and return).
    """
    _cap = getattr(term, cap)
    if _cap:
        cap_re = re.escape(_cap(*((num,) * nparams)))
        cap_re = re.sub('(\d+)', r'(\d+)', cap_re)
        if r'(\d+)' in cap_re:
            return cap_re
        warnings.warn('Missing numerics in %r, %r' % (cap, cap_re))
    return None  # no such capability


def get_movement_sequence_patterns(term):
    """ Build and return set of regexp for capabilities of ``term`` known
        to cause movement.
    """
    bnc = functools.partial(_build_numeric_capability, term)

    return set([
        # carriage_return
        re.escape(term.cr),
        # column_address: Horizontal position, absolute
        bnc(cap='hpa'),
        # row_address: Vertical position #1 absolute
        bnc(cap='vpa'),
        # cursor_address: Move to row #1 columns #2
        bnc(cap='cup', nparams=2),
        # cursor_down: Down one line
        re.escape(term.cud1),
        # cursor_home: Home cursor (if no cup)
        re.escape(term.home),
        # cursor_left: Move left one space
        re.escape(term.cub1),
        # cursor_right: Non-destructive space (move right one space)
        re.escape(term.cuf1),
        # cursor_up: Up one line
        re.escape(term.cuu1),
        # param_down_cursor: Down #1 lines
        bnc(cap='cud', optional=True),
        # restore_cursor: Restore cursor to position of last save_cursor
        re.escape(term.rc),
        # clear_screen: clear screen and home cursor
        re.escape(term.clear),
        # cursor_up: Up one line
        re.escape(term.enter_fullscreen),
        re.escape(term.exit_fullscreen),
        # forward cursor
        term._cuf,
        # backward cursor
        term._cub,
    ])


def get_wontmove_sequence_patterns(term):
    """ Build and return set of regexp for capabilities of ``term`` known
        not to cause any movement.
    """
    bnc = functools.partial(_build_numeric_capability, term)
    bna = functools.partial(_build_any_numeric_capability, term)

    return list([
        # print_screen: Print contents of screen
        re.escape(term.mc0),
        # prtr_off: Turn off printer
        re.escape(term.mc4),
        # prtr_on: Turn on printer
        re.escape(term.mc5),
        # save_cursor: Save current cursor position (P)
        re.escape(term.sc),
        # set_tab: Set a tab in every row, current columns
        re.escape(term.hts),
        # enter_bold_mode: Turn on bold (extra bright) mode
        re.escape(term.bold),
        # enter_standout_mode
        re.escape(term.standout),
        # enter_subscript_mode
        re.escape(term.subscript),
        # enter_superscript_mode
        re.escape(term.superscript),
        # enter_underline_mode: Begin underline mode
        re.escape(term.underline),
        # enter_blink_mode: Turn on blinking
        re.escape(term.blink),
        # enter_dim_mode: Turn on half-bright mode
        re.escape(term.dim),
        # cursor_invisible: Make cursor invisible
        re.escape(term.civis),
        # cursor_visible: Make cursor very visible
        re.escape(term.cvvis),
        # cursor_normal: Make cursor appear normal (undo civis/cvvis)
        re.escape(term.cnorm),
        # clear_all_tabs: Clear all tab stops
        re.escape(term.tbc),
        # change_scroll_region: Change region to line #1 to line #2
        bnc(cap='csr', nparams=2),
        # clr_bol: Clear to beginning of line
        re.escape(term.el1),
        # clr_eol: Clear to end of line
        re.escape(term.el),
        # clr_eos: Clear to end of screen
        re.escape(term.clear_eos),
        # delete_character: Delete character
        re.escape(term.dch1),
        # delete_line: Delete line (P*)
        re.escape(term.dl1),
        # erase_chars: Erase #1 characters
        bnc(cap='ech'),
        # insert_line: Insert line (P*)
        re.escape(term.il1),
        # parm_dch: Delete #1 characters
        bnc(cap='dch'),
        # parm_delete_line: Delete #1 lines
        bnc(cap='dl'),
        # exit_alt_charset_mode: End alternate character set (P)
        re.escape(term.rmacs),
        # exit_am_mode: Turn off automatic margins
        re.escape(term.rmam),
        # exit_attribute_mode: Turn off all attributes
        re.escape(term.sgr0),
        # exit_ca_mode: Strings to end programs using cup
        re.escape(term.rmcup),
        # exit_insert_mode: Exit insert mode
        re.escape(term.rmir),
        # exit_standout_mode: Exit standout mode
        re.escape(term.rmso),
        # exit_underline_mode: Exit underline mode
        re.escape(term.rmul),
        # flash_hook: Flash switch hook
        re.escape(term.hook),
        # flash_screen: Visible bell (may not move cursor)
        re.escape(term.flash),
        # keypad_local: Leave 'keyboard_transmit' mode
        re.escape(term.rmkx),
        # keypad_xmit: Enter 'keyboard_transmit' mode
        re.escape(term.smkx),
        # meta_off: Turn off meta mode
        re.escape(term.rmm),
        # meta_on: Turn on meta mode (8th-bit on)
        re.escape(term.smm),
        # orig_pair: Set default pair to its original value
        re.escape(term.op),
        # parm_ich: Insert #1 characters
        bnc(cap='ich'),
        # parm_index: Scroll forward #1
        bnc(cap='indn'),
        # parm_insert_line: Insert #1 lines
        bnc(cap='il'),
        # erase_chars: Erase #1 characters
        bnc(cap='ech'),
        # parm_rindex: Scroll back #1 lines
        bnc(cap='rin'),
        # parm_up_cursor: Up #1 lines
        bnc(cap='cuu'),
        # scroll_forward: Scroll text up (P)
        re.escape(term.ind),
        # scroll_reverse: Scroll text down (P)
        re.escape(term.rev),
        # tab: Tab to next 8-space hardware tab stop
        re.escape(term.ht),
        # set_a_background: Set background color to #1, using ANSI escape
        bna(cap='setab', num=1),
        bna(cap='setab', num=(term.number_of_colors - 1)),
        # set_a_foreground: Set foreground color to #1, using ANSI escape
        bna(cap='setaf', num=1),
        bna(cap='setaf', num=(term.number_of_colors - 1)),
    ] + [
        # set_attributes: Define video attributes #1-#9 (PG9)
        # ( not *exactly* legal, being extra forgiving. )
        bna(cap='sgr', nparams=_num) for _num in range(1, 10)
        # reset_{1,2,3}string: Reset string
    ] + map(re.escape, (term.r1, term.r2, term.r3,)))


def init_sequence_patterns(term):
    """Given a Terminal instance, ``term``, this function processes
    and parses several known terminal capabilities, and builds and
    returns a dictionary database of regular expressions, which may
    be re-attached to the terminal by attributes of the same key-name:

    ``_re_will_move``
      any sequence matching this pattern will cause the terminal
      cursor to move (such as *term.home*).

    ``_re_wont_move``
      any sequence matching this pattern will not cause the cursor
      to move (such as *term.bold*).

    ``_re_cuf``
      regular expression that matches term.cuf(N) (move N characters forward),
      or None if temrinal is without cuf sequence.

    ``_cuf1``
      *term.cuf1* sequence (cursor forward 1 character) as a static value.

    ``_re_cub``
      regular expression that matches term.cub(N) (move N characters backward),
      or None if terminal is without cub sequence.

    ``_cub1``
      *term.cuf1* sequence (cursor backward 1 character) as a static value.

    These attributes make it possible to perform introspection on strings
    containing sequences generated by this terminal, to determine the
    printable length of a string.
    """
    if term._kind in _BINTERM_UNSUPPORTED:
        warnings.warn(_BINTERM_UNSUPPORTED_MSG)

    # Build will_move, a list of terminal capabilities that have
    # indeterminate effects on the terminal cursor position.
    _will_move = _merge_sequences(get_movement_sequence_patterns(term)
                                  ) if term.does_styling else set()

    # Build wont_move, a list of terminal capabilities that mainly affect
    # video attributes, for use with measure_length().
    _wont_move = _merge_sequences(get_wontmove_sequence_patterns(term)
                                  ) if term.does_styling else set()

    # compile as regular expressions, OR'd.
    _re_will_move = re.compile('(%s)' % ('|'.join(_will_move)))
    _re_wont_move = re.compile('(%s)' % ('|'.join(_wont_move)))

    #
    # static pattern matching for horizontal_distance(ucs, term)
    #
    bnc = functools.partial(_build_numeric_capability, term)

    # parm_right_cursor: Move #1 characters to the right
    _cuf = bnc(cap='cuf', optional=True)
    _re_cuf = re.compile(_cuf) if _cuf else None

    # cursor_right: Non-destructive space (move right one space)
    _cuf1 = term.cuf1

    # parm_left_cursor: Move #1 characters to the left
    _cub = bnc(cap='cub', optional=True)
    _re_cub = re.compile(_cub) if _cub else None

    # cursor_left: Move left one space
    _cub1 = term.cub1

    return {'_re_will_move': _re_will_move,
            '_re_wont_move': _re_wont_move,
            '_re_cuf': _re_cuf,
            '_re_cub': _re_cub,
            '_cuf1': _cuf1,
            '_cub1': _cub1, }

# TODO(jquast): for some reason, 'screen' does not offer hpa and vpa,
#               although they function perfectly fine ! We need some kind
#               of patching function we may apply for such terminals ..
#
#    if term._kind == 'screen' and term.hpa == u'':
#        def screen_hpa(*args):
#            return u'\x1b[{}G'.format(len(args) and args[0] + 1 or 1)
#        term.hpa = screen_hpa
#    if term._kind == 'screen' and term.vpa == u'':
#        def screen_vpa(*args):
#            return u'\x1b[{}d'.format(len(args) and args[0] + 1 or 1)
#        term.vpa = screen_vpa


class SequenceTextWrapper(textwrap.TextWrapper):
    def __init__(self, width, term, **kwargs):
        self.term = term
        assert kwargs.get('break_long_words', False) is False, (
            'break_long_words is not sequence-safe')
        kwargs['break_long_words'] = False
        textwrap.TextWrapper.__init__(self, width, **kwargs)

    def _wrap_chunks(self, chunks):
        """
        escape-sequence aware varient of _wrap_chunks. Though
        movement sequences, such as term.left() are certainly not
        honored, sequences such as term.bold() are, and are not
        broken mid-sequence.
        """
        lines = []
        if self.width <= 0 or not isinstance(self.width, int):
            raise ValueError("invalid width %r(%s) (must be integer > 0)" % (
                self.width, type(self.width)))
        term = self.term
        drop_whitespace = not hasattr(self, 'drop_whitespace'
                                      ) or self.drop_whitespace
        chunks.reverse()
        while chunks:
            cur_line = []
            cur_len = 0
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - len(indent)
            if drop_whitespace and (
                    Sequence(chunks[-1], term).strip() == '' and lines):
                del chunks[-1]
            while chunks:
                chunk_len = Sequence(chunks[-1], term).length()
                if cur_len + chunk_len <= width:
                    cur_line.append(chunks.pop())
                    cur_len += chunk_len
                else:
                    break
            if chunks and Sequence(chunks[-1], term).length() > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
            if drop_whitespace and (
                    cur_line and Sequence(cur_line[-1], term).strip() == ''):
                del cur_line[-1]
            if cur_line:
                lines.append(indent + u''.join(cur_line))
        return lines

SequenceTextWrapper.__doc__ = textwrap.TextWrapper.__doc__


class Sequence(unicode):
    """
    This unicode-derived class understands the effect of escape sequences
    of printable length, allowing a properly implemented .rjust(), .ljust(),
    .center(), and .len()
    """

    def __new__(cls, sequence_text, term):
        """Sequence(sequence_text, term) -> unicode object

        :arg sequence_text: A string containing sequences.
        :arg term: Terminal instance this string was created with.
        """
        new = unicode.__new__(cls, sequence_text)
        new._term = term
        return new

    def ljust(self, width, fillchar=u' '):
        """S.ljust(width, fillchar) -> unicode

        Returns string derived from unicode string ``S``, left-adjusted
        by trailing whitespace padding ``fillchar``."""
        rightside = fillchar * int((max(0.0, float(width - self.length())))
                                   / float(len(fillchar)))
        return u''.join((self, rightside))

    def rjust(self, width, fillchar=u' '):
        """S.rjust(width, fillchar=u'') -> unicode

        Returns string derived from unicode string ``S``, right-adjusted
        by leading whitespace padding ``fillchar``."""
        leftside = fillchar * int((max(0.0, float(width - self.length())))
                                  / float(len(fillchar)))
        return u''.join((leftside, self))

    def center(self, width, fillchar=u' '):
        """S.center(width, fillchar=u'') -> unicode

        Returns string derived from unicode string ``S``, centered
        and surrounded with whitespace padding ``fillchar``."""
        split = max(0.0, float(width) - self.length()) / 2
        leftside = fillchar * int((max(0.0, math.floor(split)))
                                  / float(len(fillchar)))
        rightside = fillchar * int((max(0.0, math.ceil(split)))
                                   / float(len(fillchar)))
        return u''.join((leftside, self, rightside))

    def length(self):
        """S.length() -> int

        Returns printable length of unicode string ``S`` that may contain
        terminal sequences.

        Although accounted for, strings containing sequences such as
        ``term.clear`` will not give accurate returns, it is considered
        un-lengthy (length of 0).

        Strings containing ``term.left`` or ``\b`` will cause "overstrike",
        but a length less than 0 is not ever returned. So ``_\b+`` is a
        length of 1 (``+``), but ``\b`` is simply a length of 0.
        """
        # TODO(jquast): Should we implement the terminal printable
        # width of 'East Asian Fullwidth' and 'East Asian Wide' characters,
        # which can take 2 cells, see http://www.unicode.org/reports/tr11/
        # and http://www.gossamer-threads.com/lists/python/bugs/972834
        return len(self.strip_seqs())

    def strip(self):
        """S.strip() -> unicode

        Returns string derived from unicode string ``S``, stripped of
        whitespace and terminal sequences.
        """
        return self.strip_seqs().strip()

    def strip_seqs(self):
        """S.strip_seqs() -> unicode

        Return a string without sequences for a string that contains
        (most types) of (escape) sequences for the Terminal with which
        they were created.
        """
        # nxt: points to first character beyond current escape sequence.
        # width: currently estimated display length.
        outp = u''
        nxt = 0
        for idx in range(0, unicode.__len__(self)):
            # account for width of sequences that contain padding (a sort of
            # SGR-equivalent cheat for the python equivalent of ' '*N, for
            # very large values of N that may xmit fewer bytes than many raw
            # spaces. It should be noted, however, that this is a
            # non-destructive space.
            width = horizontal_distance(self[idx:], self._term)
            if width > 0:
                outp += u' ' * horizontal_distance(self[idx:], self._term)
            elif width < 0:
                # \b causes the previous character to be trimmed
                outp = outp[:width]
            if idx == nxt:
                # point beyond this sequence
                nxt = idx + measure_length(self[idx:], self._term)
            if nxt <= idx:
                outp += self[idx]
                # point beyond next sequence, if any, otherwise next character
                nxt = idx + measure_length(self[idx:], self._term) + 1
        return outp


def measure_length(ucs, term):
    """measure_length(S, term) -> int

    Returns non-zero for string ``S`` that begins with a terminal sequence,
    that is: the width of the first unprintable sequence found in S.  For use
    as a *next* pointer to skip past sequences. If string ``S`` is not a
    sequence, 0 is returned.

    A sequence may be a typical terminal sequence beginning with Escape
    (``\x1b``), especially a Control Sequence Initiator (``CSI``, ``\x1b[``,
    ...), or those of ``\a``, ``\b``, ``\r``, ``\n``, ``\xe0`` (shift in),
    ``\x0f`` (shift out). They do not necessarily have to begin with CSI, they
    need only match the capabilities of attributes ``_re_will_move`` and
    ``_re_wont_move`` of terminal ``term``.
    """

    # simple terminal control characters,
    ctrl_seqs = u'\a\b\r\n\x0e\x0f'

    if any([ucs.startswith(_ch) for _ch in ctrl_seqs]):
        return 1

    # known multibyte sequences,
    matching_seq = term and (
        term._re_will_move.match(ucs) or
        term._re_wont_move.match(ucs) or
        term._re_cub and term._re_cub.match(ucs) or
        term._re_cuf and term._re_cuf.match(ucs)
    )

    if matching_seq:
        start, end = matching_seq.span()
        return end

    # none found, must be printable!
    return 0


def termcap_distance(ucs, cap, unit, term):
    """termcap_distance(S, cap, unit, term) -> int

    Match horizontal distance by simple ``cap`` capability name, ``cub1`` or
    ``cuf1``, with string matching the sequences identified by Terminal
    instance ``term`` and a distance of ``unit`` *1* or *-1*, for right and
    left, respectively.

    Otherwise, by regular expression (using dynamic regular expressions built
    using ``cub(n)`` and ``cuf(n)``. Failing that, any of the standard SGR
    sequences (``\033[C``, ``\033[D``, ``\033[nC``, ``\033[nD``).

    Returns 0 if unmatched.
    """
    assert cap in ('cuf', 'cub')
    # match cub1(left), cuf1(right)
    one = getattr(term, '_%s1' % (cap,))
    if one and ucs.startswith(one):
        return unit

    # match cub(n), cuf(n) using regular expressions
    re_pattern = getattr(term, '_re_%s' % (cap,))
    _dist = re_pattern and re_pattern.match(ucs)
    if _dist:
        return unit * int(_dist.group(1))

    return 0


def horizontal_distance(ucs, term):
    """horizontal_distance(S, term) -> int

    Returns Integer ``<n>`` in SGR sequence of form ``<ESC>[<n>C``
    (T.move_right(n)),  or ``-(n)`` in sequence of form ``<ESC>[<n>D``
    (T.move_left(n)).  Returns -1 for backspace (0x08), Otherwise 0.

    Tabstop (``\t``) cannot be correctly calculated, as the relative column
    position cannot be determined: 8 is always (and, incorrectly) returned.
    """

    if ucs.startswith('\b'):
        return -1

    elif ucs.startswith('\t'):
        # as best as I can prove it, a tabstop is always 8 by default.
        # Though, given that blessings is:
        #  1. unaware of the output device's current cursor position, and
        #  2. unaware of the location the callee may chose to output any
        #     given string,
        # It is not possible to determine how many cells any particular
        # \t would consume on the output device!
        return 8

    return (termcap_distance(ucs, 'cub', -1, term) or
            termcap_distance(ucs, 'cuf', 1, term) or
            0)
