"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""


import os, re, inspect
from textwrap import TextWrapper, dedent

from .. import (
    policies, 
    py2and3
)
from .topicargspec import (
    topicArgsFromCallable, 
    ArgSpecGiven
)
from .topictreetraverser import TopicTreeTraverser
from .topicexc import UnrecognizedSourceFormatError


class ITopicDefnProvider:
    """
    All topic definition providers added via pub.addTopicDefnProvider()
    must have this interface. Derived classes must override the getDefn(), 
    getTreeDoc() and topicNames() methods. 
    """
    
    def getDefn(self, topicNameTuple):
        """Must return a pair (string, ArgSpecGiven) for given topic.
        The first item is a description for topic, the second item 
        contains the message data specification (MDS). Note topic name
        is in tuple format ('a', 'b', 'c') rather than 'a.b.c'. """
        msg = 'Must return (string, ArgSpecGiven), or (None, None)'
        raise NotImplementedError(msg)

    def topicNames(self):
        """Return an iterator over topic names available from this provider.
        Note that the topic names should be in tuple rather than dotted-string
        format so as to be compatible with getDefn()."""
        msg = 'Must return a list of topic names available from this provider'
        raise NotImplementedError(msg)

    def getTreeDoc(self):
        """Get the docstring for the topic tree."""
        msg = 'Must return documentation string for root topic (tree)'
        raise NotImplementedError(msg)

    def __iter__(self):
        """Same as self.topicNames(), do NOT override."""
        return self.topicNames()


# name of method in class name assumed to represent topic's listener signature
# which will get checked against topic's Message Data Specification (MDS)
SPEC_METHOD_NAME = 'msgDataSpec'


class ITopicDefnDeserializer:
    """
    Interface class for all topic definition de-serializers that can be 
    accepted by TopicDefnProvider. A deserializer 
    creates a topic tree from something such as file, module, or string. 
    """

    class TopicDefn:
        """Encapsulate date for a topic definition. Used by
        getNextTopic()."""

        def __init__(self, nameTuple, description, argsDocs, required):
            self.nameTuple = nameTuple
            self.description = description
            self.argsDocs = argsDocs
            self.required = required

        def isComplete(self):
            return (self.description is not None) and (self.argsDocs is not None)

    def getTreeDoc(self):
        """Get the docstring for the topic tree."""
        raise NotImplementedError

    def getNextTopic(self):
        """Get the next topic definition available from the data. The return
        must be an instance of TopicDefn. Must return None when no topics 
        are left."""
        raise NotImplementedError

    def doneIter(self):
        """Called automatically by TopicDefnProvider once
        it considers the iteration completed. Override this only if 
        deserializer needs to take action, such as closing a file."""
        pass

    def resetIter(self):
        """Called by the TopicDefnProvider if it needs to
        restart the topic iteration. Override this only if special action needed,
        such as resetting a file pointer to beginning of file."""
        pass


