"This sub-module provides formatting functions."
import curses

_derivatives = ('on', 'bright', 'on_bright',)

_colors = set('black red green yellow blue magenta cyan white'.split())
_compoundables = set('bold underline reverse blink dim italic shadow '
                     'standout subscript superscript'.split())

#: Valid colors and their background (on), bright, and bright-bg derivatives.
COLORS = set(['_'.join((derivitive, color))
              for derivitive in _derivatives
              for color in _colors]) | _colors

#: All valid compoundable names.
COMPOUNDABLES = (COLORS | _compoundables)


class ParameterizingString(unicode):
    """A Unicode string which can be called as a parameterizing termcap.

    For example::

        >> term = Terminal()
        >> color = ParameterizingString(term.color, term.normal, 'color')
        >> color(9)('color #9')
        u'\x1b[91mcolor #9\x1b(B\x1b[m'
    """

    def __new__(cls, *args):
        """P.__new__(cls, cap, [normal, [name]])

        :arg cap: parameterized string suitable for curses.tparm()
        :arg normal: terminating sequence for this capability.
        :arg name: name of this terminal capability.
        """
        assert len(args) and len(args) < 4, args
        new = unicode.__new__(cls, args[0])
        new._normal = len(args) > 1 and args[1] or u''
        new._name = len(args) > 2 and args[2] or u'<not specified>'
        return new

    def __call__(self, *args):
        """P(*args) -> FormattingString()

        Return evaluated terminal capability (self), receiving arguments
        ``*args``, followed by the terminating sequence (self.normal) into
        a FormattingString capable of being called.
        """
        try:
            # Re-encode the cap, because tparm() takes a bytestring in Python
            # 3. However, appear to be a plain Unicode string otherwise so
            # concats work.
            attr = curses.tparm(self.encode('latin1'), *args).decode('latin1')
            return FormattingString(attr, self._normal)
        except TypeError, err:
            # If the first non-int (i.e. incorrect) arg was a string, suggest
            # something intelligent:
            if len(args) and isinstance(args[0], basestring):
                raise TypeError(
                    "A native or nonexistent capability template, %r received"
                    " invalid argument %r: %s. You probably misspelled a"
                    " formatting call like `bright_red'" % (
                        self._name, args, err))
            # Somebody passed a non-string; I don't feel confident
            # guessing what they were trying to do.
            raise


class ParameterizingProxyString(unicode):
    """A Unicode string which can be called to proxy missing termcap entries.

    For example::

        >>> from blessed import Terminal
        >>> term = Terminal('screen')
        >>> hpa = ParameterizingString(term.hpa, term.normal, 'hpa')
        >>> hpa(9)
        u''
        >>> fmt = u'\x1b[{0}G'
        >>> fmt_arg = lambda *arg: (arg[0] + 1,)
        >>> hpa = ParameterizingProxyString((fmt, fmt_arg), term.normal, 'hpa')
        >>> hpa(9)
        u'\x1b[10G'
    """

    def __new__(cls, *args):
        """P.__new__(cls, (fmt, callable), [normal, [name]])

        :arg fmt: format string suitable for displaying terminal sequences.
        :arg callable: receives __call__ arguments for formatting fmt.
        :arg normal: terminating sequence for this capability.
        :arg name: name of this terminal capability.
        """
        assert len(args) and len(args) < 4, args
        assert type(args[0]) is tuple, args[0]
        assert callable(args[0][1]), args[0][1]
        new = unicode.__new__(cls, args[0][0])
        new._fmt_args = args[0][1]
        new._normal = len(args) > 1 and args[1] or u''
        new._name = len(args) > 2 and args[2] or u'<not specified>'
        return new

    def __call__(self, *args):
        """P(*args) -> FormattingString()

        Return evaluated terminal capability format, (self), using callable
        ``self._fmt_args`` receiving arguments ``*args``, followed by the
        terminating sequence (self.normal) into a FormattingString capable
        of being called.
        """
        return FormattingString(self.format(*self._fmt_args(*args)),
                                self._normal)


def get_proxy_string(term, attr):
    """ Returns an instance of ParameterizingProxyString
    for (some kinds) of terminals and attributes.
    """
    if term._kind == 'screen' and attr in ('hpa', 'vpa'):
        if attr == 'hpa':
            fmt = u'\x1b[{0}G'
        elif attr == 'vpa':
            fmt = u'\x1b[{0}d'
        fmt_arg = lambda *arg: (arg[0] + 1,)
        return ParameterizingProxyString((fmt, fmt_arg),
                                         term.normal, 'hpa')
    return None


class FormattingString(unicode):
    """A Unicode string which can be called using ``text``,
    returning a new string, ``attr`` + ``text`` + ``normal``::

        >> style = FormattingString(term.bright_blue, term.normal)
        >> style('Big Blue')
        u'\x1b[94mBig Blue\x1b(B\x1b[m'
    """

    def __new__(cls, *args):
        """P.__new__(cls, sequence, [normal])
        :arg sequence: terminal attribute sequence.
        :arg normal: terminating sequence for this attribute.
        """
        assert 1 <= len(args) <= 2, args
        new = unicode.__new__(cls, args[0])
        new._normal = len(args) > 1 and args[1] or u''
        return new

    def __call__(self, text):
        """P(text) -> unicode

        Return string ``text``, joined by specified video attribute,
        (self), and followed by reset attribute sequence (term.normal).
        """
        if len(self):
            return u''.join((self, text, self._normal))
        return text


