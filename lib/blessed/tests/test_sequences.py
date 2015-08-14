# -*- coding: utf-8 -*-
"""Tests for Terminal() sequences and sequence-awareness."""
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import platform
import sys
import os

from accessories import (
    unsupported_sequence_terminals,
    all_standard_terms,
    as_subprocess,
    TestTerminal,
    unicode_parm,
    many_columns,
    unicode_cap,
    many_lines,
)

import pytest
import mock


def test_capability():
    """Check that capability lookup works."""
    @as_subprocess
    def child():
        # Also test that Terminal grabs a reasonable default stream. This test
        # assumes it will be run from a tty.
        t = TestTerminal()
        sc = unicode_cap('sc')
        assert t.save == sc
        assert t.save == sc  # Make sure caching doesn't screw it up.

    child()


def test_capability_without_tty():
    """Assert capability templates are '' when stream is not a tty."""
    @as_subprocess
    def child():
        t = TestTerminal(stream=StringIO())
        assert t.save == u''
        assert t.red == u''

    child()


def test_capability_with_forced_tty():
    """force styling should return sequences even for non-ttys."""
    @as_subprocess
    def child():
        t = TestTerminal(stream=StringIO(), force_styling=True)
        assert t.save == unicode_cap('sc')

    child()


def test_parametrization():
    """Test parametrizing a capability."""
    @as_subprocess
    def child():
        assert TestTerminal().cup(3, 4) == unicode_parm('cup', 3, 4)

    child()


def test_height_and_width():
    """Assert that ``height_and_width()`` returns full integers."""
    @as_subprocess
    def child():
        t = TestTerminal()  # kind shouldn't matter.
        assert isinstance(t.height, int)
        assert isinstance(t.width, int)

    child()


def test_stream_attr():
    """Make sure Terminal ``stream`` is stdout by default."""
    @as_subprocess
    def child():
        assert TestTerminal().stream == sys.__stdout__

    child()


@pytest.mark.skipif(os.environ.get('TRAVIS', None) is not None,
                    reason="travis-ci does not have binary-packed terminals.")
def test_emit_warnings_about_binpacked(unsupported_sequence_terminals):
    """Test known binary-packed terminals (kermit, avatar) emit a warning."""
    @as_subprocess
    def child(kind):
        import warnings
        from blessed.sequences import _BINTERM_UNSUPPORTED_MSG
        warnings.filterwarnings("error", category=RuntimeWarning)
        warnings.filterwarnings("error", category=UserWarning)

        try:
            TestTerminal(kind=kind, force_styling=True)
        except UserWarning:
            err = sys.exc_info()[1]
            assert (err.args[0] == _BINTERM_UNSUPPORTED_MSG or
                    err.args[0].startswith('Unknown parameter in ')
                    ), err
        else:
            assert 'warnings should have been emitted.'
        warnings.resetwarnings()

    child(unsupported_sequence_terminals)


def test_unit_binpacked_unittest(unsupported_sequence_terminals):
    """Unit Test known binary-packed terminals emit a warning (travis-safe)."""
    import warnings
    from blessed.sequences import (_BINTERM_UNSUPPORTED_MSG,
                                   init_sequence_patterns)
    warnings.filterwarnings("error", category=UserWarning)
    term = mock.Mock()
    term._kind = unsupported_sequence_terminals

    try:
        init_sequence_patterns(term)
    except UserWarning:
        err = sys.exc_info()[1]
        assert err.args[0] == _BINTERM_UNSUPPORTED_MSG
    else:
        assert False, 'Previous stmt should have raised exception.'
    warnings.resetwarnings()


def test_merge_sequences():
    """Test sequences are filtered and ordered longest-first."""
    from blessed.sequences import _merge_sequences
    input_list = [u'a', u'aa', u'aaa', u'']
    output_expected = [u'aaa', u'aa', u'a']
    assert (_merge_sequences(input_list) == output_expected)


