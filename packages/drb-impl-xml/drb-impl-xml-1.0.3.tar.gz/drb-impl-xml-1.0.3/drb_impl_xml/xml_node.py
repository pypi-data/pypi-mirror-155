import re
from typing import Optional, Any, Union, List, Dict, Tuple
from typing.io import IO
from xml.etree.ElementTree import parse, Element
from xml.sax.handler import ContentHandler
from io import BufferedIOBase, RawIOBase

import drb
from drb import DrbNode, AbstractNode
from drb.utils.logical_node import DrbLogicalNode
from drb.path import ParsedPath
from drb.exceptions import DrbNotImplementationException, DrbException


def extract_namespace_name(value: str) -> Tuple[str, str]:
    """
    Extracts namespace and name from a tag of a Element

    Parameters:
        value: XML element tag

    Returns:
          tuple: a tuple containing the extracted namespace and name
    """
    ns, name = re.match(r'({.*})?(.*)', value).groups()
    if ns is not None:
        ns = ns[1:-1]
    return ns, name


class XmlNode(AbstractNode):

    def __init__(self, element: Element, parent: DrbNode = None, **kwargs):
        AbstractNode.__init__(self)
        namespace_uri, name = extract_namespace_name(element.tag)
        self._name = name
        self._namespace_uri = namespace_uri
        if self._namespace_uri is None:
            self._namespace_uri = element.get('xmlns', None)
        if self._namespace_uri is None and parent is not None:
            self._namespace_uri = parent.namespace_uri

        self._parent = parent
        self._attributes = None
        self._children = None
        self._elem: Element = element
        self._occurrence = kwargs.get('occurrence', 1)

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self._namespace_uri

    @property
    def value(self) -> Optional[Any]:
        if self.has_child():
            return None
        return self._elem.text

    @property
    def path(self) -> ParsedPath:
        if self._parent is None:
            return ParsedPath(f'/{self._name}')
        return self.parent.path / self.name

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            for k, v in self._elem.attrib.items():
                ns, name = extract_namespace_name(k)
                if name != 'xmlns' or ns is not None:
                    self._attributes[(name, ns)] = v
        return self._attributes

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            occurrences = {}
            for elem in self._elem:
                namespace, name = extract_namespace_name(elem.tag)
                occurrence = occurrences.get(name, 0) + 1
                occurrences[name] = occurrence
                self._children.append(
                    XmlNode(elem, self, occurrence=occurrence))
        return self._children

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) -> \
            Union[DrbNode, List[DrbNode]]:
        tag = f'ns:{name}'
        named_children = self._elem.findall(tag, {'ns': '*'})

        if len(named_children) == 0:
            raise DrbException(f'No child found having name: {name} and'
                               f' namespace: {namespace_uri}')

        children = [XmlNode(named_children[i], self, occurrence=i+1)
                    for i in range(len(named_children))]
        if self.namespace_aware or namespace_uri is not None:
            children = list(
                filter(lambda n: n.namespace_uri == namespace_uri, children))

        return children[occurrence]

    def has_impl(self, impl: type) -> bool:
        return impl == str and not self.has_child()

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            return self.value
        raise DrbNotImplementationException(
            f"XmlNode doesn't implement {impl}")

    def close(self) -> None:
        pass

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        try:
            return self.attributes[name, namespace_uri]
        except KeyError:
            raise DrbException(f'No attribute ({name}:{namespace_uri}) found!')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name is None and namespace is None:
            return len(self.children) > 0

        tag = f'ns:{name}'

        if namespace is None:
            if not self.namespace_aware:
                ns = {'ns': "*"}
            else:
                tag = name
                ns = {}
        else:
            ns = {'ns': namespace}

        found = self._elem.find(tag, ns)

        if found is not None:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.path.name) + hash(self._occurrence)


class XmlSaxNode(DrbLogicalNode):
    def __init__(self, node: DrbNode, occurrence: int = 1):
        DrbLogicalNode.__init__(self, node.name,
                                parent=node.parent,
                                namespace_uri=node.namespace_uri)
        for key, value in node.attributes.items():
            self.add_attribute(key[0], value, key[1])
        self.__occurrence = occurrence

    def __hash__(self):
        return hash((self.path.name, self.__occurrence))

    def __str__(self):
        return f"XmlSaxNode[{self.namespace_uri}:{self.name}]"


