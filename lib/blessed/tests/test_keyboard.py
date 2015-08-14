# -*- coding: utf-8 -*-
"Tests for keyboard support."
import tempfile
import StringIO
import signal
import curses
import time
import math
import tty
import pty
import sys
import os

from accessories import (
    read_until_eof,
    read_until_semaphore,
    SEND_SEMAPHORE,
    RECV_SEMAPHORE,
    as_subprocess,
    TestTerminal,
    SEMAPHORE,
    all_terms,
    echo_off,
    xterms,
)

import mock


def test_kbhit_interrupted():
    "kbhit() should not be interrupted with a signal handler."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None

        # child pauses, writes semaphore and begins awaiting input
        global got_sigwinch
        got_sigwinch = False

        def on_resize(sig, action):
            global got_sigwinch
            got_sigwinch = True

        term = TestTerminal()
        signal.signal(signal.SIGWINCH, on_resize)
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.raw():
            assert term.inkey(timeout=1.05) == u''
        os.write(sys.__stdout__.fileno(), b'complete')
        assert got_sigwinch is True
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        read_until_semaphore(master_fd)
        stime = time.time()
        os.kill(pid, signal.SIGWINCH)
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'complete'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 1.0


def test_kbhit_interrupted_nonetype():
    "kbhit() should also allow interruption with timeout of None."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None

        # child pauses, writes semaphore and begins awaiting input
        global got_sigwinch
        got_sigwinch = False

        def on_resize(sig, action):
            global got_sigwinch
            got_sigwinch = True

        term = TestTerminal()
        signal.signal(signal.SIGWINCH, on_resize)
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.raw():
            term.inkey(timeout=1)
        os.write(sys.__stdout__.fileno(), b'complete')
        assert got_sigwinch is True
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        read_until_semaphore(master_fd)
        stime = time.time()
        time.sleep(0.05)
        os.kill(pid, signal.SIGWINCH)
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'complete'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 1.0


def test_kbhit_interrupted_no_continue():
    "kbhit() may be interrupted when _intr_continue=False."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None

        # child pauses, writes semaphore and begins awaiting input
        global got_sigwinch
        got_sigwinch = False

        def on_resize(sig, action):
            global got_sigwinch
            got_sigwinch = True

        term = TestTerminal()
        signal.signal(signal.SIGWINCH, on_resize)
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.raw():
            term.inkey(timeout=1.05, _intr_continue=False)
        os.write(sys.__stdout__.fileno(), b'complete')
        assert got_sigwinch is True
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        read_until_semaphore(master_fd)
        stime = time.time()
        time.sleep(0.05)
        os.kill(pid, signal.SIGWINCH)
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'complete'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_kbhit_interrupted_nonetype_no_continue():
    "kbhit() may be interrupted when _intr_continue=False with timeout None."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None

        # child pauses, writes semaphore and begins awaiting input
        global got_sigwinch
        got_sigwinch = False

        def on_resize(sig, action):
            global got_sigwinch
            got_sigwinch = True

        term = TestTerminal()
        signal.signal(signal.SIGWINCH, on_resize)
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.raw():
            term.inkey(timeout=None, _intr_continue=False)
        os.write(sys.__stdout__.fileno(), b'complete')
        assert got_sigwinch is True
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        read_until_semaphore(master_fd)
        stime = time.time()
        time.sleep(0.05)
        os.kill(pid, signal.SIGWINCH)
        os.write(master_fd, b'X')
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'complete'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_cbreak_no_kb():
    "cbreak() should not call tty.setcbreak() without keyboard."
    @as_subprocess
    def child():
        with tempfile.NamedTemporaryFile() as stream:
            term = TestTerminal(stream=stream)
            with mock.patch("tty.setcbreak") as mock_setcbreak:
                with term.cbreak():
                    assert not mock_setcbreak.called
    child()


def test_raw_no_kb():
    "raw() should not call tty.setraw() without keyboard."
    @as_subprocess
    def child():
        with tempfile.NamedTemporaryFile() as stream:
            term = TestTerminal(stream=stream)
            with mock.patch("tty.setraw") as mock_setraw:
                with term.raw():
                    assert not mock_setraw.called
    child()


