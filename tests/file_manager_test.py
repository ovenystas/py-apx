import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import time

class TestFileManager(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_workerStartStop(self):
      #test explicit shutdown using stop method
      mgr = apx.ApxFileManager()
      mgr.start()      
      mgr.stop()
      self.assertEqual(mgr.worker, None)
   
   def test_fileManagerWithNode(self):      
      node = apx.Node('Simulator')

      node.dataTypes.append(apx.RawDataType('InactiveActive_T','C(0,3)'))
      node.providePorts.append(apx.RawProvidePort('VehicleSpeed','S','=65535'))
      node.providePorts.append(apx.RawProvidePort('MainBeam','T[0]','=3'))
      node.providePorts.append(apx.RawProvidePort('FuelLevel','C'))
      node.providePorts.append(apx.RawProvidePort('ParkBrakeActive','T[0]','=3'))
      node.requirePorts.append(apx.RawRequirePort('RheostatLevel','C','=255'))
      nodeData = apx.NodeData(node)
      fileManager = apx.ApxFileManager()
      fileManager.attachNodeData(nodeData)
      fileManager.start()
      fileManager.stop()
      


if __name__ == '__main__':
    unittest.main()   

