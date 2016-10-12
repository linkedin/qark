"""
This is the main entry-point to pubsub's core functionality. The :mod:`~pubsub.pub` 
module supports:

* messaging: publishing and receiving messages of a given topic
* tracing: tracing pubsub activity in an application
* trapping exceptions: dealing with "badly behaved" listeners (ie that leak exceptions)
* specificatio of topic tree: defining (or just documenting) the topic tree of an 
  application; message data specification (MDS)

The recommended usage is ::

    from pubsub import pub
    
    // use pub functions:
    pub.sendMessage(...)
    
Note that this module creates a "default" instance of 
pubsub.core.Publisher and binds several local functions to some of its methods
and those of the pubsub.core.TopicManager instance that it contains. However, an
application may create as many independent instances of Publisher as
required (for instance, one in each thread; with a custom queue to mediate 
message transfer between threads).
"""

"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

VERSION_API = 3  #: major API version

VERSION_SVN = "$Rev: 243 $".split()[1]  # DO NOT CHANGE: automatically updated by VCS

from .core import (
    Publisher as _Publisher,

    AUTO_TOPIC,

    ListenerMismatchError,
    TopicDefnError, 

    IListenerExcHandler,
    ExcHandlerError,

    SenderMissingReqdMsgDataError, 
    SenderUnknownMsgDataError, 
    
    TopicDefnError,
    TopicNameError,
    UnrecognizedSourceFormatError,
    
    ALL_TOPICS,
    
    MessageDataSpecError, 
    exportTopicTreeSpec,
    TOPIC_TREE_FROM_MODULE,
    TOPIC_TREE_FROM_STRING,
    TOPIC_TREE_FROM_CLASS, 

    TopicTreeTraverser,
    
    INotificationHandler,
)

__all__ = [
    # listener stuff:
    'subscribe', 
    'unsubscribe', 
    'unsubAll',
    'isSubscribed', 

    'isValid', 
    'validate',
    'ListenerMismatchError',
    'AUTO_TOPIC',

    'IListenerExcHandler',
    'getListenerExcHandler', 
    'setListenerExcHandler',
    'ExcHandlerError',
    
    # topic stuff:
    
    'ALL_TOPICS', 
    'topicTreeRoot', 
    'topicsMap', 
    
    'getDefaultTopicMgr', 

    # topioc defn provider stuff
    
    'addTopicDefnProvider', 
    'clearTopicDefnProviders',
    'getNumTopicDefnProviders',
    'TOPIC_TREE_FROM_MODULE',
    'TOPIC_TREE_FROM_CLASS', 
    'TOPIC_TREE_FROM_STRING',
    'exportTopicTreeSpec', 
    'instantiateAllDefinedTopics'

    'TopicDefnError', 
    'TopicNameError', 
    
    'setTopicUnspecifiedFatal',

    # publisher stuff:

    'sendMessage', 
    'SenderMissingReqdMsgDataError', 
    'SenderUnknownMsgDataError',

    # misc:
    
    'addNotificationHandler', 
    'setNotificationFlags', 
    'getNotificationFlags',
    'clearNotificationHandlers',
    
    'TopicTreeTraverser',

]


# --------- Publisher singleton and bound methods ------------------------------------

_publisher = _Publisher()

subscribe   = _publisher.subscribe
unsubscribe = _publisher.unsubscribe
unsubAll    = _publisher.unsubAll
sendMessage = _publisher.sendMessage

getListenerExcHandler     = _publisher.getListenerExcHandler
setListenerExcHandler     = _publisher.setListenerExcHandler

addNotificationHandler    = _publisher.addNotificationHandler
clearNotificationHandlers = _publisher.clearNotificationHandlers
setNotificationFlags      = _publisher.setNotificationFlags
getNotificationFlags      = _publisher.getNotificationFlags

setTopicUnspecifiedFatal  = _publisher.setTopicUnspecifiedFatal

getMsgProtocol            = _publisher.getMsgProtocol

def getDefaultPublisher():
    """Get the Publisher instance created by default when this module
    is imported. See the module doc for details about this instance."""
    return _publisher


# ---------- default TopicManager instance and bound methods ------------------------

_topicMgr = _publisher.getTopicMgr()

topicTreeRoot = _topicMgr.getRootAllTopics() 
topicsMap     = _topicMgr._topicsMap 


def isValid(listener, topicName):
    """Return true only if listener can subscribe to messages of given topic."""
    return _topicMgr.getTopic(topicName).isValid(listener)


def validate(listener, topicName):
    """Checks if listener can subscribe to topicName. If not, raises
    ListenerMismatchError, otherwise just returns."""
    _topicMgr.getTopic(topicName).validate(listener)


def isSubscribed(listener, topicName):
    """Returns true if listener has subscribed to topicName, false otherwise.
    WARNING: a false return is not a guarantee that listener won't get
    messages of topicName: it could receive messages of a subtopic of
    topicName. """
    return _topicMgr.getTopic(topicName).hasListener(listener)


def getDefaultTopicMgr():
    """Get the TopicManager instance created by default when this 
    module is imported. This function is a shortcut for 
    ``pub.getDefaultPublisher().getTopicMgr()``."""
    return _topicMgr


addTopicDefnProvider     = _topicMgr.addDefnProvider
clearTopicDefnProviders  = _topicMgr.clearDefnProviders
getNumTopicDefnProviders = _topicMgr.getNumDefnProviders

def instantiateAllDefinedTopics(provider):
    """Loop over all topics of given provider and "instantiate" each topic, thus 
    forcing a parse of the topics documentation, message data specification (MDS), 
    comparison with parent MDS, and MDS documentation. Without this function call, 
    an error among any of those characteristics will manifest only if the a 
    listener is registered on it. """
    for topicName in provider:
        _topicMgr.getOrCreateTopic(topicName)
        
#---------------------------------------------------------------------------
