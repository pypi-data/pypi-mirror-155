from . import _version
from .xml_node import XmlNode, XmlBaseNode, XmlSaxNode
from .xml_node_factory import XmlNodeFactory

__version__ = _version.get_versions()['version']
__all__ = ['XmlBaseNode', 'XmlNode', 'XmlSaxNode', 'XmlNodeFactory']