class TopicDefnDeserialClass(ITopicDefnDeserializer):
    """
    Convert a nested class tree as a topic definition tree. Format: the class 
    name is the topic name, its doc string is its description. The topic's 
    message data specification is determined by inspecting a class method called 
    the same as SPEC_METHOD_NAME. The doc string of that method is parsed to 
    extract the description for each message data.
     """

    def __init__(self, pyClassObj=None):
        """If pyClassObj is given, it is an object that contains nested
        classes defining root topics; the root topics contain nested
        classes defining subtopics; etc."""
        self.__rootTopics = []
        self.__iterStarted = False
        self.__nextTopic = iter(self.__rootTopics)
        self.__rootDoc = None

        if pyClassObj is not None:
            self.__rootDoc = pyClassObj.__doc__
            topicClasses = self.__getTopicClasses(pyClassObj)
            for topicName, pyClassObj in topicClasses:
                self.__addDefnFromClassObj(pyClassObj)

    def getTreeDoc(self):
        return self.__rootDoc

    def getNextTopic(self):
        self.__iterStarted = True
        try:
            topicNameTuple, topicClassObj = py2and3.nextiter(self.__nextTopic)
        except StopIteration:
            return None

        # ok get the info from class
        if hasattr(topicClassObj, SPEC_METHOD_NAME):
            protoListener = getattr(topicClassObj, SPEC_METHOD_NAME)
            argsDocs, required = topicArgsFromCallable(protoListener)
            if protoListener.__doc__:
                self.__setArgsDocsFromProtoDocs(argsDocs, protoListener.__doc__)
        else:
            # assume definition is implicitly that listener has no args
            argsDocs = {}
            required = ()
        desc = None
        if topicClassObj.__doc__:
            desc = dedent(topicClassObj.__doc__)
        return self.TopicDefn(topicNameTuple, desc, argsDocs, required)

    def resetIter(self):
        self.__iterStarted = False
        self.__nextTopic = iter(self.__rootTopics)

    def getDefinedTopics(self):
        return [nt for (nt, defn) in self.__rootTopics]

    def __addDefnFromClassObj(self, pyClassObj):
        """Extract a topic definition from a Python class: topic name,
        docstring, and MDS, and docstring for each message data. 
        The class name is the topic name, assumed to be a root topic, and
        descends recursively into nested classes to define subtopic etc. """
        if self.__iterStarted:
            raise RuntimeError('addDefnFromClassObj must be called before iteration started!')

        parentNameTuple = (pyClassObj.__name__, )
        if pyClassObj.__doc__ is not None:
            self.__rootTopics.append( (parentNameTuple, pyClassObj) )
            if self.__rootDoc is None:
                self.__rootDoc = pyClassObj.__doc__
        self.__findTopics(pyClassObj, parentNameTuple)
        # iterator is now out of sync, so reset it; obviously this would
        # screw up getNextTopic which is why we had to test for self.__iterStarted
        self.__nextTopic = iter(self.__rootTopics)

    def __findTopics(self, pyClassObj, parentNameTuple):
        assert not self.__iterStarted
        assert parentNameTuple
        assert pyClassObj.__name__ == parentNameTuple[-1]

        topicClasses = self.__getTopicClasses(pyClassObj, parentNameTuple)
        pyClassObj._topicNameStr = '.'.join(parentNameTuple)

        # make sure to update rootTopics BEFORE we recurse, so that toplevel
        # topics come first in the list
        for parentNameTuple2, topicClassObj in topicClasses:
            # we only keep track of topics that are documented, so that
            # multiple providers can co-exist without having to duplicate
            # information
            if topicClassObj.__doc__ is not None:
                self.__rootTopics.append( (parentNameTuple2, topicClassObj) )
            # now can find its subtopics
            self.__findTopics(topicClassObj, parentNameTuple2)

    def __getTopicClasses(self, pyClassObj, parentNameTuple=()):
        """Returns a list of pairs, (topicNameTuple, memberClassObj)"""
        memberNames = dir(pyClassObj)
        topicClasses = []
        for memberName in memberNames:
            if memberName.startswith('_'): 
                continue # ignore special and non-public methods
            member = getattr(pyClassObj, memberName)
            if inspect.isclass( member ):
                topicNameTuple = parentNameTuple + (memberName,)
                topicClasses.append( (topicNameTuple, member) )
        return topicClasses

    def __setArgsDocsFromProtoDocs(self, argsDocs, protoDocs):
        PAT_ITEM_STR = r'\A-\s*' # hyphen and any number of blanks
        PAT_ARG_NAME = r'(?P<argName>\w*)'
        PAT_DOC_STR  = r'(?P<doc1>.*)'
        PAT_BLANK    = r'\s*'
        PAT_ITEM_SEP = r':'
        argNamePat = re.compile(
            PAT_ITEM_STR + PAT_ARG_NAME + PAT_BLANK + PAT_ITEM_SEP
            + PAT_BLANK + PAT_DOC_STR)
        protoDocs = dedent(protoDocs)
        lines = protoDocs.splitlines()
        argName = None
        namesFound = []
        for line in lines:
            match = argNamePat.match(line)
            if match:
                argName = match.group('argName')
                namesFound.append(argName)
                argsDocs[argName] = [match.group('doc1') ]
            elif argName:
                argsDocs[argName].append(line)

        for name in namesFound:
            argsDocs[name] = '\n'.join( argsDocs[name] )


class TopicDefnDeserialModule(ITopicDefnDeserializer):
    """
    Deserialize a module containing Python source code defining a topic tree.
    This loads the module and gives it to an instance of TopicDefnDeserialClass.
    """

    def __init__(self, moduleName, searchPath=None):
        """Load the given named module, searched for in searchPath or, if not
        specified, in sys.path. Give it to a TopicDefnDeserialClass."""
        from . import imp2
        module = imp2.load_module(moduleName, searchPath)
        self.__classDeserial = TopicDefnDeserialClass(module)

    def getTreeDoc(self):
        return self.__classDeserial.getTreeDoc()
    
    def getNextTopic(self):
        return self.__classDeserial.getNextTopic()

    def doneIter(self):
        self.__classDeserial.doneIter()

    def resetIter(self):
        self.__classDeserial.resetIter()

    def getDefinedTopics(self):
        return self.__classDeserial.getDefinedTopics()


