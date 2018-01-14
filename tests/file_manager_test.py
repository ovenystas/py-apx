import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import time

class MockTransmitHandler(remotefile.TransmitHandler):
   def __init__(self):
      self.transmittedData=bytearray()
   
   def send(self, data):      
      self.transmittedData.extend(data)      
   

class TestFileManager(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_workerStartStop(self):
      #test explicit shutdown using stop method
      mgr = apx.FileManager()
      mgr.start()      
      mgr.stop()
      self.assertEqual(mgr.worker, None)
   
   def test_fileManagerWithNode(self):      
      node = apx.Node('Simulator')

      node.dataTypes.append(apx.DataType('InactiveActive_T','C(0,3)'))
      node.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
      node.append(apx.ProvidePort('MainBeam','T[0]','=3'))
      node.append(apx.ProvidePort('FuelLevel','C'))
      node.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
      node.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
      nodeData = apx.NodeData(node)
      fileManager = apx.FileManager()
      fileManager.attachNodeData(nodeData)
      self.assertEqual(len(fileManager.localFileMap), 2)
      self.assertEqual(len(fileManager.requestedFiles), 1)
      fileManager.start()
      mockHandler = MockTransmitHandler()
      fileManager.onConnected(mockHandler)
      time.sleep(0.1)      
      self.assertEqual(len(mockHandler.transmittedData), 4+63*2)
      fileManager.stop()
      


if __name__ == '__main__':
    unittest.main()   

