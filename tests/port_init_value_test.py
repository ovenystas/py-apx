import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import struct

class TestPortInitValue(unittest.TestCase):

   def test_record_init_value(self):
      port = apx.RequirePort('TestPort1', '{"x"S"y"S"z"S}','={3, 5, 8}')
      init_data = port.data_element.createInitData(port.init_value)
      self.assertEqual(init_data, struct.pack("<HHH",3,5,8))
   
      port = apx.RequirePort('TestPort1', '{"SensorData"{"x"S"y"S"z"S}"TimeStamp"L}','={{3, 5, 8},0xFFFFFFFF}')
      init_data = port.data_element.createInitData(port.init_value)
      self.assertEqual(init_data, struct.pack("<HHHL",3,5,8,0xFFFFFFFF))

      port = apx.RequirePort('TestPort1', '{"name"a[6]"Rectangle"{"x"L"y"L"width"L"height"L}}','={"",{0,0,0,0}}')
      init_data = port.data_element.createInitData(port.init_value)
      self.assertEqual(init_data, bytes(6)+struct.pack("<LLLL",0,0,0,0))
   

if __name__ == '__main__':
    unittest.main()