import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest

class TestPortAttribute(unittest.TestCase):

   def test_integer_init_value(self):
      attr = apx.base.PortAttribute('=0')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.value, 0)
      
      attr = apx.base.PortAttribute('=255')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.value, 255)
      
      attr = apx.base.PortAttribute('={3,3,7}')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_LIST)
      self.assertEqual(len(attr.initValue.elements), 3)
      self.assertEqual(attr.initValue.elements[0].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[0].value, 3)
      self.assertEqual(attr.initValue.elements[1].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[1].value, 3)
      self.assertEqual(attr.initValue.elements[2].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[2].value, 7)

   def test_string_init_value(self):
      attr = apx.base.PortAttribute('="InitValue"')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.value, "InitValue")

      attr = apx.base.PortAttribute('=""')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.value, "")

      attr = apx.base.PortAttribute('={"a","b","", "c"}')
      self.assertEqual(attr.isQueued, False)
      self.assertEqual(attr.isParameter, False)
      self.assertEqual(attr.initValue.valueType, apx.VTYPE_LIST)
      self.assertEqual(len(attr.initValue.elements), 4)
      self.assertEqual(attr.initValue.elements[0].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[0].value, "a")
      self.assertEqual(attr.initValue.elements[1].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[1].value, "b")
      self.assertEqual(attr.initValue.elements[2].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[2].value, "")
      self.assertEqual(attr.initValue.elements[3].valueType, apx.VTYPE_SCALAR)
      self.assertEqual(attr.initValue.elements[3].value, "c")

if __name__ == '__main__':
    unittest.main()