def test_kbhit_no_kb():
    "kbhit() always immediately returns False without a keyboard."
    @as_subprocess
    def child():
        term = TestTerminal(stream=StringIO.StringIO())
        stime = time.time()
        assert term.keyboard_fd is None
        assert term.kbhit(timeout=1.1) is False
        assert (math.floor(time.time() - stime) == 1.0)
    child()


def test_inkey_0s_cbreak_noinput():
    "0-second inkey without input; '' should be returned."
    @as_subprocess
    def child():
        term = TestTerminal()
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=0)
            assert (inp == u'')
            assert (math.floor(time.time() - stime) == 0.0)
    child()


def test_inkey_0s_cbreak_noinput_nokb():
    "0-second inkey without input or  keyboard."
    @as_subprocess
    def child():
        term = TestTerminal(stream=StringIO.StringIO())
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=0)
            assert (inp == u'')
            assert (math.floor(time.time() - stime) == 0.0)
    child()


def test_inkey_1s_cbreak_noinput():
    "1-second inkey without input; '' should be returned after ~1 second."
    @as_subprocess
    def child():
        term = TestTerminal()
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=1)
            assert (inp == u'')
            assert (math.floor(time.time() - stime) == 1.0)
    child()


def test_inkey_1s_cbreak_noinput_nokb():
    "1-second inkey without input or keyboard."
    @as_subprocess
    def child():
        term = TestTerminal(stream=StringIO.StringIO())
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=1)
            assert (inp == u'')
            assert (math.floor(time.time() - stime) == 1.0)
    child()


def test_inkey_0s_cbreak_input():
    "0-second inkey with input; Keypress should be immediately returned."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        # child pauses, writes semaphore and begins awaiting input
        term = TestTerminal()
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            inp = term.inkey(timeout=0)
            os.write(sys.__stdout__.fileno(), inp.encode('utf-8'))
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        os.write(master_fd, u'x'.encode('ascii'))
        read_until_semaphore(master_fd)
        stime = time.time()
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'x'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_inkey_cbreak_input_slowly():
    "0-second inkey with input; Keypress should be immediately returned."
    pid, master_fd = pty.fork()
    if pid is 0:
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        # child pauses, writes semaphore and begins awaiting input
        term = TestTerminal()
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            while True:
                inp = term.inkey(timeout=0.5)
                os.write(sys.__stdout__.fileno(), inp.encode('utf-8'))
                if inp == 'X':
                    break
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        os.write(master_fd, u'a'.encode('ascii'))
        time.sleep(0.1)
        os.write(master_fd, u'b'.encode('ascii'))
        time.sleep(0.1)
        os.write(master_fd, u'cdefgh'.encode('ascii'))
        time.sleep(0.1)
        os.write(master_fd, u'X'.encode('ascii'))
        read_until_semaphore(master_fd)
        stime = time.time()
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'abcdefghX'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_inkey_0s_cbreak_multibyte_utf8():
    "0-second inkey with multibyte utf-8 input; should decode immediately."
    # utf-8 bytes represent "latin capital letter upsilon".
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            inp = term.inkey(timeout=0)
            os.write(sys.__stdout__.fileno(), inp.encode('utf-8'))
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        os.write(master_fd, u'\u01b1'.encode('utf-8'))
        read_until_semaphore(master_fd)
        stime = time.time()
        output = read_until_eof(master_fd)
    pid, status = os.waitpid(pid, 0)
    assert output == u'Ʊ'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_inkey_0s_raw_ctrl_c():
    "0-second inkey with raw allows receiving ^C."
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        read_until_semaphore(sys.__stdin__.fileno(), semaphore=SEMAPHORE)
        with term.raw():
            os.write(sys.__stdout__.fileno(), RECV_SEMAPHORE)
            inp = term.inkey(timeout=0)
            os.write(sys.__stdout__.fileno(), inp.encode('latin1'))
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, SEND_SEMAPHORE)
        # ensure child is in raw mode before sending ^C,
        read_until_semaphore(master_fd)
        os.write(master_fd, u'\x03'.encode('latin1'))
        stime = time.time()
        output = read_until_eof(master_fd)
    pid, status = os.waitpid(pid, 0)
    if os.environ.get('TRAVIS', None) is not None:
        # For some reason, setraw has no effect travis-ci,
        # is still accepts ^C, causing system exit on py26,
        # but exit 0 on py27, and either way on py33
        # .. strange, huh?
        assert output in (u'', u'\x03')
        assert os.WEXITSTATUS(status) in (0, 2)
    else:
        assert (output == u'\x03' or
                output == u'' and not os.isatty(0))
        assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_inkey_0s_cbreak_sequence():
    "0-second inkey with multibyte sequence; should decode immediately."
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            inp = term.inkey(timeout=0)
            os.write(sys.__stdout__.fileno(), inp.name.encode('ascii'))
            sys.stdout.flush()
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, u'\x1b[D'.encode('ascii'))
        read_until_semaphore(master_fd)
        stime = time.time()
        output = read_until_eof(master_fd)
    pid, status = os.waitpid(pid, 0)
    assert output == u'KEY_LEFT'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0


