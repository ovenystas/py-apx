import apx
import remotefile

class FileManager(remotefile.FileManager):
   def __init__(self):
      super().__init__(apx.FileMap(), apx.FileMap())
    
   def attachNodeData(self, nodeData):
      if nodeData.outPortDataFile is not None:
         self.attachLocalFile(nodeData.outPortDataFile)
      if nodeData.definitionFile is not None:
         self.attachLocalFile(nodeData.definitionFile)
      if nodeData.inPortDataFile is not None:
         self.requestRemoteFile(nodeData.inPortDataFile)
   
   def __enter__(self):
      return self
   
   def __exit__(self, exc_type, exc_value, traceback):      
      super().stop()