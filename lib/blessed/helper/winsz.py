
import struct
import collections

WINSZ = collections.namedtuple('WINSZ', (
    'ws_row',     # /* rows, in characters */
    'ws_col',     # /* columns, in characters */
    'ws_xpixel',  # /* horizontal size, pixels */
    'ws_ypixel',  # /* vertical size, pixels */
))
#: format of termios structure
WINSZ._FMT = 'hhhh'
#: buffer of termios structure appropriate for ioctl argument
WINSZ._BUF = '\x00' * struct.calcsize(WINSZ._FMT)