def test_inkey_1s_cbreak_input():
    "1-second inkey w/multibyte sequence; should return after ~1 second."
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            inp = term.inkey(timeout=3)
            os.write(sys.__stdout__.fileno(), inp.name.encode('utf-8'))
            sys.stdout.flush()
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        read_until_semaphore(master_fd)
        stime = time.time()
        time.sleep(1)
        os.write(master_fd, u'\x1b[C'.encode('ascii'))
        output = read_until_eof(master_fd)

    pid, status = os.waitpid(pid, 0)
    assert output == u'KEY_RIGHT'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 1.0


def test_esc_delay_cbreak_035():
    "esc_delay will cause a single ESC (\\x1b) to delay for 0.35."
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=5)
            measured_time = (time.time() - stime) * 100
            os.write(sys.__stdout__.fileno(), (
                '%s %i' % (inp.name, measured_time,)).encode('ascii'))
            sys.stdout.flush()
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        read_until_semaphore(master_fd)
        stime = time.time()
        os.write(master_fd, u'\x1b'.encode('ascii'))
        key_name, duration_ms = read_until_eof(master_fd).split()

    pid, status = os.waitpid(pid, 0)
    assert key_name == u'KEY_ESCAPE'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0
    assert 35 <= int(duration_ms) <= 45, duration_ms


def test_esc_delay_cbreak_135():
    "esc_delay=1.35 will cause a single ESC (\\x1b) to delay for 1.35."
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=5, esc_delay=1.35)
            measured_time = (time.time() - stime) * 100
            os.write(sys.__stdout__.fileno(), (
                '%s %i' % (inp.name, measured_time,)).encode('ascii'))
            sys.stdout.flush()
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        read_until_semaphore(master_fd)
        stime = time.time()
        os.write(master_fd, u'\x1b'.encode('ascii'))
        key_name, duration_ms = read_until_eof(master_fd).split()

    pid, status = os.waitpid(pid, 0)
    assert key_name == u'KEY_ESCAPE'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 1.0
    assert 135 <= int(duration_ms) <= 145, int(duration_ms)


def test_esc_delay_cbreak_timout_0():
    """esc_delay still in effect with timeout of 0 ("nonblocking")."""
    pid, master_fd = pty.fork()
    if pid is 0:  # child
        try:
            cov = __import__('cov_core_init').init()
        except ImportError:
            cov = None
        term = TestTerminal()
        os.write(sys.__stdout__.fileno(), SEMAPHORE)
        with term.cbreak():
            stime = time.time()
            inp = term.inkey(timeout=0)
            measured_time = (time.time() - stime) * 100
            os.write(sys.__stdout__.fileno(), (
                '%s %i' % (inp.name, measured_time,)).encode('ascii'))
            sys.stdout.flush()
        if cov is not None:
            cov.stop()
            cov.save()
        os._exit(0)

    with echo_off(master_fd):
        os.write(master_fd, u'\x1b'.encode('ascii'))
        read_until_semaphore(master_fd)
        stime = time.time()
        key_name, duration_ms = read_until_eof(master_fd).split()

    pid, status = os.waitpid(pid, 0)
    assert key_name == u'KEY_ESCAPE'
    assert os.WEXITSTATUS(status) == 0
    assert math.floor(time.time() - stime) == 0.0
    assert 35 <= int(duration_ms) <= 45, int(duration_ms)


