"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from .listenerbase import (ListenerBase, ValidatorBase)
from .callables import ListenerMismatchError
from .. import policies


class Message:
    """
    A simple container object for the two components of a topic messages
    in the pubsub legacy API: the
    topic and the user data. An instance of Message is given to your
    listener when called by sendMessage(topic). The data is accessed
    via the 'data' attribute, and can be type of object.
    """
    def __init__(self, topicNameTuple, data):
        self.topic = topicNameTuple
        self.data  = data

    def __str__(self):
        return '[Topic: '+repr(self.topic)+',  Data: '+repr(self.data)+']'


class Listener(ListenerBase):
    """
    Wraps a callable so it can be stored by weak reference and introspected
    to verify that it adheres to a topic's MDS. 
    
    A Listener instance has the same hash value as the callable that it wraps. 

    A callable will be given data when a message is sent to it. In the arg1 
    protocol only one object can be sent via sendMessage, it is put in a 
    Message object in its "data" field, the listener receives the Message 
    object. 
    """
    
    def __call__(self, actualTopic, data):
        """Call the listener with data. Note that it raises RuntimeError
        if listener is dead. Should always return True (False would require
        the callable_ be dead but self hasn't yet been notified of it...)."""
        kwargs = {}
        if self._autoTopicArgName is not None:
            kwargs[self._autoTopicArgName] = actualTopic
        cb = self._callable()
        if cb is None:
            self._calledWhenDead()
        msg = Message(actualTopic.getNameTuple(), data)
        cb(msg, **kwargs)
        return True


class ListenerValidator(ValidatorBase):
    """
    Accept one arg or *args; accept any **kwarg,
    and require that the Listener have at least all the kwargs (can
    have extra) of Topic.
    """

    def _validateArgs(self, listener, paramsInfo):
        # accept **kwargs
        # accept *args
        # accept any keyword args

        if (paramsInfo.getAllArgs() == ()) and paramsInfo.acceptsAllUnnamedArgs:
            return

        if paramsInfo.getAllArgs() == ():
            msg = 'Must have at least one parameter (any name, with or without default value, or *arg)'
            raise ListenerMismatchError(msg, listener, [])

        assert paramsInfo.getAllArgs()
        #assert not paramsInfo.acceptsAllUnnamedArgs

        # verify at most one required arg
        numReqdArgs = paramsInfo.numRequired
        if numReqdArgs > 1:
            allReqd = paramsInfo.getRequiredArgs()
            msg = 'only one of %s can be a required agument' % (allReqd,)
            raise ListenerMismatchError(msg, listener, allReqd)

        # if no required args but listener has *args, then we
        # don't care about anything else:
        if numReqdArgs == 0 and paramsInfo.acceptsAllUnnamedArgs:
            return

        # if no policy set, any name ok; otherwise validate name:
        needArgName = policies.msgDataArgName
        firstArgName = paramsInfo.allParams[0]
        if (needArgName is not None) and firstArgName != needArgName:
            msg = 'listener arg name must be "%s" (is "%s")' % (needArgName, firstArgName)
            effTopicArgs = [needArgName]
            raise ListenerMismatchError(msg, listener, effTopicArgs)


