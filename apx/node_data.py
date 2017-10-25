import apx
import abc
import struct
from collections import namedtuple

PortMapRange = namedtuple('PortMapRange', "startOffset endOffset port")

class NodeDataClient(metaclass=abc.ABCMeta):
   @abc.abstractmethod
   def onRequirePortData(self, node, portId, portName, data):
      """
      called by apx.NodeData when a require port has updated its data
      """


@apx.NodeDataHandler.register
class NodeData():
   """
   APX NodeData class
   """

   def __init__(self,node):
      parser = apx.Parser()
      if isinstance(node, apx.Node):
          self.node=node
          context=apx.Context()
          context.append(node)
          apx_text=context.dumps()
      elif isinstance(node, str):
         apx_text=node
         self.node = parser.loads(apx_text)
      else:
         raise NotImplementedError(type(node))

      self.name=self.node.name
      self.inPortDataMap = []
      self.outPortDataMap = []
      self.inPortDataFile = self._createInPortDataFile(self.node) if len(self.node.requirePorts)>0 else None
      self.outPortDataFile = self._createOutPortDataFile(self.node) if len(self.node.providePorts)>0 else None
      self.definitionFile = self._createDefinitionFile(node.name,apx_text)
      if self.inPortDataFile is not None:
         self.inPortDataFile.nodeDataHandler=self
      self.nodeDataClient=None


   def _createInPortDataFile(self, node):
      offset=0
      init_data = bytearray()
      for port in node.requirePorts:
         dataElement = port.dsg.resolveDataElement(node.dataTypes)
         packLen = port.dsg.packLen(node.dataTypes)         
         self.inPortDataMap.append(PortMapRange(offset, offset+packLen, port))
         offset+=packLen
         if port.attr is not None and port.attr.initValue is not None:
            init_data.extend(dataElement.createInitData(port.attr.initValue))
         else:
            init_data.extend(bytes(packLen)) #initialize with zeros if no init value has been selected
      file_len=offset
      assert(len(init_data)==file_len)
      if file_len > 0:
         file = apx.InputFile(node.name+'.in', file_len, init_data)         
         return file
      return None

   def _createOutPortDataFile(self, node):
      offset=0
      init_data = bytearray()
      for port in node.providePorts:
         dataElement = port.dsg.resolveDataElement(node.dataTypes)
         packLen = port.dsg.packLen(node.dataTypes)         
         self.outPortDataMap.append(PortMapRange(offset, offset+packLen, port))
         offset+=packLen
         if port.attr is not None and port.attr.initValue is not None:
            init_data.extend(dataElement.createInitData(port.attr.initValue))
         else:
            init_data.extend(bytes(packLen)) #initialize with zeros if no init value has been selected         
      file_len=offset
      assert(len(init_data)==file_len)
      if file_len > 0:
         file = apx.OutputFile(node.name+'.out', file_len, init_data)         
         return file
      return None


   def _createDefinitionFile(self, node_name, apx_text):
      file = apx.OutputFile(node_name+'.apx', len(apx_text))
      file.write(0,bytes(apx_text, encoding='ascii'))
      return file

   def inPortDataWriteNotify(self, file, offset: int, data : bytes):
      """
      Called by FileManager when it receives a remote write in the node's inPortData file
      """
      if self.nodeDataClient is not None:
         startOffset=offset
         endOffset=offset+len(data)
         while offset<endOffset:
            found=False
            for portId,elem in enumerate(self.inPortDataMap):
               if elem.startOffset <= offset < elem.endOffset:
                  offset=elem.endOffset
                  found=True
                  value = self._unpackRequirePort(elem.port, data[elem.startOffset-startOffset:elem.endOffset-startOffset])
                  self.nodeDataClient.onRequirePortData(self, portId, elem.port.name, value)
                  break
            if found == False:
               break

   def writeProvidePort(self, portId, value):
      port = self.node.providePorts[portId]
      portMapElem = self.outPortDataMap[portId]
      dataElement = port.dsg.resolveDataElement(node.dataTypes)
      
      raise NotImplementedError('writeProvidePort')

   def _unpackRequirePort(self, port, data):
      raise NotImplementedError('_unpackRequirePort')

