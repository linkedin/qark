"""
Provide the Topic class.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""


from weakref import ref as weakref

from .listener import (
    Listener, 
    ListenerValidator,
)

from .topicutils import (
    ALL_TOPICS, 
    stringize, 
    tupleize, 
    validateName, 
    smartDedent,
)

from .topicexc import (
    TopicDefnError, 
    TopicNameError, 
    ExcHandlerError,
)

from .publishermixin import PublisherMixin

from .topicargspec import (
    ArgsInfo, 
    ArgSpecGiven, 
    topicArgsFromCallable, 
    SenderMissingReqdMsgDataError, 
    SenderUnknownMsgDataError, 
    MessageDataSpecError,
)

from .. import py2and3


class Topic(PublisherMixin):
    """
    Represent topics in pubsub. Contains information about a topic, 
    including topic's message data specification (MDS), the list of 
    subscribed listeners, docstring for the topic. It allows Python-like 
    access to subtopics (e.g. A.B is subtopic B of topic A).
    """

    def __init__(self, treeConfig, nameTuple, description,
        msgArgsInfo, parent=None):
        """Create a topic. Should only be called by TopicManager via its
        getOrCreateTopic() method (which gets called in several places 
        in pubsub, such as sendMessage, subscribe, and newTopic).
        
        :param treeConfig: topic tree configuration settings
        :param nameTuple: topic name, in tuple format (no dots)
        :param description: "docstring" for topic
        :param ArgsInfo msgArgsInfo: object that defines MDS for topic
        :param parent: parent of topic
        
        :raises ValueError: invalid topic name
        """
        if parent is None:
            if nameTuple != (ALL_TOPICS,):
                msg = 'Only one topic, named %s, can be root of topic tree'
                raise ValueError(msg % 'pub.ALL_TOPICS')
        else:
            validateName(nameTuple)
        self.__tupleName = nameTuple

        self.__handlingUncaughtListenerExc = False
        self._treeConfig = treeConfig
        PublisherMixin.__init__(self)

        self.__validator = None
        # Registered listeners were originally kept in a Python list; however 
        # a few methods require lookup of the Listener for the given callable, 
        # which is an O(n) operation. A set() could have been more suitable but
        # there is no way of retrieving an element from a set without iterating 
        # over the set, again an O(n) operation. A dict() is ok too. Because 
        # Listener.__eq__(callable) returns true if the Listener instance wraps
        # the given callable, and because Listener.__hash__ produces the hash 
        # value of the wrapped callable, calling dict[callable] on a 
        # dict(Listener -> Listener) mapping will be O(1) in most cases: 
        # the dict will take the callables hash, find the list of Listeners that 
        # have that hash, and then iterate over that inner list to find the 
        # Listener instance which satisfies Listener == callable, and will return
        # the Listener. 
        self.__listeners = dict()

        # specification:
        self.__description  = None
        self.setDescription(description)
        self.__msgArgs = msgArgsInfo
        if msgArgsInfo.isComplete():
            self.__finalize()
        else:
            assert not self._treeConfig.raiseOnTopicUnspecified

        # now that we know the args are fine, we can link to parent
        self.__parentTopic = None
        self.__subTopics = {}
        if parent is None:
            assert self.hasMDS()
        else:
            self.__parentTopic = weakref(parent)
            assert self.__msgArgs.parentAI() is parent._getListenerSpec()
            parent.__adoptSubtopic( self )

    def setDescription(self, desc):
        """Set the 'docstring' of topic"""
        self.__description = desc

    def getDescription(self):
        """Return the 'docstring' of topic"""
        if self.__description is None:
            return None
        return smartDedent(self.__description)

    def setMsgArgSpec(self, argsDocs, required=()):
        """Specify the message data for topic messages.
        :param argsDocs: a dictionary of keyword names (message data name) and data 'docstring'; cannot be None
        :param required: a list of those keyword names, appearing in argsDocs, 
        which are required (all others are assumed optional)
            
        Can only be called if this info has not been already set at construction 
        or in a previous call. 
        :raise RuntimeError: if MDS already set at construction or previous call."""
        assert self.__parentTopic is not None # for root of tree, this method never called!
        if argsDocs is None:
            raise ValueError('Cannot set listener spec to None')

        if self.__msgArgs is None or not self.__msgArgs.isComplete():
            try:
                specGiven = ArgSpecGiven(argsDocs, required)
                self.__msgArgs = ArgsInfo(self.__tupleName, specGiven,
                    self.__parentTopic()._getListenerSpec())
            except MessageDataSpecError:
                # discard the lower part of the stack trace
                exc = py2and3.getexcobj()
                raise exc
            self.__finalize()

        else:
            raise RuntimeError('Not allowed to call this: msg spec already set!')

    def getArgs(self):
        """Returns a pair (reqdArgs, optArgs) where reqdArgs is tuple
        of names of required message arguments, optArgs is tuple
        of names for optional arguments. If topic args not specified
        yet, returns (None, None)."""
        sendable = self.__msgArgs.isComplete()
        assert sendable == self.hasMDS()
        if sendable:
            return (self.__msgArgs.allRequired ,
                    self.__msgArgs.allOptional)
        return None, None

    def getArgDescriptions(self):
        """Get a map of keyword names to docstrings: documents each MDS element. """
        return self.__msgArgs.getArgsDocs()

    def setArgDescriptions(self, **docs):
        """Set the docstring for each MDS datum."""
        self.__msgArgs.setArgsDocs(docs)

    def hasMDS(self):
        """Return true if this topic has a message data specification (MDS)."""
        return self.__validator is not None

    def filterMsgArgs(self, msgKwargs, check=False):
        """Get the MDS docstrings for each of the spedified kwargs."""
        filteredArgs = self.__msgArgs.filterArgs(msgKwargs)
        # if no check of args yet, do it now:
        if check:
            self.__msgArgs.check(filteredArgs)
        return filteredArgs

    def isAll(self):
        """Returns true if this topic is the 'all topics' topic. All root
        topics behave as though they are child of that topic. """
        return self.__tupleName == (ALL_TOPICS,)

    def isRoot(self):
        """Returns true if this is a "root" topic, false otherwise. A
        root topic is a topic whose name contains no dots and which
        has pub.ALL_TOPICS as parent."""
        parent = self.getParent()
        if parent:
            return parent.isAll()
        assert self.isAll()
        return False

    def getName(self):
        """Return dotted form of full topic name"""
        return stringize(self.__tupleName)

    def getNameTuple(self):
        """Return tuple form of full topic name"""
        return self.__tupleName

    def getNodeName(self):
        """Return the last part of the topic name (has no dots)"""
        name = self.__tupleName[-1]
        return name

    def getParent(self):
        """Get Topic object that is parent of self (i.e. self is a subtopic
        of parent). Return none if self is the "all topics" topic."""
        if self.__parentTopic is None:
            return None
        return self.__parentTopic()

    def hasSubtopic(self, name=None):
        """Return true only if name is a subtopic of self. If name not
        specified, return true only if self has at least one subtopic."""
        if name is None:
            return len(self.__subTopics) > 0

        return name in self.__subTopics

    def getSubtopic(self, relName):
        """Get the specified subtopic object. The relName can be a valid
        subtopic name, a dotted-name string, or a tuple. """
        if not relName:
            raise ValueError("getSubtopic() arg can't be empty")
        topicTuple = tupleize(relName)
        assert topicTuple

        topicObj = self
        for topicName in topicTuple:
            child = topicObj.__subTopics.get(topicName)
            if child is None:
                msg = 'Topic "%s" doesn\'t have "%s" as subtopic' % (topicObj.getName(), topicName)
                raise TopicNameError(relName, msg)
            topicObj = child

        return topicObj

    def getSubtopics(self):
        """Get a list of Topic instances that are subtopics of self."""
        return py2and3.values(self.__subTopics)

    def getNumListeners(self):
        """Return number of listeners currently subscribed to topic. This is
        different from number of listeners that will get notified since more
        general topics up the topic tree may have listeners."""
        return len(self.__listeners)

    def hasListener(self, listener):
        """Return true if listener is subscribed to this topic."""
        return listener in self.__listeners

    def hasListeners(self):
        """Return true if there are any listeners subscribed to
        this topic, false otherwise."""
        return bool(self.__listeners)

    def getListeners(self):
        """Get a copy of list of listeners subscribed to this topic. Safe to iterate over while listeners
        get un/subscribed from this topics (such as while sending a message)."""
        return py2and3.keys(self.__listeners)

    def getListenersIter(self):
        """Get an iterator over listeners subscribed to this topic. Do not use if listeners can be
        un/subscribed while iterating. """
        return py2and3.iterkeys(self.__listeners)

    def validate(self, listener):
        """Checks whether listener could be subscribed to this topic:
        if yes, just returns; if not, raises ListenerMismatchError.
        Note that method raises TopicDefnError if self not
        hasMDS()."""
        if not self.hasMDS():
            raise TopicDefnError(self.__tupleName)
        return self.__validator.validate(listener)

    def isValid(self, listener):
        """Return True only if listener could be subscribed to this topic,
        otherwise returns False. Note that method raises TopicDefnError
        if self not hasMDS()."""
        if not self.hasMDS():
            raise TopicDefnError(self.__tupleName)
        return self.__validator.isValid(listener)

    def subscribe(self, listener):
        """Subscribe listener to this topic. Returns a pair
        (pub.Listener, success). The success is true only if listener
        was not already subscribed and is now subscribed. """
        if listener in self.__listeners:
            assert self.hasMDS()
            subdLisnr, newSub = self.__listeners[listener], False

        else:
            if self.__validator is None:
                args, reqd = topicArgsFromCallable(listener)
                self.setMsgArgSpec(args, reqd)
            argsInfo = self.__validator.validate(listener)
            weakListener = Listener(
                listener, argsInfo, onDead=self.__onDeadListener)
            self.__listeners[weakListener] = weakListener
            subdLisnr, newSub = weakListener, True

        # notify of subscription
        self._treeConfig.notificationMgr.notifySubscribe(subdLisnr, self, newSub)

        return subdLisnr, newSub

    def unsubscribe(self, listener):
        """Unsubscribe the specified listener from this topic. Returns
        the pub.Listener object associated with the listener that was
        unsubscribed, or None if the specified listener was not
        subscribed to this topic.  Note that this method calls
        ``notifyUnsubscribe(listener, self)`` on all registered notification
        handlers (see pub.addNotificationHandler)."""
        unsubdLisnr = self.__listeners.pop(listener, None)
        if unsubdLisnr is None: 
            return None

        unsubdLisnr._unlinkFromTopic_()
        assert listener == unsubdLisnr.getCallable()

        # notify of unsubscription
        self._treeConfig.notificationMgr.notifyUnsubscribe(unsubdLisnr, self)

        return unsubdLisnr

    def unsubscribeAllListeners(self, filter=None):
        """Clears list of subscribed listeners. If filter is given, it must
        be a function that takes a listener and returns true if the listener
        should be unsubscribed. Returns the list of Listener for listeners 
        that were unsubscribed."""
        unsubd = []
        if filter is None:
            for listener in self.__listeners:
                listener._unlinkFromTopic_()
            unsubd = py2and3.keys(self.__listeners)
            self.__listeners = {}
        else:
            unsubd = []
            for listener in py2and3.keys(self.__listeners):
                if filter(listener):
                    unsubd.append(listener)
                    listener._unlinkFromTopic_()
                    del self.__listeners[listener]

        # send notification regarding all listeners actually unsubscribed
        notificationMgr = self._treeConfig.notificationMgr
        for unsubdLisnr in unsubd:
            notificationMgr.notifyUnsubscribe(unsubdLisnr, self)

        return unsubd

    #############################################################
    #
    # Impementation
    #
    #############################################################

    def _getListenerSpec(self):
        """Only to be called by pubsub package"""
        return self.__msgArgs

    def _publish(self, data):
        """This sends message to listeners of parent topics as well.
        If an exception is raised in a listener, the publish is
        aborted, except if there is a handler (see
        pub.setListenerExcHandler)."""
        self._treeConfig.notificationMgr.notifySend('pre', self)

        # send to ourself
        iterState = self._mix_prePublish(data)
        self.__sendMessage(data, self, iterState)

        # send up the chain
        topicObj = self.getParent()
        while topicObj is not None:
            if topicObj.hasListeners():
                iterState = self._mix_prePublish(data, topicObj, iterState)
                self.__sendMessage(data, topicObj, iterState)

            # done for this topic, continue up branch to parent towards root
            topicObj = topicObj.getParent()

        self._treeConfig.notificationMgr.notifySend('post', self)

    def __sendMessage(self, data, topicObj, iterState):
        # now send message data to each listener for current topic;
        # use list of listeners rather than iterator, so that if listeners added/removed during
        # send loop, no runtime exception:
        for listener in topicObj.getListeners():
            try:
                self._treeConfig.notificationMgr.notifySend('in', topicObj, pubListener=listener)
                self._mix_callListener(listener, data, iterState)

            except Exception:
                # if exception handling is on, handle, otherwise re-raise
                handler = self._treeConfig.listenerExcHandler
                if handler is None or self.__handlingUncaughtListenerExc:
                    raise

                # try handling the exception so we can continue the send:
                try:
                    self.__handlingUncaughtListenerExc = True
                    handler( listener.name(), topicObj )
                    self.__handlingUncaughtListenerExc = False
                except Exception:
                    exc = py2and3.getexcobj()
                    #print 'exception raised', exc
                    self.__handlingUncaughtListenerExc = False
                    raise ExcHandlerError(listener.name(), topicObj, exc)

    def __finalize(self):
        """Finalize the topic specification, which currently means
        creating the listener validator for this topic. This allows 
        calls to subscribe() to validate that listener adheres to 
        topic's message data specification (MDS)."""
        assert self.__msgArgs.isComplete()
        assert not self.hasMDS()

        # must make sure can adopt a validator
        required = self.__msgArgs.allRequired
        optional = self.__msgArgs.allOptional
        self.__validator = ListenerValidator(required, list(optional) )
        assert not self.__listeners

    def _undefineSelf_(self, topicsMap):
        """Called by topic manager when deleting a topic."""
        if self.__parentTopic is not None:
            self.__parentTopic().__abandonSubtopic(self.__tupleName[-1])
        self.__undefineBranch(topicsMap)

    def __undefineBranch(self, topicsMap):
        """Unsubscribe all our listeners, remove all subtopics from self,
        then detach from parent. Parent is not notified, because method
        assumes it has been called by parent"""
        #print 'Remove %s listeners (%s)' % (self.getName(), self.getNumListeners())
        self.unsubscribeAllListeners()
        self.__parentTopic = None

        for subName, subObj in py2and3.iteritems(self.__subTopics):
            assert isinstance(subObj, Topic)
            #print 'Unlinking %s from parent' % subObj.getName()
            subObj.__undefineBranch(topicsMap)

        self.__subTopics = {}
        del topicsMap[self.getName()]

    def __adoptSubtopic(self, topicObj):
        """Add topicObj as child topic."""
        assert topicObj.__parentTopic() is self
        attrName = topicObj.getNodeName()
        self.__subTopics[attrName] = topicObj

    def __abandonSubtopic(self, name):
        """The given subtopic becomes orphan (no parent)."""
        topicObj = self.__subTopics.pop(name)
        assert topicObj.__parentTopic() is self

    def __onDeadListener(self, weakListener):
        """One of our subscribed listeners has died, so remove it and notify"""
        pubListener = self.__listeners.pop(weakListener)
        # notify:
        self._treeConfig.notificationMgr.notifyDeadListener(pubListener, self)

    def __str__(self):
        return "%s(%s)" % (self.getName(), self.getNumListeners())


