import curses
import tty
import os
import sys
import termios
import fcntl
import select
import contextlib
from winsz import *

@contextlib.contextmanager
def cbreak(terminal):
    """Return a context manager that enters 'cbreak' mode: disabling line
    buffering of keyboard input, making characters typed by the user
    immediately available to the program.  Also referred to as 'rare'
    mode, this is the opposite of 'cooked' mode, the default for most
    shells.

    In 'cbreak' mode, echo of input is also disabled: the application must
    explicitly print any input received, if they so wish.

    More information can be found in the manual page for curses.h,
    http://www.openbsd.org/cgi-bin/man.cgi?query=cbreak

    The python manual for curses,
    http://docs.python.org/2/library/curses.html

    Note also that setcbreak sets VMIN = 1 and VTIME = 0,
    http://www.unixwiz.net/techtips/termios-vmin-vtime.html
    """
    if self.keyboard_fd is not None:
        # save current terminal mode,
        save_mode = termios.tcgetattr(self.keyboard_fd)
        tty.setcbreak(terminal.keyboard_fd, termios.TCSANOW)
        try:
            yield
        finally:
            # restore prior mode,
            termios.tcsetattr(self.keyboard_fd,
                              termios.TCSAFLUSH,
                              save_mode)
    else:
        yield

def buffered(terminal):
    """Sets bufferred mode for current terminal"""

def get_size(terminal):
    """Gets he size of the current terminal"""

def echo(terminal, echo_bool):
    """Sets the terminal to echo output or not"""

def raw(terminal):
    """Return a context manager that enters *raw* mode. Raw mode is
    similar to *cbreak* mode, in that characters typed are immediately
    available to ``inkey()`` with one exception: the interrupt, quit,
    suspend, and flow control characters are all passed through as their
    raw character values instead of generating a signal.
    """
    if self.keyboard_fd is not None:
        # save current terminal mode,
        save_mode = termios.tcgetattr(self.keyboard_fd)
        tty.setraw(self.keyboard_fd, termios.TCSANOW)
        try:
            yield
        finally:
            # restore prior mode,
            termios.tcsetattr(self.keyboard_fd,
                              termios.TCSAFLUSH,
                              save_mode)
    else:
        yield

def getch(terminal):
        """T.getch() -> unicode

        Read and decode next byte from keyboard stream.  May return u''
        if decoding is not yet complete, or completed unicode character.
        Should always return bytes when self.kbhit() returns True.

        Implementors of input streams other than os.read() on the stdin fd
        should derive and override this method.
        """
        byte = os.read(self.keyboard_fd, 1)
        return self._keyboard_decoder.decode(byte, final=False)
def _winsize(fd):
        """T._winsize -> WINSZ(ws_row, ws_col, ws_xpixel, ws_ypixel)

        The tty connected by file desriptor fd is queried for its window size,
        and returned as a collections.namedtuple instance WINSZ.

        May raise exception IOError.
        """
        data = fcntl.ioctl(fd, termios.TIOCGWINSZ, WINSZ._BUF)
        return WINSZ(*struct.unpack(WINSZ._FMT, data))
def _height_and_width(terminal):
    """Return a tuple of (terminal height, terminal width).
    """
    # TODO(jquast): hey kids, even if stdout is redirected to a file,
    # we can still query sys.__stdin__.fileno() for our terminal size.
    # -- of course, if both are redirected, we have no use for this fd.
    for fd in (terminal._init_descriptor, sys.__stdout__):
        try:
            if fd is not None:
                return _winsize(fd)
        except IOError:
            pass

    return WINSZ(ws_row=int(os.getenv('LINES', '25')),
                 ws_col=int(os.getenv('COLUMNS', '80')),
                 ws_xpixel=None,
                 ws_ypixel=None)
def kbhit(terminal, timeout=None, _intr_continue=True):
    """T.kbhit([timeout=None]) -> bool

    Returns True if a keypress has been detected on keyboard.

    When ``timeout`` is 0, this call is non-blocking, Otherwise blocking
    until keypress is detected (default).  When ``timeout`` is a positive
    number, returns after ``timeout`` seconds have elapsed.

    If input is not a terminal, False is always returned.
    """
    # Special care is taken to handle a custom SIGWINCH handler, which
    # causes select() to be interrupted with errno 4 (EAGAIN) --
    # it is ignored, and a new timeout value is derived from the previous,
    # unless timeout becomes negative, because signal handler has blocked
    # beyond timeout, then False is returned. Otherwise, when timeout is 0,
    # we continue to block indefinitely (default).
    stime = time.time()
    check_w, check_x = [], []
    check_r = [terminal.keyboard_fd] if terminal.keyboard_fd is not None else []

    while True:
        try:
            ready_r, ready_w, ready_x = select.select(
                check_r, check_w, check_x, timeout)
        except InterruptedError:
            if not _intr_continue:
                return u''
            if timeout is not None:
                # subtract time already elapsed,
                timeout -= time.time() - stime
                if timeout > 0:
                    continue
                # no time remains after handling exception (rare)
                ready_r = []
                break
        else:
            break

    return False if terminal.keyboard_fd is None else check_r == ready_r

