"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from .topicmgr import (
    TopicManager, 
    TreeConfig
)

from .. import py2and3 


class PublisherBase:
    """
    Represent the class that send messages to listeners of given
    topics and that knows how to subscribe/unsubscribe listeners
    from topics.
    """
    
    def __init__(self, treeConfig = None):
        """If treeConfig is None, a default one is created from an
        instance of TreeConfig."""
        self.__treeConfig = treeConfig or TreeConfig()
        self.__topicMgr = TopicManager(self.__treeConfig)

    def getTopicMgr(self):
        """Get the topic manager created for this publisher."""
        return self.__topicMgr

    def getListenerExcHandler(self):
        """Get the listener exception handler that was registered
        via setListenerExcHandler(), or None of none registered."""
        return self.__treeConfig.listenerExcHandler

    def setListenerExcHandler(self, handler):
        """Set the function to call when a listener raises an exception
        during a sendMessage(). The handler must adhere to the 
        IListenerExcHandler API. """
        self.__treeConfig.listenerExcHandler = handler

    def addNotificationHandler(self, handler):
        """Add a handler for tracing pubsub activity. The handler should be
        a class that adheres to the API of INotificationHandler. """
        self.__treeConfig.notificationMgr.addHandler(handler)

    def clearNotificationHandlers(self):
        """Remove all notification handlers that were added via
        self.addNotificationHandler(). """
        self.__treeConfig.notificationMgr.clearHandlers()

    def setNotificationFlags(self, **kwargs):
        """Set the notification flags on or off for each type of
        pubsub activity. The kwargs keys can be any of the following:
        
        - subscribe:    if True, get notified whenever a listener subscribes to a topic;
        - unsubscribe:  if True, get notified whenever a listener unsubscribes from a topic;
        - deadListener: if True, get notified whenever a subscribed listener has been garbage-collected;
        - sendMessage:  if True, get notified whenever sendMessage() is called;
        - newTopic:     if True, get notified whenever a new topic is created;
        - delTopic:     if True, get notified whenever a topic is "deleted" from topic tree;
        - all:          set all of the above to the given value (True or False).

        The kwargs that are None are left at their current value. Those that are 
        False will cause corresponding notification to be silenced. The 'all'
        is set first, then the others. E.g.

            mgr.setFlagStates(all=True, delTopic=False)

        will toggle all notifications on, but will turn off the 'delTopic'
        notification.
        """
        self.__treeConfig.notificationMgr.setFlagStates(**kwargs)

    def getNotificationFlags(self):
        """Return a dictionary with the notification flag states."""
        return self.__treeConfig.notificationMgr.getFlagStates()

    def setTopicUnspecifiedFatal(self, newVal=True, checkExisting=True):
        """Changes the creation policy for topics.

        By default, pubsub will accept topic names for topics that 
        don't have a message data specification (MDS). This default behavior 
        makes pubsub easier to use initially, but allows topic
        names with typos to go uncaught in common operations such as
        sendMessage() and subscribe(). In a large application, this 
        can lead to nasty bugs. Pubsub's default behavior is equivalent
        to setTopicUnspecifiedFatal(false).
        
        When called with newVal=True, any future pubsub operation that
        requires a topic (such as subscribe and sendMessage) will require 
        an MDS; if none is available, pubsub will raise a TopicDefnError
        exception. 
        
        If checkExisting is not given or True, all existing
        topics are validated. A TopicDefnError exception is
        raised if one is found to be incomplete (has hasMDS() false).

        Returns previous value of newVal.

        Note that this method can be used in several ways:

        1. Only use it in your application when something is not working
           as expected: just add a call at the beginning of your app when
           you have a problem with topic messages not being received
           (for instance), and remove it when you have fixed the problem.

        2. Use it from the beginning of your app and never use newVal=False:
           add a call at the beginning of your app and you leave it in
           (forever), and use Topic Definition Providers to provide the
           listener specifications. These are easy to use via the
           pub.addTopicDefnProvider().

        3. Use it as in #1 during app development, and once stable, use
           #2. This is easiest to do in combination with
           pub.exportTopicTreeSpec().
         """
        oldVal = self.__treeConfig.raiseOnTopicUnspecified
        self.__treeConfig.raiseOnTopicUnspecified = newVal

        if newVal and checkExisting:
            self.__topicMgr.checkAllTopicsHaveMDS()

        return oldVal

    def sendMessage(self, topicName, *args, **kwargs):
        """Send a message for topic name with given data (args and kwargs).
        This will be overridden by derived classes that implement
        message-sending for different messaging protocols; not all 
        parameters may be accepted."""
        raise NotImplementedError

    def subscribe(self, listener, topicName):
        """Subscribe listener to named topic. Raises ListenerMismatchError
        if listener isn't compatible with the topic's MDS. Returns
        (pubsub.core.Listener, success), where success is False if listener 
        was already subscribed. The pub.core.Listener wraps the callable 
        subscribed and provides introspection-based info about 
        the callable.

        Note that if 'subscribe' notification is on, the handler's
        'notifySubscribe' method is called after subscription."""
        topicObj = self.__topicMgr.getOrCreateTopic(topicName)
        subscribedListener, success = topicObj.subscribe(listener)
        return subscribedListener, success

    def unsubscribe(self, listener, topicName):
        """Unsubscribe from given topic. Returns the pubsub.core.Listener
        instance that was used to wrap listener at subscription
        time. Raises an TopicNameError if topicName doesn't exist.

        Note that if 'unsubscribe' notification is on, the handler's
        notifyUnsubscribe() method will be called after unsubscribing. """
        topicObj = self.__topicMgr.getTopic(topicName)
        unsubdLisnr = topicObj.unsubscribe(listener)

        return unsubdLisnr

    def unsubAll(self, topicName = None,
        listenerFilter = None, topicFilter = None):
        """By default (no args given), unsubscribe all listeners from all
        topics. A listenerFilter can be given so that only the listeners
        that satisfy listenerFilter(listener) == True will be unsubscribed
        (with listener being a pub.Listener wrapper instance for each listener
        subscribed). A topicFilter can also be given so that only topics
        that satisfy topicFilter(topic name) == True will be affected.
        If only one topic should have listeners unsubscribed, then a topic
        name 'topicName' can be given *instead* instead of a topic filter.

        Returns the list of all listeners (instances of pub.Listener) that
        were unsubscribed from the topic tree).

        Note: this method will generate one 'unsubcribe' notification message
        (see pub.setNotificationFlags()) for each listener unsubscribed."""
        unsubdListeners = []

        if topicName is None:
            # unsubscribe all listeners from all topics
            topicsMap = self.__topicMgr._topicsMap
            for topicName, topicObj in py2and3.iteritems(topicsMap):
                if topicFilter is None or topicFilter(topicName):
                    tmp = topicObj.unsubscribeAllListeners(listenerFilter)
                    unsubdListeners.extend(tmp)

        else:
            topicObj = self.__topicMgr.getTopic(topicName)
            unsubdListeners = topicObj.unsubscribeAllListeners(listenerFilter)

        return unsubdListeners