def test_keystroke_default_args():
    "Test keyboard.Keystroke constructor with default arguments."
    from blessed.keyboard import Keystroke
    ks = Keystroke()
    assert ks._name is None
    assert ks.name == ks._name
    assert ks._code is None
    assert ks.code == ks._code
    assert u'x' == u'x' + ks
    assert ks.is_sequence is False
    assert repr(ks) in ("u''",  # py26, 27
                        "''",)  # py33


def test_a_keystroke():
    "Test keyboard.Keystroke constructor with set arguments."
    from blessed.keyboard import Keystroke
    ks = Keystroke(ucs=u'x', code=1, name=u'the X')
    assert ks._name is u'the X'
    assert ks.name == ks._name
    assert ks._code is 1
    assert ks.code == ks._code
    assert u'xx' == u'x' + ks
    assert ks.is_sequence is True
    assert repr(ks) == "the X"


def test_get_keyboard_codes():
    "Test all values returned by get_keyboard_codes are from curses."
    from blessed.keyboard import (
        get_keyboard_codes,
        CURSES_KEYCODE_OVERRIDE_MIXIN,
    )
    exemptions = dict(CURSES_KEYCODE_OVERRIDE_MIXIN)
    for value, keycode in get_keyboard_codes().items():
        if keycode in exemptions:
            assert value == exemptions[keycode]
            continue
        assert hasattr(curses, keycode)
        assert getattr(curses, keycode) == value


def test_alternative_left_right():
    "Test _alternative_left_right behavior for space/backspace."
    from blessed.keyboard import _alternative_left_right
    term = mock.Mock()
    term._cuf1 = u''
    term._cub1 = u''
    assert not bool(_alternative_left_right(term))
    term._cuf1 = u' '
    term._cub1 = u'\b'
    assert not bool(_alternative_left_right(term))
    term._cuf1 = u'seq-right'
    term._cub1 = u'seq-left'
    assert (_alternative_left_right(term) == {
        u'seq-right': curses.KEY_RIGHT,
        u'seq-left': curses.KEY_LEFT})


def test_cuf1_and_cub1_as_RIGHT_LEFT(all_terms):
    "Test that cuf1 and cub1 are assigned KEY_RIGHT and KEY_LEFT."
    from blessed.keyboard import get_keyboard_sequences

    @as_subprocess
    def child(kind):
        term = TestTerminal(kind=kind, force_styling=True)
        keymap = get_keyboard_sequences(term)
        if term._cuf1:
            assert term._cuf1 != u' '
            assert term._cuf1 in keymap
            assert keymap[term._cuf1] == term.KEY_RIGHT
        if term._cub1:
            assert term._cub1 in keymap
            if term._cub1 == '\b':
                assert keymap[term._cub1] == term.KEY_BACKSPACE
            else:
                assert keymap[term._cub1] == term.KEY_LEFT

    child(all_terms)


def test_get_keyboard_sequences_sort_order(xterms):
    "ordereddict ensures sequences are ordered longest-first."
    @as_subprocess
    def child():
        term = TestTerminal(force_styling=True)
        maxlen = None
        for sequence, code in term._keymap.items():
            if maxlen is not None:
                assert len(sequence) <= maxlen
            assert sequence
            maxlen = len(sequence)
    child()


