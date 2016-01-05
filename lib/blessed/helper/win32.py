import msvcrt
import console
import contextlib
import os
from winsz import *

@contextlib.contextmanager
def cbreak(terminal):
    """Sets cbreak mode for current terminal.
    This is currently a stub here in Win32.

    This functionality may need to be implemented for the terminal
    essentially changing how getch below operates (filterng control
    sequences that generate signals on POSIX) but for now, 
    leaving as a stub"""
    try:
        yield
    finally:
	pass

@contextlib.contextmanager
def buffered(terminal):
    """Windows consoles operate differently from POSIX terminals.
    Terminals generate signals on control sequences, and they can be
    switched between key-at-a-time and line-at-a-time modes.  Windows
    consoles on the other hand have different APIs for reading
    key-at-a-time vs line-at-a-time.

    Because the only application here is to restore a POSIX terminal at the
    end of a curses run, this functionality is not implemented here."""
    try:
        yield
    finally:
	pass

@contextlib.contextmanager
def raw(terminal):
    """Windows terminals operate differently from POSIX terminals.
       By default they are already in raw mode, so this is necessarily a stub"""
    try:
        yield
    finally:
	pass

def get_size(terminal):
    """Gets he size of the current terminal"""

def echo(terminal, echo_bool):
    """Sets the terminal to echo output or not.  Not currently implemented.
    It is not believed this is needed at present"""
    return echo_bool

def getch(terminal):
    """Returns a single keystroke entered on the console window.
    This is not echoed in output."""
    return msvcrt32.getch()

def _height_and_width(terminal):
    """Return a tuple of (terminal height, terminal width).
       Always returns 25x80 on Windows currently unless environment
       variables say otherwise.
    """
    return WINSZ(ws_row=int(os.getenv('LINES', '25')),
                 ws_col=int(os.getenv('COLUMNS', '80')),
                 ws_xpixel=None,
                 ws_ypixel=None)

def _winsize(fd):
    """T._winsize -> WINSZ(ws_row, ws_col, ws_xpixel, ws_ypixel)

    The tty connected by file desriptor fd is queried for its window size,
    and returned as a collections.namedtuple instance WINSZ.

    On Windows, just returns _height_and_width(terminal)
    """
    return _height_and_width(None)
def kbhit(terminal, timeout=None, _intr_continue=None):
    return msvcrt.kbhit()
