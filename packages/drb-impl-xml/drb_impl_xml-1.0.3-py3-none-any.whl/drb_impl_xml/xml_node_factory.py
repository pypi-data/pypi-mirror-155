import os
from io import BufferedIOBase, StringIO
from typing import Union
from drb import DrbNode
from drb.utils.logical_node import DrbLogicalNode
from drb.factory.factory import DrbFactory
from drb.exceptions import DrbFactoryException
from .xml_node import XmlBaseNode


class XmlNodeFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if node.has_impl(BufferedIOBase):
            return XmlBaseNode(node, node.get_impl(BufferedIOBase))

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        if isinstance(source, str):
            base_node = DrbLogicalNode("/")
            if os.path.exists(source):
                return XmlBaseNode(base_node, source)[0]
            return XmlBaseNode(base_node, StringIO(source))[0]
        elif isinstance(source, DrbNode):
            return self._create(source)
        raise DrbFactoryException(f'Invalid parameter type: {type(source)}')