def test_get_keyboard_sequence(monkeypatch):
    "Test keyboard.get_keyboard_sequence. "
    import curses.has_key
    import blessed.keyboard

    (KEY_SMALL, KEY_LARGE, KEY_MIXIN) = range(3)
    (CAP_SMALL, CAP_LARGE) = 'cap-small cap-large'.split()
    (SEQ_SMALL, SEQ_LARGE, SEQ_MIXIN, SEQ_ALT_CUF1, SEQ_ALT_CUB1) = (
        b'seq-small-a',
        b'seq-large-abcdefg',
        b'seq-mixin',
        b'seq-alt-cuf1',
        b'seq-alt-cub1_')

    # patch curses functions
    monkeypatch.setattr(curses, 'tigetstr',
                        lambda cap: {CAP_SMALL: SEQ_SMALL,
                                     CAP_LARGE: SEQ_LARGE}[cap])

    monkeypatch.setattr(curses.has_key, '_capability_names',
                        dict(((KEY_SMALL, CAP_SMALL,),
                              (KEY_LARGE, CAP_LARGE,))))

    # patch global sequence mix-in
    monkeypatch.setattr(blessed.keyboard,
                        'DEFAULT_SEQUENCE_MIXIN', (
                            (SEQ_MIXIN.decode('latin1'), KEY_MIXIN),))

    # patch for _alternative_left_right
    term = mock.Mock()
    term._cuf1 = SEQ_ALT_CUF1.decode('latin1')
    term._cub1 = SEQ_ALT_CUB1.decode('latin1')
    keymap = blessed.keyboard.get_keyboard_sequences(term)

    assert keymap.items() == [
        (SEQ_LARGE.decode('latin1'), KEY_LARGE),
        (SEQ_ALT_CUB1.decode('latin1'), curses.KEY_LEFT),
        (SEQ_ALT_CUF1.decode('latin1'), curses.KEY_RIGHT),
        (SEQ_SMALL.decode('latin1'), KEY_SMALL),
        (SEQ_MIXIN.decode('latin1'), KEY_MIXIN)]


def test_resolve_sequence():
    "Test resolve_sequence for order-dependent mapping."
    from blessed.keyboard import resolve_sequence, OrderedDict
    mapper = OrderedDict(((u'SEQ1', 1),
                          (u'SEQ2', 2),
                          # takes precedence over LONGSEQ, first-match
                          (u'KEY_LONGSEQ_longest', 3),
                          (u'LONGSEQ', 4),
                          # wont match, LONGSEQ is first-match in this order
                          (u'LONGSEQ_longer', 5),
                          # falls through for L{anything_else}
                          (u'L', 6)))
    codes = {1: u'KEY_SEQ1',
             2: u'KEY_SEQ2',
             3: u'KEY_LONGSEQ_longest',
             4: u'KEY_LONGSEQ',
             5: u'KEY_LONGSEQ_longer',
             6: u'KEY_L'}
    ks = resolve_sequence(u'', mapper, codes)
    assert ks == u''
    assert ks.name is None
    assert ks.code is None
    assert ks.is_sequence is False
    assert repr(ks) in ("u''",  # py26, 27
                        "''",)  # py33

    ks = resolve_sequence(u'notfound', mapper=mapper, codes=codes)
    assert ks == u'n'
    assert ks.name is None
    assert ks.code is None
    assert ks.is_sequence is False
    assert repr(ks) in (u"u'n'", "'n'",)

    ks = resolve_sequence(u'SEQ1', mapper, codes)
    assert ks == u'SEQ1'
    assert ks.name == u'KEY_SEQ1'
    assert ks.code is 1
    assert ks.is_sequence is True
    assert repr(ks) in (u"KEY_SEQ1", "KEY_SEQ1")

    ks = resolve_sequence(u'LONGSEQ_longer', mapper, codes)
    assert ks == u'LONGSEQ'
    assert ks.name == u'KEY_LONGSEQ'
    assert ks.code is 4
    assert ks.is_sequence is True
    assert repr(ks) in (u"KEY_LONGSEQ", "KEY_LONGSEQ")

    ks = resolve_sequence(u'LONGSEQ', mapper, codes)
    assert ks == u'LONGSEQ'
    assert ks.name == u'KEY_LONGSEQ'
    assert ks.code is 4
    assert ks.is_sequence is True
    assert repr(ks) in (u"KEY_LONGSEQ", "KEY_LONGSEQ")

    ks = resolve_sequence(u'Lxxxxx', mapper, codes)
    assert ks == u'L'
    assert ks.name == u'KEY_L'
    assert ks.code is 6
    assert ks.is_sequence is True
    assert repr(ks) in (u"KEY_L", "KEY_L")