class TopicDefnDeserialString(ITopicDefnDeserializer):
    """
    Deserialize a string containing Python source code defining a topic tree.
    The string has the same format as expected by TopicDefnDeserialModule.
    """

    def __init__(self, source):
        """This just saves the string into a temporary file created in
        os.getcwd(), and the rest is delegated to TopicDefnDeserialModule. 
        The temporary file (module -- as well as its byte-compiled 
        version) will be deleted when the doneIter() method is called."""

        def createTmpModule():
            moduleNamePre = 'tmp_export_topics_'
            import os, tempfile
            creationDir = os.getcwd()
            fileID, path = tempfile.mkstemp('.py', moduleNamePre, dir=creationDir)
            stringFile = os.fdopen(fileID, 'w')
            stringFile.write( dedent(source) )
            stringFile.close()
            return path, [creationDir]

        self.__filename, searchPath = createTmpModule()
        moduleName = os.path.splitext( os.path.basename(self.__filename) )[0]
        self.__modDeserial = TopicDefnDeserialModule(moduleName, searchPath)

    def getTreeDoc(self):
        return self.__modDeserial.getTreeDoc()

    def getNextTopic(self):
        return self.__modDeserial.getNextTopic()

    def doneIter(self):
        self.__modDeserial.doneIter()
        # remove the temporary module and its compiled version (*.pyc)
        os.remove(self.__filename)
        try: # py3.2+ uses special folder/filename for .pyc files
            from imp import cache_from_source
            os.remove(cache_from_source(self.__filename))
        except ImportError:
            os.remove(self.__filename + 'c')

    def resetIter(self):
        self.__modDeserial.resetIter()

    def getDefinedTopics(self):
        return self.__modDeserial.getDefinedTopics()


TOPIC_TREE_FROM_MODULE = 'module'
TOPIC_TREE_FROM_STRING = 'string'
TOPIC_TREE_FROM_CLASS  = 'class'


class TopicDefnProvider(ITopicDefnProvider):
    """
    Default implementation of the ITopicDefnProvider API. This
    implementation accepts several formats for the topic tree 
    source data and delegates to a registered ITopicDefnDeserializer
    that converts source data into topic definitions. 
    
    This provider is instantiated automatically by 
    ``pub.addTopicDefnProvider(source, format)``
    when source is *not* an ITopicDefnProvider.
    
    Additional de-serializers can be registered via registerTypeForImport().
    """

    _typeRegistry = {}

    def __init__(self, source, format, **providerKwargs):
        """Find the correct de-serializer class from registry for the given
        format; instantiate it with given source and providerKwargs; get 
        all available topic definitions."""
        if format not in self._typeRegistry:
            raise UnrecognizedSourceFormatError()
        providerClassObj = self._typeRegistry[format]
        provider = providerClassObj(source, **providerKwargs)
        self.__topicDefns = {}
        self.__treeDocs = provider.getTreeDoc()
        try:
            topicDefn = provider.getNextTopic()
            while topicDefn is not None:
                self.__topicDefns[topicDefn.nameTuple] = topicDefn
                topicDefn = provider.getNextTopic()
        finally:
            provider.doneIter()

    def getDefn(self, topicNameTuple):
        desc, spec = None, None
        defn = self.__topicDefns.get(topicNameTuple, None)
        if defn is not None:
            assert defn.isComplete()
            desc = defn.description
            spec = ArgSpecGiven(defn.argsDocs, defn.required)
        return desc, spec

    def topicNames(self):
        return py2and3.iterkeys(self.__topicDefns)

    def getTreeDoc(self):
        return self.__treeDocs

    @classmethod
    def registerTypeForImport(cls, typeName, providerClassObj):
        """If a new type of importer is defined for topic definitions, it
        can be registered with pubsub by providing a name for the new 
        importer (typeName), and the class to instantiate when 
        pub.addTopicDefnProvider(obj, typeName) is called. For instance, ::  
        
            from pubsub.core.topicdefnprovider import ITopicDefnDeserializer
            class SomeNewImporter(ITopicDefnDeserializer): 
                ...
            TopicDefnProvider.registerTypeForImport('some name', SomeNewImporter)
            # will instantiate SomeNewImporter(source)
            pub.addTopicDefnProvider(source, 'some name') 
        """
        assert issubclass(providerClassObj, ITopicDefnDeserializer)
        cls._typeRegistry[typeName] = providerClassObj

    @classmethod
    def initTypeRegistry(cls):
        cls.registerTypeForImport(TOPIC_TREE_FROM_MODULE, TopicDefnDeserialModule)
        cls.registerTypeForImport(TOPIC_TREE_FROM_STRING, TopicDefnDeserialString)
        cls.registerTypeForImport(TOPIC_TREE_FROM_CLASS,  TopicDefnDeserialClass)