def test_location_with_styling(all_standard_terms):
    """Make sure ``location()`` works on all terminals."""
    @as_subprocess
    def child_with_styling(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        with t.location(3, 4):
            t.stream.write(u'hi')
        expected_output = u''.join(
            (unicode_cap('sc'),
             unicode_parm('cup', 4, 3),
             u'hi', unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    child_with_styling(all_standard_terms)


def test_location_without_styling():
    """Make sure ``location()`` silently passes without styling."""
    @as_subprocess
    def child_without_styling():
        """No side effect for location as a context manager without styling."""
        t = TestTerminal(stream=StringIO(), force_styling=None)

        with t.location(3, 4):
            t.stream.write(u'hi')

        assert t.stream.getvalue() == u'hi'

    child_without_styling()


def test_horizontal_location(all_standard_terms):
    """Make sure we can move the cursor horizontally without changing rows."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        with t.location(x=5):
            pass
        expected_output = u''.join(
            (unicode_cap('sc'),
             unicode_parm('hpa', 5),
             unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    # skip 'screen', hpa is proxied (see later tests)
    if all_standard_terms != 'screen':
        child(all_standard_terms)


def test_vertical_location(all_standard_terms):
    """Make sure we can move the cursor horizontally without changing rows."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        with t.location(y=5):
            pass
        expected_output = u''.join(
            (unicode_cap('sc'),
             unicode_parm('vpa', 5),
             unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    # skip 'screen', vpa is proxied (see later tests)
    if all_standard_terms != 'screen':
        child(all_standard_terms)


def test_inject_move_x_for_screen():
    """Test injection of hpa attribute for screen (issue #55)."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        COL = 5
        with t.location(x=COL):
            pass
        expected_output = u''.join(
            (unicode_cap('sc'),
             u'\x1b[{0}G'.format(COL + 1),
             unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    child('screen')


def test_inject_move_y_for_screen():
    """Test injection of vpa attribute for screen (issue #55)."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        ROW = 5
        with t.location(y=ROW):
            pass
        expected_output = u''.join(
            (unicode_cap('sc'),
             u'\x1b[{0}d'.format(ROW + 1),
             unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    child('screen')


def test_zero_location(all_standard_terms):
    """Make sure ``location()`` pays attention to 0-valued args."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=True)
        with t.location(0, 0):
            pass
        expected_output = u''.join(
            (unicode_cap('sc'),
             unicode_parm('cup', 0, 0),
             unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    child(all_standard_terms)


def test_mnemonic_colors(all_standard_terms):
    """Make sure color shortcuts work."""
    @as_subprocess
    def child(kind):
        def color(t, num):
            return t.number_of_colors and unicode_parm('setaf', num) or ''

        def on_color(t, num):
            return t.number_of_colors and unicode_parm('setab', num) or ''

        # Avoid testing red, blue, yellow, and cyan, since they might someday
        # change depending on terminal type.
        t = TestTerminal(kind=kind)
        assert (t.white == color(t, 7))
        assert (t.green == color(t, 2))  # Make sure it's different than white.
        assert (t.on_black == on_color(t, 0))
        assert (t.on_green == on_color(t, 2))
        assert (t.bright_black == color(t, 8))
        assert (t.bright_green == color(t, 10))
        assert (t.on_bright_black == on_color(t, 8))
        assert (t.on_bright_green == on_color(t, 10))

    child(all_standard_terms)


def test_callable_numeric_colors(all_standard_terms):
    """``color(n)`` should return a formatting wrapper."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        if t.magenta:
            assert t.color(5)('smoo') == t.magenta + 'smoo' + t.normal
        else:
            assert t.color(5)('smoo') == 'smoo'

        if t.on_magenta:
            assert t.on_color(5)('smoo') == t.on_magenta + 'smoo' + t.normal
        else:
            assert t.color(5)(u'smoo') == 'smoo'

        if t.color(4):
            assert t.color(4)(u'smoo') == t.color(4) + u'smoo' + t.normal
        else:
            assert t.color(4)(u'smoo') == 'smoo'

        if t.on_green:
            assert t.on_color(2)('smoo') == t.on_green + u'smoo' + t.normal
        else:
            assert t.on_color(2)('smoo') == 'smoo'

        if t.on_color(6):
            assert t.on_color(6)('smoo') == t.on_color(6) + u'smoo' + t.normal
        else:
            assert t.on_color(6)('smoo') == 'smoo'

    child(all_standard_terms)


def test_null_callable_numeric_colors(all_standard_terms):
    """``color(n)`` should be a no-op on null terminals."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(stream=StringIO(), kind=kind)
        assert (t.color(5)('smoo') == 'smoo')
        assert (t.on_color(6)('smoo') == 'smoo')

    child(all_standard_terms)


def test_naked_color_cap(all_standard_terms):
    """``term.color`` should return a stringlike capability."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        assert (t.color + '' == t.setaf + '')

    child(all_standard_terms)


def test_formatting_functions(all_standard_terms):
    """Test simple and compound formatting wrappers."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        # test simple sugar,
        if t.bold:
            expected_output = u''.join((t.bold, u'hi', t.normal))
        else:
            expected_output = u'hi'
        assert t.bold(u'hi') == expected_output
        # Plain strs for Python 2.x
        if t.green:
            expected_output = u''.join((t.green, 'hi', t.normal))
        else:
            expected_output = u'hi'
        assert t.green('hi') == expected_output
        # Test unicode
        if t.underline:
            expected_output = u''.join((t.underline, u'boö', t.normal))
        else:
            expected_output = u'boö'
        assert (t.underline(u'boö') == expected_output)

        if t.subscript:
            expected_output = u''.join((t.subscript, u'[1]', t.normal))
        else:
            expected_output = u'[1]'

        assert (t.subscript(u'[1]') == expected_output)

    child(all_standard_terms)


def test_compound_formatting(all_standard_terms):
    """Test simple and compound formatting wrappers."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        if any((t.bold, t.green)):
            expected_output = u''.join((t.bold, t.green, u'boö', t.normal))
        else:
            expected_output = u'boö'
        assert t.bold_green(u'boö') == expected_output

        if any((t.on_bright_red, t.bold, t.bright_green, t.underline)):
            expected_output = u''.join(
                (t.on_bright_red, t.bold, t.bright_green, t.underline, u'meh',
                 t.normal))
        else:
            expected_output = u'meh'
        assert (t.on_bright_red_bold_bright_green_underline('meh')
                == expected_output)

    child(all_standard_terms)


def test_formatting_functions_without_tty(all_standard_terms):
    """Test crazy-ass formatting wrappers when there's no tty."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO(), force_styling=False)
        assert (t.bold(u'hi') == u'hi')
        assert (t.green('hi') == u'hi')
        # Test non-ASCII chars, no longer really necessary:
        assert (t.bold_green(u'boö') == u'boö')
        assert (t.bold_underline_green_on_red('loo') == u'loo')
        assert (t.on_bright_red_bold_bright_green_underline('meh') == u'meh')

    child(all_standard_terms)


def test_nice_formatting_errors(all_standard_terms):
    """Make sure you get nice hints if you misspell a formatting wrapper."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind)
        try:
            t.bold_misspelled('hey')
            assert not t.is_a_tty or False, 'Should have thrown exception'
        except TypeError:
            e = sys.exc_info()[1]
            assert 'probably misspelled' in e.args[0]
        try:
            t.bold_misspelled(u'hey')  # unicode
            assert not t.is_a_tty or False, 'Should have thrown exception'
        except TypeError:
            e = sys.exc_info()[1]
            assert 'probably misspelled' in e.args[0]

        try:
            t.bold_misspelled(None)  # an arbitrary non-string
            assert not t.is_a_tty or False, 'Should have thrown exception'
        except TypeError:
            e = sys.exc_info()[1]
            assert 'probably misspelled' not in e.args[0]

        if platform.python_implementation() != 'PyPy':
            # PyPy fails to toss an exception, Why?!
            try:
                t.bold_misspelled('a', 'b')  # >1 string arg
                assert not t.is_a_tty or False, 'Should have thrown exception'
            except TypeError:
                e = sys.exc_info()[1]
                assert 'probably misspelled' in e.args[0], e.args

    child(all_standard_terms)


def test_null_callable_string(all_standard_terms):
    """Make sure NullCallableString tolerates all kinds of args."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(stream=StringIO(), kind=kind)
        assert (t.clear == '')
        assert (t.move(1 == 2) == '')
        assert (t.move_x(1) == '')
        assert (t.bold() == '')
        assert (t.bold('', 'x', 'huh?') == '')
        assert (t.bold('', 9876) == '')
        assert (t.uhh(9876) == '')
        assert (t.clear('x') == 'x')

    child(all_standard_terms)


def test_bnc_parameter_emits_warning():
    """A fake capability without target digits emits a warning."""
    import warnings
    from blessed.sequences import _build_numeric_capability

    # given,
    warnings.filterwarnings("error", category=UserWarning)
    term = mock.Mock()
    fake_cap = lambda *args: u'NO-DIGIT'
    term.fake_cap = fake_cap

    # excersize,
    try:
        _build_numeric_capability(term, 'fake_cap', base_num=1984)
    except UserWarning:
        err = sys.exc_info()[1]
        assert err.args[0].startswith('Unknown parameter in ')
    else:
        assert False, 'Previous stmt should have raised exception.'
    warnings.resetwarnings()


def test_bna_parameter_emits_warning():
    """A fake capability without any digits emits a warning."""
    import warnings
    from blessed.sequences import _build_any_numeric_capability

    # given,
    warnings.filterwarnings("error", category=UserWarning)
    term = mock.Mock()
    fake_cap = lambda *args: 'NO-DIGIT'
    term.fake_cap = fake_cap

    # excersize,
    try:
        _build_any_numeric_capability(term, 'fake_cap')
    except UserWarning:
        err = sys.exc_info()[1]
        assert err.args[0].startswith('Missing numerics in ')
    else:
        assert False, 'Previous stmt should have raised exception.'
    warnings.resetwarnings()