class NullCallableString(unicode):
    """A dummy callable Unicode to stand in for ``FormattingString`` and
    ``ParameterizingString`` for terminals that cannot perform styling.
    """
    def __new__(cls):
        new = unicode.__new__(cls, u'')
        return new

    def __call__(self, *args):
        """Return a Unicode or whatever you passed in as the first arg
        (hopefully a string of some kind).

        When called with an int as the first arg, return an empty Unicode. An
        int is a good hint that I am a ``ParameterizingString``, as there are
        only about half a dozen string-returning capabilities listed in
        terminfo(5) which accept non-int arguments, they are seldom used.

        When called with a non-int as the first arg (no no args at all), return
        the first arg, acting in place of ``FormattingString`` without
        any attributes.
        """
        if len(args) != 1 or isinstance(args[0], int):
            # I am acting as a ParameterizingString.

            # tparm can take not only ints but also (at least) strings as its
            # 2nd...nth argument. But we don't support callable parameterizing
            # capabilities that take non-ints yet, so we can cheap out here.

            # TODO(erikrose): Go through enough of the motions in the
            # capability resolvers to determine which of 2 special-purpose
            # classes, NullParameterizableString or NullFormattingString,
            # to return, and retire this one.

            # As a NullCallableString, even when provided with a parameter,
            # such as t.color(5), we must also still be callable, fe:
            #
            # >>> t.color(5)('shmoo')
            #
            # is actually simplified result of NullCallable()() on terminals
            # without color support, so turtles all the way down: we return
            # another instance.
            return NullCallableString()
        return args[0]


def split_compound(compound):
    """Split a possibly compound format string into segments.

    >>> split_compound('bold_underline_bright_blue_on_red')
    ['bold', 'underline', 'bright_blue', 'on_red']

    """
    merged_segs = []
    # These occur only as prefixes, so they can always be merged:
    mergeable_prefixes = ['on', 'bright', 'on_bright']
    for s in compound.split('_'):
        if merged_segs and merged_segs[-1] in mergeable_prefixes:
            merged_segs[-1] += '_' + s
        else:
            merged_segs.append(s)
    return merged_segs


def resolve_capability(term, attr):
    """Return a Unicode string for the terminal capability ``attr``,
    or an empty string if not found, or if terminal is without styling
    capabilities.
    """
    # Decode sequences as latin1, as they are always 8-bit bytes, so when
    # b'\xff' is returned, this must be decoded to u'\xff'.
    if not term.does_styling:
        return u''
    val = curses.tigetstr(term._sugar.get(attr, attr))
    return u'' if val is None else val.decode('latin1')


def resolve_color(term, color):
    """resolve_color(T, color) -> FormattingString()

    Resolve a ``color`` name to callable capability, ``FormattingString``
    unless ``term.number_of_colors`` is 0, then ``NullCallableString``.

    Valid ``color`` capabilities names are any of the simple color
    names, such as ``red``, or compounded, such as ``on_bright_green``.
    """
    # NOTE(erikrose): Does curses automatically exchange red and blue and cyan
    # and yellow when a terminal supports setf/setb rather than setaf/setab?
    # I'll be blasted if I can find any documentation. The following
    # assumes it does.
    color_cap = (term._background_color if 'on_' in color else
                 term._foreground_color)

    # curses constants go up to only 7, so add an offset to get at the
    # bright colors at 8-15:
    offset = 8 if 'bright_' in color else 0
    base_color = color.rsplit('_', 1)[-1]
    if term.number_of_colors == 0:
        return NullCallableString()

    attr = 'COLOR_%s' % (base_color.upper(),)
    fmt_attr = color_cap(getattr(curses, attr) + offset)
    return FormattingString(fmt_attr, term.normal)


def resolve_attribute(term, attr):
    """Resolve a sugary or plain capability name, color, or compound
    formatting name into a *callable* unicode string capability,
    ``ParameterizingString`` or ``FormattingString``.
    """
    # A simple color, such as `red' or `blue'.
    if attr in COLORS:
        return resolve_color(term, attr)

    # A direct compoundable, such as `bold' or `on_red'.
    if attr in COMPOUNDABLES:
        sequence = resolve_capability(term, attr)
        return FormattingString(sequence, term.normal)

    # Given `bold_on_red', resolve to ('bold', 'on_red'), RECURSIVE
    # call for each compounding section, joined and returned as
    # a completed completed FormattingString.
    formatters = split_compound(attr)
    if all(fmt in COMPOUNDABLES for fmt in formatters):
        resolution = (resolve_attribute(term, fmt) for fmt in formatters)
        return FormattingString(u''.join(resolution), term.normal)
    else:
        # and, for special terminals, such as 'screen', provide a Proxy
        # ParameterizingString for attributes they do not claim to support, but
        # actually do! (such as 'hpa' and 'vpa').
        proxy = get_proxy_string(term, term._sugar.get(attr, attr))
        if proxy is not None:
            return proxy
        # otherwise, this is our end-game: given a sequence such as 'csr'
        # (change scrolling region), return a ParameterizingString instance,
        # that when called, performs and returns the final string after curses
        # capability lookup is performed.
        tparm_capseq = resolve_capability(term, attr)
        return ParameterizingString(tparm_capseq, term.normal, attr)