class _NamespaceManager(object):
    """
    Manage XML namespace inheritance and allowing to retrieve the corresponding
    namespace at each tag level in the XML data.
    """
    def __init__(self):
        self.__namespaces = []
        self.__default_ns = []

    def retrieve_namespace(self, prefix: str = None) -> str:
        """
        Retrieves a namespace URI from the given `prefix` or returns the
        current default namespace if `prefix` is not specified.

        Parameters:
            prefix (str): (optional) namespace URI prefix
        Returns:
            str: namespace URI associated to the given `prefix` or the current
                 default namespace URI if `prefix` is ``None``
        """
        if prefix is None:
            return next((ns for ns in reversed(self.__default_ns)
                         if ns is not None), None)

        for i in reversed(range(len(self.__namespaces))):
            namespace = self.__namespaces[i].get(prefix, None)
            if namespace is not None:
                return namespace

    def on_fragment_start(self, tag: str, attrs) -> None:
        """
        Opens and initializes a new namespace scope for a new fragment

        Parameters:
             tag (str): tag name (may contain a namespace prefix)
             attrs: tag attributes
        """
        # initialize new fragment namespace scope
        self.__namespaces.append({})
        self.__default_ns.append(None)

        # retrieve all namespace defined from attrs
        namespaces = list(filter(lambda x: x.startswith('xmlns'),
                                 attrs.keys()))
        namespaces = {k: attrs.getValue(k) for k in namespaces}

        # append namespaces in the current scope
        for ns_prefix, uri in namespaces.items():
            prefix = ns_prefix[6:]
            if prefix == '':
                self.__default_ns[-1] = uri
            else:
                self.__namespaces[-1][prefix] = uri

        tag_composition = tag.split(':', 1)
        if len(tag_composition) == 2:
            self.__default_ns[-1] = self.retrieve_namespace(tag_composition[0])

    def on_fragment_end(self) -> None:
        """
        Closes and the namespace scope of the current fragment
        """
        self.__default_ns.pop()
        self.__namespaces.pop()

    def extract_namespace_name(self, tag: str) -> Tuple[Optional[str], str]:
        """
        Retrieves the namespace and the name of the given XML tag.

        Parameters:
            tag: a XML tag
        Returns:
            tuple: the namespace and name of the given tag (namespace may be
            ``None``)
        """
        tag_composition = tag.split(':', 1)
        if len(tag_composition) == 2:
            return (self.retrieve_namespace(tag_composition[0]),
                    tag_composition[1])
        return self.retrieve_namespace(), tag


class SaxNodeHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.__root: DrbLogicalNode = None
        self.__parents: List[DrbLogicalNode] = []
        self.__current: DrbLogicalNode = None
        self.__ns_mng: _NamespaceManager = _NamespaceManager()

    def __extract_attributes(self, attrs) -> \
            List[Tuple[str, Any, Optional[str]]]:
        attributes = filter(lambda x: not x[0].startswith('xmlns'),
                            attrs.items())
        node_attributes = []
        for name, value in attributes:
            ns_name = name.split(':', 1)
            if len(ns_name) == 2:
                node_attributes.append((
                    ns_name[1],
                    value,
                    self.__ns_mng.retrieve_namespace(ns_name[0])))
            else:
                node_attributes.append((name, value, None))
        return node_attributes

    def startElement(self, name, attrs):
        self.startElementNS(name, None, attrs)

    def endElement(self, name):
        self.endElementNS(name, None)

    def startElementNS(self, name, qname, attrs):
        self.__ns_mng.on_fragment_start(name, attrs)
        namespace, name = self.__ns_mng.extract_namespace_name(name)
        attributes = self.__extract_attributes(attrs)

        # prepare node
        node = DrbLogicalNode(name, namespace_uri=namespace)
        for n, v, ns in attributes:
            node.add_attribute(n, v, ns)

        # case: first XML tag
        if self.__root is None:
            node = XmlSaxNode(node)
            self.__root = node
        else:
            parent = self.__parents[-1]
            try:
                occurrence = len(self.__parents[-1][name, namespace, :]) + 1
            except KeyError:
                occurrence = 1
            node = XmlSaxNode(node, occurrence)
            parent.append_child(node)

        self.__parents.append(node)
        self.__current = node

    def endElementNS(self, name, qname):
        self.__ns_mng.on_fragment_end()
        self.__parents.pop()
        self.__current = None

    def characters(self, content):
        text = ''.join(content.split())
        if text != '' and self.__current is not None:
            if self.__current.value is None:
                self.__current.value = content
            else:
                self.__current.value += content

    def get_node(self):
        return self.__root


class XmlBaseNode(AbstractNode):
    """
    This class represents a single node of a tree of data.
    When the data came from another implementation.

    Parameters:
        node (DrbNode): the base node of this node.
        source(Union[BufferedIOBase, RawIOBase, IO]): The xml data.
    """
    def __init__(self, node: DrbNode, source: Union[BufferedIOBase, IO]):
        super().__init__()
        self.__base_node = node
        self.__source = source
        self.__xml_node = XmlNode(parse(source).getroot(), node)

    @property
    def name(self) -> str:
        return self.__base_node.name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self.__base_node.namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return self.__base_node.value

    @property
    def path(self) -> ParsedPath:
        return self.__base_node.path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__base_node.parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self.__base_node.attributes

    @property
    def children(self) -> List[DrbNode]:
        return [self.__xml_node]

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if name is None and namespace is None:
            return True

        if namespace is not None or self.namespace_aware:
            if self.__xml_node.namespace_uri != namespace:
                return False

        if self.__xml_node.name == name:
            return True

        return False

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self.__base_node.get_attribute(name, namespace_uri)

    def has_impl(self, impl: type) -> bool:
        return self.__base_node.has_impl(impl)

    def get_impl(self, impl: type, **kwargs) -> Any:
        return self.__base_node.get_impl(impl)

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) -> \
            Union[DrbNode, List[DrbNode]]:
        if self.__xml_node.name == name and \
                ((not self.namespace_aware and namespace_uri is None)
                 or self.__xml_node.namespace_uri == namespace_uri):
            return [self.__xml_node][occurrence]
        raise DrbException(f'No child found having name: {name} and'
                           f' namespace: {namespace_uri}')

    def close(self) -> None:
        self.__base_node.close()
