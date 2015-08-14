"""
Contributed by Joshua R English, adapted by Oliver Schoenborn to be 
consistent with pubsub API. 

An extension for pubsub (http://pubsub.sourceforge.net) so topic tree 
specification can be encoded in XML format rather than pubsub's default 
Python nested class format.

To use:

    xml = '''
        <topicdefntree>
        <description>Test showing topic hierarchy and inheritance</description>
        <topic id="parent">
            <description>Parent with a parameter and subtopics</description>
            <listenerspec>
                <arg id="name" optional="true">given name</arg>
                <arg id="lastname">surname</arg>
            </listenerspec>

            <topic id="child">
                <description>This is the first child</description>
                <listenerspec>
                    <arg id="nick">A nickname</arg>
                </listenerspec>
            </topic>
        </topic>
        </topicdefntree>
    '''

These topic definitions are loaded through an XmlTopicDefnProvider:

    pub.addTopicDefnProvider( XmlTopicDefnProvider(xml) )

The XmlTopicDefnProvider also accepts a filename instead of XML string: 

    provider = XmlTopicDefnProvider("path/to/XMLfile.xml", TOPIC_TREE_FROM_FILE)
    pub.addTopicDefnProvider( provider )

Topics can be exported to an XML file using the exportTopicTreeSpecXml function.
This will create a text file for the XML and return the string representation
of the XML tree.

:copyright: Copyright since 2013 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

__author__ = 'Joshua R English'
__revision__ = 6
__date__ = '2013-07-27'


from ..core.topictreetraverser import ITopicTreeVisitor
from ..core.topicdefnprovider import (
    ITopicDefnProvider,
    ArgSpecGiven,
    TOPIC_TREE_FROM_STRING,
    )
from .. import py2and3

try:
    from elementtree import ElementTree as ET
except ImportError:
    try: # for Python 2.4, must use cElementTree:
        from xml.etree import ElementTree as ET
    except ImportError:
        from cElementTree import ElementTree as ET

__all__ = [
    'XmlTopicDefnProvider',
    'exportTopicTreeSpecXml',
    'TOPIC_TREE_FROM_FILE'
    ]

    
def _get_elem(elem):
    """Assume an ETree.Element object or a string representation.
    Return the ETree.Element object"""
    if not ET.iselement(elem):
        try:
            elem = ET.fromstring(elem)
        except:
            py2and3.print_("Value Error", elem)
            raise ValueError("Cannot convert to element")
    return elem

    
TOPIC_TREE_FROM_FILE = 'file'


class XmlTopicDefnProvider(ITopicDefnProvider):

    class XmlParserError(RuntimeError): pass

    class UnrecognizedSourceFormatError(ValueError): pass
    
    def __init__(self, xml, format=TOPIC_TREE_FROM_STRING):
        self._topics = {}
        self._treeDoc = ''
        if format == TOPIC_TREE_FROM_FILE:
            self._parse_tree(_get_elem(open(xml,mode="r").read()))
        elif format == TOPIC_TREE_FROM_STRING:
            self._parse_tree(_get_elem(xml))
        else:
            raise UnrecognizedSourceFormatError()

    def _parse_tree(self, tree):
        doc_node = tree.find('description')

        if doc_node is None:
            self._treeDoc = "UNDOCUMENTED"
        else:
            self._treeDoc = ' '.join(doc_node.text.split())

        for node in tree.findall('topic'):
            self._parse_topic(node)

    def _parse_topic(self, node, parents=None, specs=None, reqlist=None):
        parents = parents or []
        specs = specs or {}
        reqlist = reqlist or []

        descNode = node.find('description')

        if descNode is None:
            desc = "UNDOCUMENTED"
        else:
            desc = ' '.join(descNode.text.split())

        node_id = node.get('id')
        if node_id is None:
            raise XmlParserError("topic element must have an id attribute")

        for this in (node.findall('listenerspec/arg')):
            this_id = this.get('id')
            if this_id is None:
                raise XmlParserError("arg element must have an id attribute")

            this_desc = this.text.strip()
            this_desc = this_desc or "UNDOCUMENTED"
            this_desc = ' '.join(this_desc.split())

            specs[this_id] = this_desc

            if this.get('optional', '').lower() not in ['true', 't','yes','y']:
                reqlist.append(this_id)

        defn = ArgSpecGiven(specs, tuple(reqlist))

        parents.append(node.get('id'))

        self._topics[tuple(parents)] = desc, defn

        for subtopic in node.findall('topic'):
            self._parse_topic(subtopic, parents[:], specs.copy(), reqlist[:])


    def getDefn(self, topicNameTuple):
        return self._topics.get(topicNameTuple, (None, None))

    def topicNames(self):
        return py2and3.iterkeys(self._topics) # dict_keys iter in 3, list in 2

    def getTreeDoc(self):
        return self._treeDoc

    
class XmlVisitor(ITopicTreeVisitor):
    def __init__(self, elem):
        self.tree = elem
        self.known_topics = []

    def _startTraversal(self):
        self.roots = [self.tree]

    def _onTopic(self, topicObj):
        if topicObj.isAll():
            self.last_elem = self.tree
            return
        if self.roots:
            this_elem = ET.SubElement(self.roots[-1], 'topic',
                {'id':topicObj.getNodeName()})
        else:
            this_elem = ET.Element('topic', {'id':topicObj.getNodeName()})
        req, opt = topicObj.getArgs()
        req = req or ()
        opt = opt or ()
        desc_elem = ET.SubElement(this_elem, 'description')
        topicDesc = topicObj.getDescription()
        if topicDesc:
            desc_elem.text = ' '.join(topicDesc.split()) 
        else:
            desc_elem.text = "UNDOCUMENTED"
        argDescriptions = topicObj.getArgDescriptions()

        # pubsub way of getting known_args
        known_args = []
        parent = topicObj.getParent()
        while parent:
            if parent in self.known_topics:
                p_req, p_opt = parent.getArgs()
                if p_req:
                    known_args.extend(p_req)
                if p_opt:
                    known_args.extend(p_opt)
            parent = parent.getParent()

        # there is probably a cleaner way to do this
        if req or opt:
            spec = ET.SubElement(this_elem, 'listenerspec')
            for arg in req:
                if arg in known_args:
                    continue
                arg_elem = ET.SubElement(spec, 'arg', {'id': arg})
                arg_elem.text = ' '.join(argDescriptions.get(arg, 'UNDOCUMENTED').split())
            for arg in opt:
                if arg in known_args:
                    continue
                arg_elem = ET.SubElement(spec, 'arg', {'id': arg, 'optional':'True'})
                arg_elem.text = ' '.join(argDescriptions.get(arg, 'UNDOCUMENTED').split())

        self.last_elem = this_elem
        self.known_topics.append(topicObj)

    def _startChildren(self):
        self.roots.append(self.last_elem)

    def _endChildren(self):
        self.roots.pop()

        
## http://infix.se/2007/02/06/gentlemen-indent-your-xml
def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        else:
            elem.tail="\n"


def exportTopicTreeSpecXml(moduleName=None, rootTopic=None, bak='bak', moduleDoc=None):
    """
    If rootTopic is None, then pub.getDefaultTopicTreeRoot() is assumed.
    """

    if rootTopic is None:
        from .. import pub
        rootTopic = pub.getDefaultTopicTreeRoot()
    elif py2and3.isstring(rootTopic):
        from .. import pub
        rootTopic = pub.getTopic(rootTopic)

    tree = ET.Element('topicdefntree')
    if moduleDoc:
        mod_desc = ET.SubElement(tree, 'description')
        mod_desc.text = ' '.join(moduleDoc.split())

    traverser = pub.TopicTreeTraverser(XmlVisitor(tree))
    traverser.traverse(rootTopic)

    indent(tree)

    if moduleName:

        filename = '%s.xml' % moduleName
        if bak:
            pub._backupIfExists(filename, bak)

        fulltree= ET.ElementTree(tree)
        fulltree.write(filename, "utf-8", True)

    return ET.tostring(tree)




