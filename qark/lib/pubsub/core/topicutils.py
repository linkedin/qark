"""
Various utilities used by topic-related modules. 

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.

"""

from textwrap import TextWrapper, dedent

from .topicexc import TopicNameError

from .. import py2and3

__all__ = []


UNDERSCORE = '_' # topic name can't start with this
# just want something unlikely to clash with user's topic names
ALL_TOPICS = 'ALL_TOPICS'


class WeakNone:
    """Pretend to be a weak reference to nothing. Used by ArgsInfos to
    refer to parent when None so no if-else blocks needed. """
    def __call__(self):
        return None


def smartDedent(paragraph):
    """Dedent paragraph using textwrap.dedent(), but properly dedents
    even if the first line of paragraph does not contain blanks. 
    This handles the case where a user types a documentation string as 
        '''A long string spanning
        several lines.'''
    """
    if paragraph.startswith(' '):
        para = dedent(paragraph)
    else:
        lines = paragraph.split('\n')
        exceptFirst = dedent('\n'.join(lines[1:]))
        para = lines[0]+exceptFirst
    return para


import re
_validNameRE = re.compile(r'[-0-9a-zA-Z]\w*')


def validateName(topicName):
    """Raise TopicNameError if nameTuple not valid as topic name."""
    topicNameTuple = tupleize(topicName)
    if not topicNameTuple:
        reason = 'name tuple must have at least one item!'
        raise TopicNameError(None, reason)

    class topic: pass
    for subname in topicNameTuple:
        if not subname:
            reason = 'can\'t contain empty string or None'
            raise TopicNameError(topicNameTuple, reason)

        if subname.startswith(UNDERSCORE):
            reason = 'must not start with "%s"' % UNDERSCORE
            raise TopicNameError(topicNameTuple, reason)

        if subname == ALL_TOPICS:
            reason = 'string "%s" is reserved for root topic' % ALL_TOPICS
            raise TopicNameError(topicNameTuple, reason)

        if _validNameRE.match(subname) is None:
            reason = 'element #%s ("%s") has invalid characters' % \
                (1+list(topicNameTuple).index(subname), subname)
            raise TopicNameError(topicNameTuple, reason)


def stringize(topicName):
    """If topicName is a string, just return it
    as is. If it is a topic definition object (ie an object that has 
    'msgDataSpec' as data member), return the dotted name of corresponding
    topic. Otherwise, assume topicName is a tuple and convert it to to a 
    dotted name i.e. ('a','b','c') => 'a.b.c'. Empty name is not allowed 
    (ValueError). The reverse operation is tupleize(topicName)."""
    if py2and3.isstring(topicName):
        return topicName
    
    if hasattr(topicName, "msgDataSpec"): 
        return topicName._topicNameStr

    try:
        name = '.'.join(topicName)
    except Exception:
        exc = py2and3.getexcobj()
        raise TopicNameError(topicName, str(exc))
    
    return name


def tupleize(topicName):
    """If topicName is a tuple of strings, just return it as is. Otherwise,
    convert it to tuple, assuming dotted notation used for topicName. I.e. 
    'a.b.c' => ('a','b','c'). Empty topicName is not allowed (ValueError). 
    The reverse operation is stringize(topicNameTuple)."""
    # assume name is most often str; if more often tuple, 
    # then better use isinstance(name, tuple)
    if hasattr(topicName, "msgDataSpec"): 
        topicName = topicName._topicNameStr
    if py2and3.isstring(topicName): 
        topicTuple = tuple(topicName.split('.'))
    else:
        topicTuple = tuple(topicName) # assume already tuple of strings
        
    if not topicTuple:
        raise TopicNameError(topicTuple, "Topic name can't be empty!")
                
    return topicTuple


