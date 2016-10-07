"""
Some topic definition validation functions. 

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from .topicexc import MessageDataSpecError


def verifyArgsDifferent(allArgs, allParentArgs, topicName):
    """Verify that allArgs does not contain any of allParentArgs. Raise
    MessageDataSpecError if fail. """
    extra = set(allArgs).intersection(allParentArgs)
    if extra:
        msg = 'Args %%s already used in parent of "%s"' % topicName
        raise MessageDataSpecError( msg, tuple(extra) )


def verifySubset(all, sub, topicName, extraMsg=''):
    """Verify that sub is a subset of all for topicName. Raise
    MessageDataSpecError if fail. """
    notInAll = set(sub).difference(all)
    if notInAll:
        args = ','.join(all)
        msg = 'Params [%s] missing inherited [%%s] for topic "%s"%s' % (args, topicName, extraMsg)
        raise MessageDataSpecError(msg, tuple(notInAll) )


