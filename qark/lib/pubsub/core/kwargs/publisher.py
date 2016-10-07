"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""


from .publisherbase import PublisherBase
from .datamsg import Message
from .. import (policies, py2and3)



class Publisher(PublisherBase):
    """
    Publisher used for kwargs protocol, ie when sending message data
    via keyword arguments.
    """

    def sendMessage(self, topicName, **kwargs):
        """Send a message.

        :param topicName: name of message topic (dotted or tuple format)
        :param kwargs: message data (must satisfy the topic's MDS)
        """
        topicMgr = self.getTopicMgr()
        topicObj = topicMgr.getOrCreateTopic(topicName)
        topicObj.publish(**kwargs)

    def getMsgProtocol(self):
        return 'kwargs'


class PublisherArg1Stage2(Publisher):
    """
    This is used when transitioning from arg1 to kwargs
    messaging protocol.
    """

    _base = Publisher
    
    class SenderTooManyKwargs(RuntimeError):
        def __init__(self, kwargs, commonArgName):
            extra = kwargs.copy()
            del extra[commonArgName]
            msg = 'Sender has too many kwargs (%s)' % ( py2and3.keys(extra),)
            RuntimeError.__init__(self, msg)

    class SenderWrongKwargName(RuntimeError):
        def __init__(self, actualKwargName, commonArgName):
            msg = 'Sender uses wrong kwarg name ("%s" instead of "%s")' \
                % (actualKwargName, commonArgName)
            RuntimeError.__init__(self, msg)

    def __init__(self, treeConfig = None):
        self._base.__init__(self, treeConfig)
        self.Msg = Message

    def sendMessage(self, _topicName, **kwarg):
        commonArgName = policies.msgDataArgName
        if len(kwarg) > 1:
            raise self.SenderTooManyKwargs(kwarg, commonArgName)
        elif len(kwarg) == 1 and commonArgName not in kwarg:
            raise self.SenderWrongKwargName( py2and3.keys(kwarg)[0], commonArgName)

        data = kwarg.get(commonArgName, None)
        kwargs = { commonArgName: self.Msg( _topicName, data) }
        self._base.sendMessage( self, _topicName, **kwargs )

    def getMsgProtocol(self):
        return 'kwarg1'


if policies.msgProtocolTransStage is not None:
    Publisher = PublisherArg1Stage2
    #print 'Using protocol', Publisher


