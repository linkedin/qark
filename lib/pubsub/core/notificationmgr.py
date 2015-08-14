"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""
import sys

class NotificationMgr:
    """
    Manages notifications for tracing pubsub activity. When pubsub takes a 
    certain action such as sending a message or creating a topic, and 
    the notification flag for that activity is True, all registered
    notification handlers get corresponding method called with information
    about the activity, such as which listener subscribed to which topic. 
    See INotificationHandler for which method gets called for each activity.
    
    If more than one notification handler has been registered, the order in 
    which they are notified is unspecified (do not rely on it).

    Note that this manager automatically unregisters all handlers when
    the Python interpreter exits, to help avoid NoneType exceptions during
    shutdown. This "shutdown" starts when the last line of app "main" has
    executed; the Python interpreter then starts cleaning up, garbage 
    collecting everything, which could lead to various pubsub notifications
    -- by then they should be of no interest -- such as dead
    listeners, etc. 
    """

    def __init__(self, notificationHandler = None):
        self.__notifyOnSend = False
        self.__notifyOnSubscribe = False
        self.__notifyOnUnsubscribe = False

        self.__notifyOnNewTopic = False
        self.__notifyOnDelTopic = False
        self.__notifyOnDeadListener = False

        self.__handlers = []
        if notificationHandler is not None:
            self.addHandler(notificationHandler)

        self.__atExitRegistered = False

    def addHandler(self, handler):
        if not self.__atExitRegistered:
            self.__registerForAppExit()
        self.__handlers.append(handler)

    def getHandlers(self):
        return self.__handlers[:]

    def clearHandlers(self):
        self.__handlers = []

    def notifySubscribe(self, *args, **kwargs):
        if self.__notifyOnSubscribe and self.__handlers:
            for handler in self.__handlers:
                handler.notifySubscribe(*args, **kwargs)

    def notifyUnsubscribe(self, *args, **kwargs):
        if self.__notifyOnUnsubscribe and self.__handlers:
            for handler in self.__handlers:
                handler.notifyUnsubscribe(*args, **kwargs)

    def notifySend(self, *args, **kwargs):
        if self.__notifyOnSend and self.__handlers:
            for handler in self.__handlers:
                handler.notifySend(*args, **kwargs)

    def notifyNewTopic(self, *args, **kwargs):
        if self.__notifyOnNewTopic and self.__handlers:
            for handler in self.__handlers:
                handler.notifyNewTopic(*args, **kwargs)

    def notifyDelTopic(self, *args, **kwargs):
        if self.__notifyOnDelTopic and self.__handlers:
            for handler in self.__handlers:
                handler.notifyDelTopic(*args, **kwargs)

    def notifyDeadListener(self, *args, **kwargs):
        if self.__notifyOnDeadListener and self.__handlers:
            for handler in self.__handlers:
                handler.notifyDeadListener(*args, **kwargs)

    def getFlagStates(self):
        """Return state of each notification flag, as a dict."""
        return dict(
            subscribe    = self.__notifyOnSubscribe,
            unsubscribe  = self.__notifyOnUnsubscribe,
            deadListener = self.__notifyOnDeadListener,
            sendMessage  = self.__notifyOnSend,
            newTopic     = self.__notifyOnNewTopic,
            delTopic     = self.__notifyOnDelTopic,
            )
    
    def setFlagStates(self, subscribe=None, unsubscribe=None,
        deadListener=None, sendMessage=None, newTopic=None,
        delTopic=None, all=None):
        """Set the notification flag on/off for various aspects of pubsub.
        The kwargs that are None are left at their current value. The 'all',
        if not None, is set first. E.g.

            mgr.setFlagStates(all=True, delTopic=False)

        will toggle all notifications on, but will turn off the 'delTopic'
        notification.
        """
        if all is not None:
            # ignore all other arg settings, and set all of them to true:
            numArgs = 7 # how many args in this method
            self.setFlagStates( all=None, * ((numArgs-1)*[all]) )

        if sendMessage is not None:
            self.__notifyOnSend = sendMessage
        if subscribe is not None:
            self.__notifyOnSubscribe = subscribe
        if unsubscribe is not None:
            self.__notifyOnUnsubscribe = unsubscribe

        if newTopic is not None:
            self.__notifyOnNewTopic = newTopic
        if delTopic is not None:
            self.__notifyOnDelTopic = delTopic
        if deadListener is not None:
            self.__notifyOnDeadListener = deadListener


    def __registerForAppExit(self):
        import atexit
        atexit.register(self.clearHandlers)
        self.__atExitRegistered = True



class INotificationHandler:
    """
    Defines the interface expected by pubsub for pubsub activity 
    notifications. Any instance that supports the same methods, or 
    derives from this class, will work as a notification handler
    for pubsub events (see pub.addNotificationHandler).
    """
    
    def notifySubscribe(self, pubListener, topicObj, newSub):
        """Called when a listener is subscribed to a topic.
        :param pubListener: the pubsub.core.Listener that wraps subscribed listener.
        :param topicObj: the pubsub.core.Topic object subscribed to.
        :param newSub: false if pubListener was already subscribed. """
        raise NotImplementedError
        
    def notifyUnsubscribe(self, pubListener, topicObj):
        """Called when a listener is unsubscribed from given topic.
        :param pubListener: the pubsub.core.Listener that wraps unsubscribed listener.
        :param topicObj: the pubsub.core.Topic object unsubscribed from."""
        raise NotImplementedError
        
    def notifyDeadListener(self, pubListener, topicObj):
        """Called when a listener has been garbage collected.
        :param pubListener: the pubsub.core.Listener that wraps GC'd listener.
        :param topicObj: the pubsub.core.Topic object it was subscribed to."""
        raise NotImplementedError
        
    def notifySend(self, stage, topicObj, pubListener=None):
        """Called multiple times during a sendMessage: once before message
        sending has started (pre), once for each listener about to be sent the 
        message, and once after all listeners have received the message (post).
        :param stage: 'pre', 'post', or 'loop'.
        :param topicObj: the Topic object for the message.
        :param pubListener: None for pre and post stages; for loop, the listener
            that is about to be sent the message."""
        raise NotImplementedError
    
    def notifyNewTopic(self, topicObj, description, required, argsDocs):
        """Called whenever a new topic is added to the topic tree.
        :param topicObj: the Topic object for the message.
        :param description: docstring for the topic.
        :param required: list of message data names (keys in argsDocs) that are required.
        :param argsDocs: dictionary of all message data names, with the 
        corresponding docstring. """
        raise NotImplementedError
        
    def notifyDelTopic(self, topicName):
        """Called whenever a topic is removed from topic tree.
        :param topicName: name of topic removed."""
        raise NotImplementedError


