"""
Code related to the concept of topic tree and its management: creating 
and removing topics, getting info about a particular topic, etc. 

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

__all__ = [
    'TopicManager',
    'TopicNameError',
    'TopicDefnError',
    ]


from .callables import getID

from .topicutils import (
    ALL_TOPICS, 
    tupleize, 
    stringize,
)

from .topicexc import (
    TopicNameError, 
    TopicDefnError,
)

from .topicargspec import (
    ArgSpecGiven,
    ArgsInfo,
    topicArgsFromCallable,
)

from .topicobj import (
    Topic, 
)

from .treeconfig import TreeConfig
from .topicdefnprovider import ITopicDefnProvider
from .topicmgrimpl import getRootTopicSpec

from .. import py2and3


# ---------------------------------------------------------

ARGS_SPEC_ALL     = ArgSpecGiven.SPEC_GIVEN_ALL
ARGS_SPEC_NONE    = ArgSpecGiven.SPEC_GIVEN_NONE


# ---------------------------------------------------------

class TopicManager:
    """
    Manages the registry of all topics and creation/deletion
    of topics. 

    Note that any method that accepts a topic name can accept it in the 
    'dotted' format such as ``'a.b.c.'`` or in tuple format such as 
    ``('a', 'b', 'c')``. Any such method will raise a ValueError
    if name not valid (empty, invalid characters, etc). 
    """
    
    # Allowed return values for isTopicSpecified()
    TOPIC_SPEC_NOT_SPECIFIED   = 0 # false
    TOPIC_SPEC_ALREADY_CREATED = 1 # all other values equate to "true" but different reason
    TOPIC_SPEC_ALREADY_DEFINED = 2


    def __init__(self, treeConfig=None):
        """The optional treeConfig is an instance of TreeConfig, used to
        configure the topic tree such as notification settings, etc. A
        default config is created if not given. This method should only be 
        called by an instance of Publisher (see Publisher.getTopicManager())."""
        self.__allTopics = None # root of topic tree
        self._topicsMap = {} # registry of all topics
        self.__treeConfig = treeConfig or TreeConfig()
        self.__defnProvider = _MasterTopicDefnProvider(self.__treeConfig)

        # define root of all topics
        assert self.__allTopics is None
        argsDocs, reqdArgs = getRootTopicSpec()
        desc = 'Root of all topics'
        specGiven = ArgSpecGiven(argsDocs, reqdArgs)
        self.__allTopics = self.__createTopic((ALL_TOPICS,), desc, specGiven=specGiven)

    def getRootAllTopics(self):
        """Get the topic that is parent of all root (ie top-level) topics,
        for default TopicManager instance created when this module is imported. 
        Some notes:

        - "root of all topics" topic satisfies isAll()==True, isRoot()==False,
          getParent() is None;
        - all root-level topics satisfy isAll()==False, isRoot()==True, and
          getParent() is getDefaultTopicTreeRoot();
        - all other topics satisfy neither. """
        return self.__allTopics
    
    def addDefnProvider(self, providerOrSource, format=None):
        """Register a topic definition provider. After this method is called, whenever a topic must be created,
        the first definition provider that has a definition
        for the required topic is used to instantiate the topic. 
        
        If providerOrSource is an instance of ITopicDefnProvider, register 
        it as a provider of topic definitions. Otherwise, register a new 
        instance of TopicDefnProvider(providerOrSource, format). In that case, 
        if format is not given, it defaults to TOPIC_TREE_FROM_MODULE. Either
        way, returns the instance of ITopicDefnProvider registered.
        """
        if isinstance(providerOrSource, ITopicDefnProvider):
            provider = providerOrSource
        else:
            from .topicdefnprovider import (TopicDefnProvider, TOPIC_TREE_FROM_MODULE)
            source = providerOrSource
            provider = TopicDefnProvider(source, format or TOPIC_TREE_FROM_MODULE)
        self.__defnProvider.addProvider(provider)
        return provider
    
    def clearDefnProviders(self):
        """Remove all registered topic definition providers"""
        self.__defnProvider.clear()

    def getNumDefnProviders(self):
        """Get how many topic definitions providers are registered."""
        return self.__defnProvider.getNumProviders()

    def getTopic(self, name, okIfNone=False):
        """Get the Topic instance for the given topic name. By default, raises
        an TopicNameError exception if a topic with given name doesn't exist. If
        okIfNone=True, returns None instead of raising an exception."""
        topicNameDotted = stringize(name)
        #if not name:
        #    raise TopicNameError(name, 'Empty topic name not allowed')
        obj = self._topicsMap.get(topicNameDotted, None)
        if obj is not None:
            return obj

        if okIfNone:
            return None

        # NOT FOUND! Determine what problem is and raise accordingly:
        # find the closest parent up chain that does exists:
        parentObj, subtopicNames = self.__getClosestParent(topicNameDotted)
        assert subtopicNames
        
        subtopicName = subtopicNames[0]
        if parentObj is self.__allTopics:
            raise TopicNameError(name, 'Root topic "%s" doesn\'t exist' % subtopicName)

        msg = 'Topic "%s" doesn\'t have "%s" as subtopic' % (parentObj.getName(), subtopicName)
        raise TopicNameError(name, msg)

    def newTopic(self, _name, _desc, _required=(), **_argDocs):
        """Deprecated legacy method.
        If topic _name already exists, just returns it and does nothing else.
        Otherwise, uses getOrCreateTopic() to create it, then sets its
        description (_desc) and its message data specification (_argDocs
        and _required). Replaced by getOrCreateTopic()."""
        topic = self.getTopic(_name, True)
        if topic is None:
            topic = self.getOrCreateTopic(_name)
            topic.setDescription(_desc)
            topic.setMsgArgSpec(_argDocs, _required)
        return topic

    def getOrCreateTopic(self, name, protoListener=None):
        """Get the Topic instance for topic of given name, creating it
        (and any of its missing parent topics) as necessary. Pubsub 
        functions such as subscribe() use this to obtain the Topic object
        corresponding to a topic name. 
        
        The name can be in dotted or string format (``'a.b.'`` or ``('a','b')``). 
        
        This method always attempts to return a "complete" topic, i.e. one 
        with a Message Data Specification (MDS). So if the topic does not have 
        an MDS, it attempts to add it. It first tries to find an MDS 
        from a TopicDefnProvider (see addDefnProvider()). If none is available, 
        it attempts to set it from protoListener, if it has been given. If not, 
        the topic has no MDS. 
        
        Once a topic's MDS has been set, it is never again changed or accessed
        by this method. 
                
        Examples::
            
            # assume no topics exist
            # but a topic definition provider has been added via 
            # pub.addTopicDefnProvider() and has definition for topics 'a' and 'a.b'
            
            # creates topic a and a.b; both will have MDS from the defn provider:
            t1 = topicMgr.getOrCreateTopic('a.b')
            t2 = topicMgr.getOrCreateTopic('a.b')
            assert(t1 is t2)
            assert(t1.getParent().getName() == 'a')
            
            def proto(req1, optarg1=None): pass
            # creates topic c.d with MDS based on proto; creates c without an MDS
            # since no proto for it, nor defn provider:
            t1 = topicMgr.getOrCreateTopic('c.d', proto)
            
        The MDS can also be defined via a call to subscribe(listener, topicName), 
        which indirectly calls getOrCreateTopic(topicName, listener).
        """
        obj = self.getTopic(name, okIfNone=True)
        if obj:
            # if object is not sendable but a proto listener was given,
            # update its specification so that it is sendable
            if (protoListener is not None) and not obj.hasMDS():
                allArgsDocs, required = topicArgsFromCallable(protoListener)
                obj.setMsgArgSpec(allArgsDocs, required)
            return obj

        # create missing parents
        nameTuple = tupleize(name)
        parentObj = self.__createParentTopics(nameTuple)

        # now the final topic object, args from listener if provided
        desc, specGiven = self.__defnProvider.getDefn(nameTuple)
        # POLICY: protoListener is used only if no definition available
        if specGiven is None:
            if protoListener is None:
                desc = 'UNDOCUMENTED: created without spec'
            else:
                allArgsDocs, required = topicArgsFromCallable(protoListener)
                specGiven = ArgSpecGiven(allArgsDocs, required)
                desc = 'UNDOCUMENTED: created from protoListener "%s" in module %s' % getID(protoListener)

        return self.__createTopic(nameTuple, desc, parent = parentObj, specGiven = specGiven)

    def isTopicInUse(self, name):
        """Determine if topic 'name' is in use. True if a Topic object exists
        for topic name (i.e. message has already been sent for that topic, or a 
        least one listener subscribed), false otherwise. Note: a topic may be in use 
        but not have a definition (MDS and docstring); or a topic may have a
        definition, but not be in use."""
        return self.getTopic(name, okIfNone=True) is not None
        
    def hasTopicDefinition(self, name):
        """Determine if there is a definition avaiable for topic 'name'. Return
        true if there is, false otherwise. Note: a topic may have a
        definition without being in use, and vice versa."""
        # in already existing Topic object:
        alreadyCreated = self.getTopic(name, okIfNone=True)
        if alreadyCreated is not None and alreadyCreated.hasMDS():
            return True
            
        # from provider?
        nameTuple = tupleize(name)
        if self.__defnProvider.isDefined(nameTuple):
            return True

        return False

    def checkAllTopicsHaveMDS(self):
        """Check that all topics that have been created for their MDS.
        Raise a TopicDefnError if one is found that does not have one."""
        for topic in py2and3.itervalues(self._topicsMap):
            if not topic.hasMDS():
                raise TopicDefnError(topic.getNameTuple())

    def delTopic(self, name):
        """Delete the named topic, including all sub-topics. Returns False
        if topic does not exist; True otherwise. Also unsubscribe any listeners 
        of topic and all subtopics. """
        # find from which parent the topic object should be removed
        dottedName = stringize(name)
        try:
            #obj = weakref( self._topicsMap[dottedName] )
            obj = self._topicsMap[dottedName]
        except KeyError:
            return False

        #assert obj().getName() == dottedName
        assert obj.getName() == dottedName
        # notification must be before deletion in case
        self.__treeConfig.notificationMgr.notifyDelTopic(dottedName)

        #obj()._undefineSelf_(self._topicsMap)
        obj._undefineSelf_(self._topicsMap)
        #assert obj() is None

        return True

    def getTopicsSubscribed(self, listener):
        """Get the list of Topic objects that have given listener
        subscribed. Note: the listener can also get messages from any 
        sub-topic of returned list."""
        assocTopics = []
        for topicObj in py2and3.itervalues(self._topicsMap):
            if topicObj.hasListener(listener):
                assocTopics.append(topicObj)
        return assocTopics        
        
    def __getClosestParent(self, topicNameDotted):
        """Returns a pair, (closest parent, tuple path from parent). The
        first item is the closest parent Topic that exists.
        The second one is the list of topic name elements that have to be 
        created to create the given topic.

        So if topicNameDotted = A.B.C.D, but only A.B exists (A.B.C and
        A.B.C.D not created yet), then return is (A.B, ['C','D']).
        Note that if none of the branch exists (not even A), then return
        will be [root topic, ['A',B','C','D']). Note also that if A.B.C
        exists, the return will be (A.B.C, ['D']) regardless of whether
        A.B.C.D exists. """
        subtopicNames = []
        headTail = topicNameDotted.rsplit('.', 1)
        while len(headTail) > 1:
            parentName = headTail[0]
            subtopicNames.insert( 0, headTail[1] )
            obj = self._topicsMap.get( parentName, None )
            if obj is not None:
                return obj, subtopicNames
            
            headTail = parentName.rsplit('.', 1)
            
        subtopicNames.insert( 0, headTail[0] )
        return self.__allTopics, subtopicNames
    
    def __createParentTopics(self, topicName):
        """This will find which parents need to be created such that
        topicName can be created (but doesn't create given topic),
        and creates them. Returns the parent object."""
        assert self.getTopic(topicName, okIfNone=True) is None
        parentObj, subtopicNames = self.__getClosestParent(stringize(topicName))
        
        # will create subtopics of parentObj one by one from subtopicNames
        if parentObj is self.__allTopics:
            nextTopicNameList = []
        else:
            nextTopicNameList = list(parentObj.getNameTuple())
        for name in subtopicNames[:-1]:
            nextTopicNameList.append(name)
            desc, specGiven = self.__defnProvider.getDefn( tuple(nextTopicNameList) )
            if desc is None:
                desc = 'UNDOCUMENTED: created as parent without specification'
            parentObj = self.__createTopic( tuple(nextTopicNameList),
                desc, specGiven = specGiven,  parent = parentObj)
            
        return parentObj
    
    def __createTopic(self, nameTuple, desc, specGiven, parent=None):
        """Actual topic creation step. Adds new Topic instance to topic map,
        and sends notification message (see ``Publisher.addNotificationMgr()``) 
        regarding topic creation."""
        if specGiven is None:
            specGiven = ArgSpecGiven()
        parentAI = None
        if parent:
            parentAI = parent._getListenerSpec()
        argsInfo = ArgsInfo(nameTuple, specGiven, parentAI)
        if (self.__treeConfig.raiseOnTopicUnspecified
            and not argsInfo.isComplete()):
            raise TopicDefnError(nameTuple)

        newTopicObj = Topic(self.__treeConfig, nameTuple, desc,
                            argsInfo, parent = parent)
        # sanity checks:
        assert newTopicObj.getName() not in self._topicsMap
        if parent is self.__allTopics:
            assert len( newTopicObj.getNameTuple() ) == 1
        else:
            assert parent.getNameTuple() == newTopicObj.getNameTuple()[:-1]
        assert nameTuple == newTopicObj.getNameTuple()

        # store new object and notify of creation
        self._topicsMap[ newTopicObj.getName() ] = newTopicObj
        self.__treeConfig.notificationMgr.notifyNewTopic(
            newTopicObj, desc, specGiven.reqdArgs, specGiven.argsDocs)
        
        return newTopicObj


def validateNameHierarchy(topicTuple):
    """Check that names in topicTuple are valid: no spaces, not empty.
    Raise ValueError if fails check. E.g. ('',) and ('a',' ') would
    both fail, but ('a','b') would be ok. """
    if not topicTuple:
        topicName = stringize(topicTuple)
        errMsg = 'empty topic name'
        raise TopicNameError(topicName, errMsg)
    
    for indx, topic in enumerate(topicTuple):
        errMsg = None
        if topic is None:
            topicName = list(topicTuple)
            topicName[indx] = 'None'
            errMsg = 'None at level #%s'

        elif not topic:
            topicName = stringize(topicTuple)
            errMsg = 'empty element at level #%s'

        elif topic.isspace():
            topicName = stringize(topicTuple)
            errMsg = 'blank element at level #%s'

        if errMsg:
            raise TopicNameError(topicName, errMsg % indx)


class _MasterTopicDefnProvider:
    """
    Stores a list of topic definition providers. When queried for a topic
    definition, queries each provider (registered via addProvider()) and
    returns the first complete definition provided, or (None,None).

    The providers must follow the ITopicDefnProvider protocol.
    """

    def __init__(self, treeConfig):
        self.__providers = []
        self.__treeConfig = treeConfig

    def addProvider(self, provider):
        """Add given provider IF not already added. """
        assert(isinstance(provider, ITopicDefnProvider))
        if provider not in self.__providers:
            self.__providers.append(provider)

    def clear(self):
        """Remove all providers added."""
        self.__providers = []

    def getNumProviders(self):
        """Return how many providers added."""
        return len(self.__providers)

    def getDefn(self, topicNameTuple):
        """Returns a pair (docstring, MDS) for the topic. The first item is
        a string containing the topic's "docstring", i.e. a description string 
        for the topic, or None if no docstring available for the topic. The 
        second item is None or an instance of ArgSpecGiven specifying the
        required and optional message data for listeners of this topic. """
        desc, defn = None, None
        for provider in self.__providers:
            tmpDesc, tmpDefn = provider.getDefn(topicNameTuple)
            if (tmpDesc is not None) and (tmpDefn is not None):
                assert tmpDefn.isComplete()
                desc, defn = tmpDesc, tmpDefn
                break

        return desc, defn

    def isDefined(self, topicNameTuple):
        """Returns True only if a complete definition exists, ie topic
        has a description and a complete message data specification (MDS)."""
        desc, defn = self.getDefn(topicNameTuple)
        if desc is None or defn is None:
            return False
        if defn.isComplete():
            return True
        return False


