import apx
import remotefile
import abc

class DataListener(metaclass=abc.ABCMeta):
   @abc.abstractmethod
   def on_data(self, port, data):
      """
      called by apx.client when a require port has updated its data
      """

@apx.NodeDataClient.register
class Client:
   """
   APX Client class for a single APX node
   """
   def __init__(self, node=None):
      self.providePortMap = None
      self.fileManager=apx.FileManager()
      self.socketAdapter=remotefile.TcpSocketAdapter()
      self.attachLocalNode(node)
      self.fileManager.start()
      self.dataListener=None
      
      
   
   def attachLocalNode(self, node):
      self.node=node if isinstance(node, apx.Node) else None
      if self.node is not None:
         self.nodeData=apx.NodeData(node)
         inPortDataFile = self.nodeData.inPortDataFile
         outPortDataFile = self.nodeData.outPortDataFile
         definitionDataFile = self.nodeData.definitionFile
         if inPortDataFile is not None:
            self.fileManager.requestRemoteFile(inPortDataFile)
         if outPortDataFile is not None:
            self.fileManager.attachLocalFile(outPortDataFile)
         if definitionDataFile is not None:
            self.fileManager.attachLocalFile(definitionDataFile)
         self.nodeData.nodeDataClient=self         
         self.providePortMap={}         
         for i,port in enumerate(self.node.providePorts):
            self.providePortMap[port.name]=i
            
   
   
   def createLocalNode(self, apxText):
      parser = apx.Parser()
      node = parser.loads(apxText)
      if node is not None:
         self.attachLocalNode(node)
      
   
   def connectTcp(self, address, port):
      self.socketAdapter.setReceiveHandler(self.fileManager)
      if self.socketAdapter.connect(address, port):         
         self.socketAdapter.start()
         return True
      else:
         return False
      
   def stop(self):
      self.socketAdapter.stop()
      self.fileManager.stop()
   
   def set_listener(self, dataListener):
      self.dataListener=dataListener

   def onRequirePortData(self, node, port, data):
      if self.dataListener:
         self.dataListener.on_data(port, data)
   
   def write_port(self, identifier, value):
      if isinstance(identifier, str):
         portId = self.providePortMap[identifier]         
      elif isinstance(identifier, int):
         portId = identifier
      else:
         raise ValueError(identifier)
      self.nodeData.writeProvidePort(portId, value)