TopicDefnProvider.initTypeRegistry()


def _backupIfExists(filename, bak):
    import os, shutil
    if os.path.exists(filename):
        backupName = '%s.%s' % (filename, bak)
        shutil.copy(filename, backupName)


defaultTopicTreeSpecHeader = \
"""
Topic tree for application.
Used via pub.addTopicDefnProvider(thisModuleName).
"""

defaultTopicTreeSpecFooter = \
"""\
# End of topic tree definition. Note that application may load
# more than one definitions provider.
"""


def exportTopicTreeSpec(moduleName = None, rootTopic=None, bak='bak', moduleDoc=None):
    """Using TopicTreeSpecPrinter, exports the topic tree rooted at rootTopic to a
    Python module (.py) file. This module will define module-level classes 
    representing root topics, nested classes for subtopics etc. Returns a string 
    representing the contents of the file. Parameters:

        - If moduleName is given, the topic tree is written to moduleName.py in
          os.getcwd(). By default, it is first backed up, it it already exists, 
          using bak as the filename extension. If bak is None, existing module file 
          gets overwritten. 
        - If rootTopic is specified, the export only traverses tree from 
          corresponding topic. Otherwise, complete tree, using 
          pub.getDefaultTopicTreeRoot() as starting  point.
        - The moduleDoc is the doc string for the module ie topic tree.
    """

    if rootTopic is None:
        from .. import pub
        rootTopic = pub.getDefaultTopicMgr().getRootAllTopics()
    elif py2and3.isstring(rootTopic):
        from .. import pub
        rootTopic = pub.getDefaultTopicMgr().getTopic(rootTopic)

    # create exporter
    if moduleName is None:
        capture = py2and3.StringIO()
        TopicTreeSpecPrinter(rootTopic, fileObj=capture, treeDoc=moduleDoc)
        return capture.getvalue()

    else:
        filename = '%s.py' % moduleName
        if bak:
            _backupIfExists(filename, bak)
        moduleFile = open(filename, 'w')
        try:
            TopicTreeSpecPrinter(rootTopic, fileObj=moduleFile, treeDoc=moduleDoc)
        finally:
            moduleFile.close()

##############################################################

class TopicTreeSpecPrinter:
    """
    Helper class to print the topic tree using the Python class
    syntax. The "printout" can be sent to any file object (object that has a
    write() method). If printed to a module, the module can be imported and
    given to pub.addTopicDefnProvider(module, 'module'). Importing the module 
    also provides code completion of topic names (rootTopic.subTopic can be 
    given to any pubsub function requiring a topic name).
    """

    INDENT_CH = ' '
    #INDENT_CH = '.'

    def __init__(self, rootTopic=None, fileObj=None, width=70, indentStep=4, 
        treeDoc = defaultTopicTreeSpecHeader, footer = defaultTopicTreeSpecFooter):
        """For formatting, can specify the width of output, the indent step, the
        header and footer to print to override defaults. The destination is fileObj;
        if none is given, then sys.stdout is used. If rootTopic is given, calls
        writeAll(rootTopic) at end of __init__."""
        self.__traverser = TopicTreeTraverser(self)

        import sys
        fileObj = fileObj or sys.stdout

        self.__destination = fileObj
        self.__output = []
        self.__header = self.__toDocString(treeDoc)
        self.__footer = footer
        self.__lastWasAll = False # True when last topic done was the ALL_TOPICS

        self.__width   = width
        self.__wrapper = TextWrapper(width)
        self.__indentStep = indentStep
        self.__indent  = 0

        args = dict(width=width, indentStep=indentStep, treeDoc=treeDoc,
                    footer=footer, fileObj=fileObj)
        def fmItem(argName, argVal):
            if py2and3.isstring(argVal):
                MIN_OFFSET = 5
                lenAV = width - MIN_OFFSET - len(argName)
                if lenAV > 0:
                    argVal = repr(argVal[:lenAV] + '...')
            elif argName == 'fileObj':
                argVal = fileObj.__class__.__name__
            return '# - %s: %s' % (argName, argVal)
        fmtArgs = [fmItem(key, args[key]) for key in sorted(py2and3.iterkeys(args))]
        self.__comment = [
            '# Automatically generated by %s(**kwargs).' % self.__class__.__name__,
            '# The kwargs were:',
        ]
        self.__comment.extend(fmtArgs)
        self.__comment.extend(['']) # two empty line after comment
        
        if rootTopic is not None:
            self.writeAll(rootTopic)

    def getOutput(self):
        """Each line that was sent to fileObj was saved in a list; returns a
        string which is ``'\\n'.join(list)``."""
        return '\n'.join( self.__output )

    def writeAll(self, topicObj):
        """Traverse each topic of topic tree, starting at topicObj, printing
        each topic definition as the tree gets traversed. """
        self.__traverser.traverse(topicObj)

    def _accept(self, topicObj):
        # accept every topic
        return True

    def _startTraversal(self):
        # output comment
        self.__wrapper.initial_indent = '# '
        self.__wrapper.subsequent_indent = self.__wrapper.initial_indent
        self.__output.extend( self.__comment )

        # output header:
        if self.__header:
            self.__output.extend([''])
            self.__output.append(self.__header)
            self.__output.extend([''])

    def _doneTraversal(self):
        if self.__footer:
            self.__output.append('')
            self.__output.append('')
            self.__output.append(self.__footer)

        if self.__destination is not None:
            self.__destination.write(self.getOutput())

    def _onTopic(self, topicObj):
        """This gets called for each topic. Print as per specified content."""
        # don't print root of tree, it is the ALL_TOPICS builtin topic
        if topicObj.isAll():
            self.__lastWasAll = True
            return
        self.__lastWasAll = False

        self.__output.append( '' ) # empty line
        # topic name
        self.__wrapper.width = self.__width
        head = 'class %s:' % topicObj.getNodeName()
        self.__formatItem(head)

        # each extra content (assume constructor verified that chars are valid)
        self.__printTopicDescription(topicObj)
        if policies.msgDataProtocol != 'arg1':
            self.__printTopicArgSpec(topicObj)

    def _startChildren(self):
        """Increase the indent"""
        if not self.__lastWasAll:
            self.__indent += self.__indentStep

    def _endChildren(self):
        """Decrease the indent"""
        if not self.__lastWasAll:
           self.__indent -= self.__indentStep

    def __toDocString(self, msg):
        if not msg:
            return msg
        if msg.startswith("'''") or msg.startswith('"""'):
            return msg
        return '"""\n%s\n"""' % msg.strip()

    def __printTopicDescription(self, topicObj):
        if topicObj.getDescription():
            extraIndent = self.__indentStep
            self.__formatItem('"""', extraIndent)
            self.__formatItem( topicObj.getDescription(), extraIndent )
            self.__formatItem('"""', extraIndent)

    def __printTopicArgSpec(self, topicObj):
        extraIndent = self.__indentStep

        # generate the message data specification
        reqdArgs, optArgs = topicObj.getArgs()
        argsStr = []
        if reqdArgs:
            argsStr.append( ", ".join(reqdArgs) )
        if optArgs:
            optStr = ', '.join([('%s=None' % arg) for arg in optArgs])
            argsStr.append(optStr)
        argsStr = ', '.join(argsStr)

        # print it only if there are args; ie if listener() don't print it
        if argsStr:
            # output a blank line and protocol
            self.__formatItem('\n', extraIndent)
            protoListener = 'def %s(%s):' % (SPEC_METHOD_NAME, argsStr)
            self.__formatItem(protoListener, extraIndent)

            # and finally, the args docs
            extraIndent += self.__indentStep
            self.__formatItem('"""', extraIndent)
            # but ignore the arg keys that are in parent args docs:
            parentMsgKeys = ()
            if topicObj.getParent() is not None:
                parentMsgKeys = topicObj.getParent().getArgDescriptions().keys() # keys iter ok
            argsDocs = topicObj.getArgDescriptions()
            for key in sorted(py2and3.iterkeys(argsDocs)):
                if key not in parentMsgKeys:
                    argDesc = argsDocs[key]
                    msg = "- %s: %s" % (key, argDesc)
                    self.__formatItem(msg, extraIndent)
            self.__formatItem('"""', extraIndent)

    def __formatItem(self, item, extraIndent=0):
        indent = extraIndent + self.__indent
        indentStr = self.INDENT_CH * indent
        lines = item.splitlines()
        for line in lines:
            self.__output.append( '%s%s' % (indentStr, line) )

    def __formatBlock(self, text, extraIndent=0):
        self.__wrapper.initial_indent = self.INDENT_CH * (self.__indent + extraIndent)
        self.__wrapper.subsequent_indent = self.__wrapper.initial_indent
        self.__output.append( self.__wrapper.fill(text) )


